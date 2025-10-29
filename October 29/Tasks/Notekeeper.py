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
# 3. Define helper tools
# ------------------------------------------------------------

def greet(name: str) -> str:
    """Return a friendly greeting."""
    name = name.strip().replace('"', "").replace("'", "")
    return f"Hello {name}, welcome to the AI Agent demo!"


def note_keeper(action: str, note: str = None) -> str:
    """Store or retrieve notes."""
    if action.lower() == "note" and note:
        # Store note in memory
        memory_notes.append(note)
        return f"Agent: Noted: \"{note}\""

    if action.lower() == "get" and note.lower() == "notes":
        # Retrieve all stored notes
        if memory_notes:
            notes_str = "\n".join([f"\"{n}\"" for n in memory_notes])
            return f"Agent: You currently have {len(memory_notes)} note(s):\n{notes_str}"
        else:
            return "Agent: You don't have any notes yet."


# ------------------------------------------------------------
# 4. Initialize memory
# ------------------------------------------------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
memory_notes = []  # To store personal notes

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

    # Handle Note command: Store a note
    if user_input.lower().startswith("note"):
        try:
            note_text = " ".join(user_input.split()[1:]).strip()
            if not note_text:
                print("Agent: Please provide a note to remember.")
                continue
            response = note_keeper("note", note_text)
            print(response)
            memory.save_context({"input": user_input}, {"output": response})
            continue
        except Exception as e:
            print("Agent: Could not store the note:", e)
            continue

    # Handle Get Notes command: Retrieve all stored notes
    if user_input.lower() == "get notes":
        try:
            response = note_keeper("get", "notes")
            print(response)
            memory.save_context({"input": user_input}, {"output": response})
            continue
        except Exception as e:
            print("Agent: Could not retrieve notes:", e)
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
