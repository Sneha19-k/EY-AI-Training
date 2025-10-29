# ============================================================
# Memory-Tools.py — Conversational Mistral Agent (fully working)
# ============================================================

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from textblob import TextBlob  # Import TextBlob for sentiment analysis

# ------------------------------------------------------------
# 1. Load environment variables
# ------------------------------------------------------------
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

# ------------------------------------------------------------
# 2. Initialize the Mistral model via OpenRouter
# ------------------------------------------------------------
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.4,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)


# ------------------------------------------------------------
# 3. Define helper tools
# ------------------------------------------------------------

def greet(name: str) -> str:
    """Return a friendly greeting."""
    name = name.strip().replace('"', "").replace("'", "")
    return f"Hello {name}, welcome to the AI Agent demo!"


def sentiment_analyze(text: str) -> str:
    """Analyze the sentiment of the text and return a sentiment category."""
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity  # range from -1 (negative) to 1 (positive)

    if sentiment_score > 0:
        return "positive"
    elif sentiment_score < 0:
        return "negative"
    else:
        return "neutral"


# ------------------------------------------------------------
# 4. Initialize memory
# ------------------------------------------------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ------------------------------------------------------------
# 5. Conversational loop
# ------------------------------------------------------------
print("\n=== Start chatting with your Agent ===")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("\nConversation ended.")
        break

    # Handle Sentiment Analysis command
    if user_input.lower().startswith("analyze"):
        try:
            text_to_analyze = " ".join(user_input.split()[1:]).strip()
            if not text_to_analyze:
                print("Agent: Please provide text for sentiment analysis.")
                continue
            sentiment = sentiment_analyze(text_to_analyze)
            if sentiment == "positive":
                print("Agent: The sentiment is positive — happiness or contentment detected.")
            elif sentiment == "negative":
                print("Agent: The sentiment is negative — frustration or stress detected.")
            else:
                print("Agent: The sentiment is neutral — no strong emotion detected.")
            memory.save_context({"input": user_input}, {"output": sentiment})
            continue
        except Exception as e:
            print("Agent: Could not analyze the sentiment:", e)
            continue

    # Handle name introduction
    if "my name is" in user_input.lower():
        name = user_input.split("is")[-1].strip()
        memory.save_context({"input": user_input}, {"output": name})
        print("Agent:", greet(name))
        continue

    # Handle asking for name
    if "what" in user_input.lower() and "my name" in user_input.lower():
        messages = memory.load_memory_variables({}).get("chat_history", [])
        if messages:
            last_output = messages[-1].content
            print("Agent: You said your name is", last_output)
        else:
            print("Agent: I don't know your name yet.")
        continue

    # Default: use LLM
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print("Error:", e)
