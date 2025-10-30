

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# Load your .env file
load_dotenv()

# Map OpenRouter key to what CrewAI expects
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")

os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
# os.environ["OPENAI_MODEL_NAME"] = "mistralai/mistral-7b-instruct"
# llm = ChatOpenAI(model="mistralai/mistral-7b-instruct", temperature=0.7)
# --- User Input ---
topic = input("Enter a topic for research: ")

# --- Define Agents ---
researcher = Agent(
    role="Researcher",
    goal=f"Find information about {topic}",
    backstory="An AI researcher skilled at gathering reliable and up-to-date information."
)

writer = Agent(
    role="Writer",
    goal=f"Summarize research findings about {topic}",
    backstory="A writer skilled in creating clear and concise summaries."
)

# --- Define Tasks ---
task1 = Task(
    description=f"Research and gather key points, trends, and insights about {topic}.",
    expected_output="A list of bullet-point findings about the topic.",
    agent=researcher
)

task2 = Task(
    description=f"Write a short, readable summary based on the research findings about {topic}.",
    expected_output="A short paragraph summarizing the key insights about the topic.",
    agent=writer
)

# --- Create and Run the Crew ---
crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    verbose=False
)

result = crew.kickoff()

print("\n--- Final Output ---\n")
print(result)