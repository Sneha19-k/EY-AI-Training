# main.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from agent import create_agents_and_tasks
from memory import memory

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

# Initialize the OpenAI model via OpenRouter
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.4,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

# Create the agents and tasks using CrewAI
crew = create_agents_and_tasks(llm)

# Conversational loop
print("\n=== Start chatting with your Agent ===")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("\nConversation ended.")
        break

    # Save the user's input to memory
    memory.save_context({"input": user_input}, {"output": user_input})

    # Use Crew to process the user input
    result = crew.kickoff(user_input)

    # Print the result from Crew (Text Improvement + Sentiment Analysis)
    print("Agent (Improved Text):", result[0])  # Text Improvement Result
    print("Agent (Sentiment Analysis):", result[1])  # Sentiment Analysis Result
