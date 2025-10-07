from fastapi import FastAPI

#instance
app= FastAPI()

#creating root endpoint
@app.get("/")
def read_root():
    return {"Meassage: Welcome to Fast API demo!"}

#path parameters
@app.get("/students/{student_id}")
def get_student(student_id: int):
    return{"student_id": student_id, "name": "Rahul", "course": "AI"}