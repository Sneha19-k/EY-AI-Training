import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import requests

# Load environment variables from .env file
load_dotenv()

# Set up OpenRouter API Key for OpenAI
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# Initialize LangChain OpenAI API with OpenRouter integration
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# --- User Input ---
print("Welcome to the MovieBot! Tell me your preferences to get a movie recommendation.")
genre = input("What genre of movie are you interested in? (e.g., Action, Comedy, Drama): ")
mood = input("What mood are you in? (e.g., Happy, Sad, Excited): ")

# --- Define Agents ---
movie_recommender = Agent(
    role="MovieRecommender",
    goal=f"Recommend a movie based on genre '{genre}' and mood '{mood}'.",
    backstory="A movie enthusiast that can suggest movies based on various genres and moods."
)

movie_summary = Agent(
    role="MovieSummaryAgent",
    goal=f"Provide a summary of a movie recommended in the genre '{genre}' and mood '{mood}'.",
    backstory="A movie critic skilled at summarizing plot details, director, and cast information."
)

activity_suggester = Agent(
    role="ActivitySuggestionAgent",
    goal="Suggest activities related to watching a movie, like discussion topics, fan clubs, or movie trivia.",
    backstory="An entertainment expert who can suggest engaging activities related to movies."
)

# --- Define Tasks ---
task1 = Task(
    description=f"Recommend a movie based on the user's genre '{genre}' and mood '{mood}'.",
    expected_output="A list of movie recommendations.",
    agent=movie_recommender
)

task2 = Task(
    description="Provide a detailed summary of the recommended movie including plot, director, and cast.",
    expected_output="A short summary of the movie with plot and main details.",
    agent=movie_summary
)

task3 = Task(
    description="Suggest fun activities related to the movie like discussion topics or fan clubs.",
    expected_output="List of engaging activities related to the movie.",
    agent=activity_suggester
)

# --- Define Functions for OpenRouter Interaction ---
def openrouter_response(prompt):
    url = "https://api.openrouter.ai/v1/completion"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",  # Example model; you can choose other models if preferred
        "prompt": prompt,
        "max_tokens": 150
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json().get('text', 'Sorry, I couldn’t understand that.')
    else:
        return "Sorry, something went wrong with the request."

# --- Create and Run the Crew ---
crew = Crew(
    agents=[movie_recommender, movie_summary, activity_suggester],
    tasks=[task1, task2, task3],
    verbose=True  # To see the steps of execution
)

# Run the crew and get the results
result = crew.kickoff()

# Output the final result after all agents have completed their tasks
print("\n--- Final Output ---\n")
print(result)
