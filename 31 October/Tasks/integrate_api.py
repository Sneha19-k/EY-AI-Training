import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
import litellm
import requests

# ---------------------------------------------------------------------
# 1. Load environment variables
# ---------------------------------------------------------------------
load_dotenv()
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# ---------------------------------------------------------------------
# 2. Configure LiteLLM globally for OpenRouter
# ---------------------------------------------------------------------
litellm.api_key = os.getenv("OPENROUTER_API_KEY")
litellm.api_base = "https://openrouter.ai/api/v1"
model_name = "openrouter/mistralai/mistral-7b-instruct"


# ---------------------------------------------------------------------
# 3. Define Helper Functions for Weather Data
# ---------------------------------------------------------------------
def get_weather_data(city: str):
    """Fetch weather data from OpenWeatherMap API."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        }
        return weather_info
    else:
        return {"error": "Unable to fetch weather data."}


# ---------------------------------------------------------------------
# 4. Define Agents
# ---------------------------------------------------------------------
# Weather Agent to ask for region and get data
weather_agent = Agent(
    role="WeatherAgent",
    goal="Ask the user for a region (city) and fetch the weather data.",
    backstory="An AI assistant that fetches current weather data for a given city.",
    allow_delegation=True,
    llm=model_name,
)

planner = Agent(
    role="Planner",
    goal="Create a structured 3-step plan with goals and deliverables.",
    backstory="A strategic AI project planner who designs clear blueprints.",
    allow_delegation=True,
    llm=model_name,
)

specialist = Agent(
    role="Specialist",
    goal="Execute the Planner’s 3-step plan and summarize the results clearly.",
    backstory="A detail-oriented AI engineer capable of executing complex plans.",
    llm=model_name,
)

# ---------------------------------------------------------------------
# 5. Define Tasks
# ---------------------------------------------------------------------
weather_task = Task(
    description="Ask for a region (city) and fetch weather data for that region. If not provided, use Dubai by default.",
    expected_output="Weather data for the requested city, or default to Dubai.",
    agent=weather_agent,
)

plan_task = Task(
    description="Given the topic, create a 3-step plan with goals and deliverables.",
    expected_output="A structured plan with 3 steps, each having a goal and deliverable.",
    agent=planner,
)

execute_task = Task(
    description="Take the Planner’s 3-step plan and write a short summary of what was achieved.",
    expected_output="A 3-point summary explaining the outcomes for each step in less than 10 words each.",
    agent=specialist,
)


# ---------------------------------------------------------------------
# 6. Define Agent Logic for Weather Agent
# ---------------------------------------------------------------------
def weather_agent_logic(user_input: str):
    """Agent logic to ask for city name and fetch weather."""
    # Default city is Dubai
    city = "Dubai" if not user_input else user_input
    weather_info = get_weather_data(city)

    if "error" in weather_info:
        return f"Sorry, could not retrieve weather data for {city}."

    weather_report = (
        f"Weather for {weather_info['city']}:\n"
        f"Temperature: {weather_info['temperature']}°C\n"
        f"Description: {weather_info['description']}\n"
        f"Humidity: {weather_info['humidity']}%\n"
    )
    return weather_report


# ---------------------------------------------------------------------
# 7. Create and Run the Crew
# ---------------------------------------------------------------------
crew = Crew(
    agents=[weather_agent, planner, specialist],
    tasks=[weather_task, plan_task, execute_task],
    process=Process.sequential,
    verbose=True,
)

# ---------------------------------------------------------------------
# 8. Main Execution
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # Input for region or city
    region = input("Enter a region: ").strip()

    # Execute the workflow
    print("\n--- Running CrewAI Weather-Planning Workflow ---")
    weather_result = weather_agent_logic(region)
    print("\nWeather Information:\n", weather_result)

    topic = "Developing an AI-based document summarization system"
    print(f"\n--- Running CrewAI Planner–Specialist Workflow ---\nTopic: {topic}\n")
    crew_result = crew.kickoff(inputs={"topic": topic})

    # Output final results
    print("\n--- FINAL OUTPUT ---\n")
    print("Weather Report:\n", weather_result)
    print("Planner-Specialist Results:\n", crew_result)
