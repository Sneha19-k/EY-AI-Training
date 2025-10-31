# agents.py
from crewai import Agent, Task, Crew
from tool import improve_text
from langchain_openai import ChatOpenAI
from memory import memory

# Define the Text Improvement Agent
def text_improvement_agent(user_input: str, llm: ChatOpenAI):
    """Handles text improvement requests."""
    return improve_text(user_input, llm)

# Define the Sentiment Analysis Agent
def sentiment_analysis_agent(improved_text: str, llm: ChatOpenAI):
    """Analyzes the sentiment of the improved text."""
    prompt = f"Analyze the sentiment of the following text: '{improved_text}'"
    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return f"Sentiment analysis failed: {e}"

# Create CrewAI agents and tasks for chaining
def create_agents_and_tasks(llm: ChatOpenAI):
    # Agent 1: Text Improvement
    text_improvement = Agent(
        role="TextImprovementAgent",
        goal="Improve the clarity and professionalism of the user input.",
        backstory="A text improvement expert that refines and enhances text.",
        task=Task(
            description="Improve the user-provided text",
            agent_fn=lambda user_input: text_improvement_agent(user_input, llm)
        )
    )

    # Agent 2: Sentiment Analysis
    sentiment_analysis = Agent(
        role="SentimentAnalysisAgent",
        goal="Analyze the sentiment of the improved text.",
        backstory="A sentiment analysis expert that evaluates the tone of text.",
        task=Task(
            description="Analyze the sentiment of the improved text",
            agent_fn=lambda improved_text: sentiment_analysis_agent(improved_text, llm)
        )
    )

    # Define the Crew (task orchestration)
    crew = Crew(
        agents=[text_improvement, sentiment_analysis],
        verbose=True
    )

    return crew
