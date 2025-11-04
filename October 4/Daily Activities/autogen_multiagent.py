import os
from dotenv import load_dotenv
import wikipediaapi
from autogen import AssistantAgent

# Load environment variables from .env file
load_dotenv()

# Fetch API key and base URL from environment variables
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

# Configuration for the LLM (Large Language Model)
llm_config = {
    "model": "meta-llama/llama-3-8b-instruct",  # Example LLM model
    "api_key": api_key,
    "base_url": base_url,
    "temperature": 0.7,
    "max_tokens": 500,
}

# Initialize AssistantAgents for different roles
researcher = AssistantAgent(
    name="Researcher",
    llm_config=llm_config,
    system_message="You are a research expert. Your job is to find and summarize useful information about any given topic in bullet points."
)

writer = AssistantAgent(
    name="Writer",
    llm_config=llm_config,
    system_message="You are a professional content writer. You will take research summaries and write a clear, engaging 3-paragraph report."
)

reviewer = AssistantAgent(
    name="Reviewer",
    llm_config=llm_config,
    system_message="You are an editor and critic. Your job is to review the writer's report, check for clarity, grammar, and completeness, and suggest improvements."
)


# Function to get Wikipedia content for a given topic
def get_wikipedia_content(topic: str) -> str:
    """
    Fetches content from Wikipedia for the given topic using the wikipedia-api library.
    """
    # Specify the user_agent directly in the constructor
    wiki = wikipediaapi.Wikipedia(language='en', user_agent='MyWikipediaBot/1.0 (me.eskay1@gmail.com)')

    page = wiki.page(topic)

    if page.exists():
        return page.text  # Return full text of the Wikipedia page
    else:
        return f"Sorry, no information found for '{topic}'."


# Example topic
topic = "Impact of Artificial Intelligence on Education"

# Step 1: Fetch research from Wikipedia
research_content = get_wikipedia_content(topic)
print("\nWikipedia Research Content:\n", research_content, "\n")

# Step 2: Researcher Agent summarizes the Wikipedia content
research_summary = researcher.generate_reply(
    messages=[{"role": "user",
               "content": f"Please research the topic: {topic}. Here is some information:\n{research_content}"}]
)
print("\nResearch Summary:\n", research_summary, "\n")

# Step 3: Writer Agent drafts a report based on the research summary
report_draft = writer.generate_reply(
    messages=[{"role": "user", "content": f"Write a report based on this research summary:\n{research_summary}"}]
)
print("Draft Report:\n", report_draft, "\n")

# Step 4: Reviewer Agent reviews and improves the draft report
reviewed_report = reviewer.generate_reply(
    messages=[{"role": "user", "content": f"Please review and improve this report:\n{report_draft}"}]
)
print("Final Reviewed Report:\n", reviewed_report)
