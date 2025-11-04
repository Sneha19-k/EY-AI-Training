import os
import json
from dotenv import load_dotenv
import requests
import wikipediaapi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ----------------------------------------------------------
# 1. Load environment variables
# ----------------------------------------------------------
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

# ----------------------------------------------------------
# 2. Initialize Mistral Model (via OpenRouter)
# ----------------------------------------------------------

class MistralModel:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def generate(self, prompt: str):
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 256,
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content'].strip()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

# Initialize Mistral model instance
mistral_model = MistralModel(api_key=api_key, base_url=base_url)

# ----------------------------------------------------------
# 3. Define the Researcher Agent (Fetching from Wikipedia using wikipedia-api)
# ----------------------------------------------------------

def researcher_agent(query: str):
    """
    This function uses wikipedia-api to fetch information from Wikipedia.
    """
    print("Researching...")
    wiki = wikipediaapi.Wikipedia(language='en', user_agent='MyWikipediaBot/1.0 (me.eskay1@gmail.com)')
    page = wiki.page(query)

    if page.exists():
        return page.text
    else:
        return f"Sorry, no information found for '{query}'."

# ----------------------------------------------------------
# 4. Define the Summarizer Agent (Using Mistral via OpenRouter)
# ----------------------------------------------------------

# Define ChatPromptTemplate for summarization
summarization_prompt = ChatPromptTemplate.from_template(
    "<s>[INST] You are a concise assistant. Summarize the following information in simple terms: {information} [/INST]"
)

parser = StrOutputParser()

def summarizer_agent(information: str):
    """
    This function formats the research into a prompt for the Mistral model
    and then generates a summary.
    """
    prompt = summarization_prompt.format(information=information)
    print("Summarizing the research...")
    return mistral_model.generate(prompt)

# ----------------------------------------------------------
# 5. Define the Notifier Agent (Output to Console or File)
# ----------------------------------------------------------

def notifier_agent(summary: str, output_to_file: bool = False):
    """
    This function prints the summary to the console or writes it to a file.
    """

    if output_to_file:
        os.makedirs(name="logs", exist_ok=True)
        log_entry = {
            "summary": summary
        }
        with open("logs/summary_output.jsonl", "a", encoding="utf-8") as file:
            file.write(json.dumps(log_entry) + "\n")
        print("Summary has been written to 'logs/summary_output.jsonl'.")
    else:
        print("Summary Notification:")
        print(summary)

# ----------------------------------------------------------
# 6. Combine the Agents into a Multi-Agent System
# ----------------------------------------------------------

def multi_agent_system(query: str, output_to_file: bool = False):
    """
    Runs the multi-agent system:
    - Researches the topic
    - Summarizes the research using Mistral
    - Notifies the user (prints to console or writes to file)
    """
    # Step 1: Research the topic
    research = researcher_agent(query)
    print("Research complete.\n")

    # Step 2: Summarize the research using Mistral
    summary = summarizer_agent(research)
    print("Summary complete.\n")

    # Step 3: Notify the user
    notifier_agent(summary, output_to_file)

# ----------------------------------------------------------
# 7. Run the System
# ----------------------------------------------------------

if __name__ == "__main__":
    # Example usage:
    user_topic = input("Enter a topic you want explained: ").strip()
    multi_agent_system(user_topic, output_to_file=True)  # Set to True to write to a file, False for console output
