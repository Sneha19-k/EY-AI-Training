import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from simpleeval import simple_eval
import os
import re
import logging

# -------------------------------------------------
# ✅ Setup Logging to app.log
# -------------------------------------------------
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - QUERY: %(message)s",
)

def log_event(query, response):
    logging.info(f"{query} -> RESPONSE: {response}")


# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Query Assistant",
    page_icon="🤖",
    layout="centered"
)

# Initialize LangChain with OpenRouter
@st.cache_resource
def get_llm():
    api_key = os.getenv("OPENROUTER_API_KEY")
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

    return ChatOpenAI(
        model="mistralai/mistral-7b-instruct",
        temperature=0.7,
        max_tokens=256,
        api_key=api_key,
        base_url=base_url,
    )


def process_query(query: str) -> str:
    """Process the query and return appropriate response"""
    query = query.strip()

    if not query:
        return "⚠️ Query cannot be empty"

    # ✅ Reverse the word logic
    match_reverse = re.match(r"reverse the word (\w+)", query, re.IGNORECASE)
    if match_reverse:
        word = match_reverse.group(1)
        result = word[::-1]
        log_event(query, result)
        return result

    # ✅ Try math expression safely
    try:
        safe_query = re.sub(r'[^0-9\+\-\*/\.\(\)\s]', '', query)
        if safe_query:
            result = str(simple_eval(safe_query))
            log_event(query, result)
            return result
    except:
        pass

    # ✅ Otherwise send to LLM
    try:
        llm = get_llm()
        result = llm.invoke(query)
        response = result.content
        log_event(query, response)
        return response

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        log_event(query, error_msg)
        return error_msg


# -------------------------------------------------
# ✅ Streamlit UI
# -------------------------------------------------

st.title("🤖 AI Query Assistant")
st.markdown("Ask me anything! I can solve math, reverse words, or answer questions.")

with st.form(key="query_form"):
    user_query = st.text_area(
        "Enter your query:",
        height=100,
        placeholder="eg : What is 25 * 4?"
    )
    submit_button = st.form_submit_button("Submit", use_container_width=True)

if submit_button:
    if user_query:
        with st.spinner("Processing your query..."):
            response = process_query(user_query)

        st.success("Response:")
        st.write(response)
    else:
        st.warning("Please enter a query before submitting.")

# Sidebar Examples
with st.sidebar:
    st.header("📋 Example Queries")
    st.markdown("""
    **Math:**
    - `25 * 4 + 10`
    - `(100 - 25) / 5`

    **Word Reverse:**
    - `reverse the word hello`
    - `reverse the word python`

    **AI Questions:**
    - `What is artificial intelligence?`
    - `Explain the solar system`
    """)
    st.divider()
    st.caption("Powered by Mistral-7B via OpenRouter")

# Store history
if "history" not in st.session_state:
    st.session_state.history = []

if submit_button and user_query:
    st.session_state.history.append({
        "query": user_query,
        "response": response
    })

if st.session_state.history:
    with st.expander("📜 Query History"):
        for i, item in enumerate(reversed(st.session_state.history[-5:]), 1):
            st.markdown(f"**Q{i}:** {item['query']}")
            st.markdown(f"**A{i}:** {item['response']}")
            st.divider()
