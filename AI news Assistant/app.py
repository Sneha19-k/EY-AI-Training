import streamlit as st
from dotenv import load_dotenv
import os
from agents.orchestrator import run_news_pipeline

load_dotenv()  # load .env in local dev

st.set_page_config(page_title="📰 Multi-Agent News Assistant", layout="centered")

st.title("📰 Multi-Agent News Assistant (Streamlit)")

st.markdown(
    "Enter a topic, your email, and get a short summarized digest from multiple free news sources, "
    "summarized with Mistral (via OpenRouter)."
)

with st.form("news_form"):
    topic = st.text_input("Topic (keywords):", value="technology")
    email = st.text_input("Your email (to receive digest):", value="")
    send_copy = st.checkbox("Send digest via email", value=True)
    submitted = st.form_submit_button("Get my news")

if submitted:
    if send_copy and (not email or "@" not in email):
        st.error("Please enter a valid email address to receive the digest.")
    else:
        with st.spinner("Fetching articles and generating summaries..."):
            try:
                summaries = run_news_pipeline(topic, email if send_copy else "")
                st.success("Done — digest prepared and sent!" if send_copy else "Done — digest prepared!")
                st.markdown("---")
                for s in summaries:
                    st.markdown(f"### [{s['title']}]({s['url']})")
                    # show the summary (safe)
                    st.write(s['summary'])
                    st.markdown("---")
            except Exception as e:
                st.error(f"Error: {e}")
                st.exception(e)
