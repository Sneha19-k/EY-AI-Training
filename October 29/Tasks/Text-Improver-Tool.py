import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

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
# 3. Define Text Improver Tool
# ------------------------------------------------------------

def improve_text(text: str) -> str:
    """Improve the clarity or professionalism of the text."""
    prompt = f"Rewrite the following text to make it clearer and more professional: '{text}'"
    try:
        response = llm.invoke(prompt)
        return f"Agent: Suggested rewrite: {response.content.strip()}"
    except Exception as e:
        return f"Agent: Could not improve the text: {e}"

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

    # Handle Text Improvement command
    if user_input.lower().startswith("improve"):
        try:
            text_to_improve = " ".join(user_input.split()[1:]).strip()
            if not text_to_improve:
                print("Agent: Please provide text to improve.")
                continue
            improved_text = improve_text(text_to_improve)
            print(improved_text)
            memory.save_context({"input": user_input}, {"output": improved_text})
            continue
        except Exception as e:
            print("Agent: Could not improve the text:", e)
            continue

    # Default: use LLM for other queries
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print("Error:", e)

