from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, json
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

load_dotenv()
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HISTORY_FILE = "history.json"

class Prompt(BaseModel):
    query: str

def save_history(question: str, answer: str):
    # Check if file exists; if not, create with an empty list
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f)

    # Load existing history
    with open(HISTORY_FILE, "r") as f:
        data = json.load(f)

    # Append new QnA
    entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer
    }
    data.append(entry)

    # Save back to file
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.post("/generate")
async def generate_response(prompt: Prompt):
    # ✅ Validation
    if not prompt.query or prompt.query.strip() == "":
        raise HTTPException(
            status_code=404,
            detail="Query cannot be empty. Please provide a valid topic or question."
        )

    try:
        # Call GPT model
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt.query}
            ]
        )

        answer = response.choices[0].message.content

        # History saved to history.json
        save_history(prompt.query, answer)
        print("History saved to history.json")

        return {"response": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
