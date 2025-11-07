# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, json
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
from typing import List

load_dotenv()  # ensure OPENAI_API_KEY is in .env or env vars

app = FastAPI()

# Allow browser JS (dev). In production restrict origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HISTORY_FILE = "history.json"

class Prompt(BaseModel):
    query: str

def ensure_history_file():
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f)

def load_history() -> List[dict]:
    ensure_history_file()
    with open(HISTORY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_history_entry(question: str, answer: str):
    data = load_history()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer
    }
    data.append(entry)
    # Optionally limit history length (uncomment next two lines)
    # MAX = 500
    # data = data[-MAX:]
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.post("/generate")
async def generate_response(prompt: Prompt):
    # Validation: empty or whitespace -> 404
    if not prompt.query or prompt.query.strip() == "":
        raise HTTPException(
            status_code=404,
            detail="Query cannot be empty. Please provide a valid topic or question."
        )

    try:
        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-4-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt.query}
            ]
        )

        # Extract answer (safely)
        answer = ""
        try:
            answer = response.choices[0].message.content
        except Exception:
            answer = str(response)

        # Save to history
        save_history_entry(prompt.query, answer)

        return {"response": answer}

    except HTTPException:
        raise
    except Exception as e:
        # Return 500 so frontend can show error
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history():
    return load_history()
