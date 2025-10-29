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
# 3. Define Task Priority Classifier Tool
# ------------------------------------------------------------

def classify_task_priority(task: str) -> str:
    """Classify task priority based on keywords."""
    # Keywords for high priority tasks
    high_priority_keywords = ["tonight", "today", "ASAP", "urgent", "deadline", "immediately"]
    low_priority_keywords = ["snacks", "office", "meeting", "review", "admin", "miscellaneous"]

    task_lower = task.lower()

    # Check for high priority keywords
    if any(keyword in task_lower for keyword in high_priority_keywords):
        return f"Agent: Task \"{task}\" marked as HIGH priority."

    # Check for low priority keywords
    if any(keyword in task_lower for keyword in low_priority_keywords):
        return f"Agent: Task \"{task}\" marked as LOW priority."

    # Default: medium priority if no keywords match
    return f"Agent: Task \"{task}\" marked as MEDIUM priority."


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

    # Handle Task Priority command
    if user_input.lower().startswith("priority"):
        try:
            task_text = " ".join(user_input.split()[1:]).strip()
            if not task_text:
                print("Agent: Please provide a task to prioritize.")
                continue
            priority_response = classify_task_priority(task_text)
            print(priority_response)
            memory.save_context({"input": user_input}, {"output": priority_response})
            continue

        except Exception as e:
            print("Error:", e)
            continue  # This ensures the program doesn't crash if an exception occurs

    # Default: use LLM for other queries
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print("Error:", e)
