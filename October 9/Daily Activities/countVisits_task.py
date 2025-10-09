from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
import traceback

app = FastAPI()

# Global visit counter
visit_count = 0

# ---------------- Middleware to count visits ----------------
@app.middleware("http")
async def count_visits(request: Request, call_next):
    global visit_count
    visit_count += 1
    current_count = visit_count
    print(f"Visit number: {current_count}")
    response = await call_next(request)
    return response

# ---------------- Sample students data ----------------
students = [
    {"id": 1, "name": "Rahul"},
    {"id": 2, "name": "Neha"}
]

# ---------------- Routes ----------------
@app.get("/students")
def get_students():
    return students

@app.get("/visits")
def get_visit_count():
    return {"total_visits": visit_count}
