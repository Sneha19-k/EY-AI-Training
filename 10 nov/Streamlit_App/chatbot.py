from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from simpleeval import simple_eval
import os
import re

load_dotenv()

app = FastAPI()

# Allow fetch() from browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Initialize LangChain with OpenRouter
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

class Prompt(BaseModel):
    query: str

@app.post("/generate")
async def generate_response(prompt: Prompt):
    query = prompt.query.strip()

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # ✅ Reverse the word logic
    match_reverse = re.match(r"reverse the word (\w+)", query, re.IGNORECASE)
    if match_reverse:
        word = match_reverse.group(1)
        return {"response": word[::-1]}

    # ✅ Try math expression safely
    try:
        # Keep only valid math characters
        safe_query = re.sub(r'[^0-9\+\-\*/\.\(\)\s]', '', query)
        result = simple_eval(safe_query)
        return {"response": result}
    except:
        pass  # If math fails, continue to AI

    # ✅ Otherwise send to LLM normally
    try:
        result = llm.invoke(query)
        return {"response": result.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenRouter Error: {str(e)}")
