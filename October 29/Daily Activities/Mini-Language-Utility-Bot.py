import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# ------------------------------------------------------------
# 1. Load environment variables (if needed for LLM API)
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
# 3. Define Helper Tools
# ------------------------------------------------------------

# Word Counter Tool
def count_words(sentence: str) -> str:
    """Count the number of words in a sentence."""
    word_count = len(sentence.split())
    return f"Agent: Your sentence has {word_count} words."

# Reverse Text Tool
def reverse_text(sentence: str) -> str:
    """Reverse the given sentence."""
    words = sentence.split()
    reversed_sentence = " ".join(reversed(words))
    return f"Agent: {reversed_sentence}"

# Vocabulary Helper Tool (using LLM for word definitions)
def define_word(word: str) -> str:
    """Use the LLM to define a word."""
    response = llm.invoke(f"Define the word '{word}'")
    return f"Agent: {response.content}"

# Uppercase / Lowercase Tool
def convert_case(sentence: str, case_type: str) -> str:
    """Convert text to uppercase or lowercase."""
    if case_type == 'upper':
        return f"Agent: {sentence.upper()}"
    elif case_type == 'lower':
        return f"Agent: {sentence.lower()}"
    else:
        return "Agent: Invalid case type. Please use 'upper' or 'lower'."

# Word Repeater Tool
def repeat_word(word: str, times: int) -> str:
    """Repeat a word a specified number of times."""
    repeated = " ".join([word] * times)
    return f"Agent: {repeated}"

# ------------------------------------------------------------
# 4. Conversational loop (Simpler without advanced memory features)
# ------------------------------------------------------------
print("\n=== Start chatting with your Mini Language Utility Bot ===")
print("Type 'exit' to quit.\n")

# Simple in-memory conversation history (using a list of inputs and outputs)
conversation_history = []

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("\nConversation ended.")
        break

    # Handle Word Counter command
    if user_input.lower().startswith("count"):
        sentence = " ".join(user_input.split()[1:]).strip()
        if not sentence:
            print("Agent: Please provide a sentence to count the words.")
            continue
        result = count_words(sentence)
        print(result)
        conversation_history.append(f"You: {user_input}")
        conversation_history.append(f"Agent: {result}")
        continue

    # Handle Reverse Text command
    if user_input.lower().startswith("reverse"):
        sentence = " ".join(user_input.split()[1:]).strip()
        if not sentence:
            print("Agent: Please provide a sentence to reverse.")
            continue
        result = reverse_text(sentence)
        print(result)
        conversation_history.append(f"You: {user_input}")
        conversation_history.append(f"Agent: {result}")
        continue

    # Handle Vocabulary Helper command
    if user_input.lower().startswith("define"):
        word = " ".join(user_input.split()[1:]).strip()
        if not word:
            print("Agent: Please specify a word to define.")
            continue
        result = define_word(word)
        print(result)
        conversation_history.append(f"You: {user_input}")
        conversation_history.append(f"Agent: {result}")
        continue

    # Handle Uppercase/Lowercase commands
    if user_input.lower().startswith("upper") or user_input.lower().startswith("lower"):
        parts = user_input.split()
        case_type = parts[0].lower()
        sentence = " ".join(parts[1:])
        if not sentence:
            print("Agent: Please provide text to convert.")
            continue
        result = convert_case(sentence, case_type)
        print(result)
        conversation_history.append(f"You: {user_input}")
        conversation_history.append(f"Agent: {result}")
        continue

    # Handle Word Repeater command
    if user_input.lower().startswith("repeat"):
        parts = user_input.split()
        word = parts[1]
        try:
            times = int(parts[2])
            if times <= 0:
                print("Agent: Please provide a positive number of repetitions.")
                continue
        except ValueError:
            print("Agent: Please provide a valid number of repetitions.")
            continue
        result = repeat_word(word, times)
        print(result)
        conversation_history.append(f"You: {user_input}")
        conversation_history.append(f"Agent: {result}")
        continue

    # Handle History command (prints all previous inputs and outputs)
    if user_input.lower() == "history":
        if conversation_history:
            print("\nAgent: Here is the conversation history:")
            for msg in conversation_history:
                print(msg)
        else:
            print("Agent: No conversation history available.")
        continue

    # Default: Use LLM for other queries
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        conversation_history.append(f"You: {user_input}")
        conversation_history.append(f"Agent: {response.content}")
    except Exception as e:
        print("Error:", e)
