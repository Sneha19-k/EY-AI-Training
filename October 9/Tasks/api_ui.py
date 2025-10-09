from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
def serve_html():
    html_path = os.path.join(BASE_DIR, "students.html")
    return FileResponse(html_path)

# Dummy student data
students = [
    {"id": 1, "name": "Rahul", "age": 20},
    {"id": 2, "name": "Priya", "age": 21},
    {"id": 3, "name": "Riya", "age": 22},
    {"id": 4, "name": "Rama", "age": 23},
    {"id": 5, "name": "Shyam", "age": 24}
]

@app.get("/students")
def get_students():
    return {"students": students}
