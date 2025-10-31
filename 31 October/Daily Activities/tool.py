# tool.py
from langchain_openai import ChatOpenAI

def improve_text(text: str, llm: ChatOpenAI) -> str:
    """Improves the clarity or professionalism of the text."""
    prompt = f"Rewrite the following text to make it clearer and more professional: '{text}'"
    try:
        response = llm.invoke(prompt)
        return f"Suggested rewrite: {response.content.strip()}"
    except Exception as e:
        return f"Could not improve the text: {e}"
