from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

#instance
app= FastAPI()

#pydantic model for validation
class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str

# in memory database
students =[
    {"id":1, "name": "Rahul", "age": 21, "course": "AI"},
    {"id": 2, "name": "Priya", "age": 22, "course": "ML"},
]
#-----------------GET-------------
@app.get("/students")
def get_all_students():
    return{"Students" : students}

@app.get("/students/{student_id}")
def get_student(student_id: int):
    for s in students:
        if s["id"] == student_id:
            return s
    raise HTTPException(status_code=404, detail="Student not found")

#-----------POST--------------------
@app.post("/students", status_code=201)
def add_student(student: Student):
    students.append(student.dict())
    return {"message": "student added successfully", "students": students}

#--------------PUT-----------------------
@app.put("/students/{student_id}")
def update_student(student_id : int, updated_student: Student ):
    for i, s in enumerate(students):
        if s["id"]== student_id:
            students[i] = updated_student.dict()
            return {"message": "student updated successfully", "student": updated_student}
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for i, s in enumerate(students):
        if s["id"] == student_id:
            deleted_student = students.pop(i)
            return {"message": "Student deleted successfully", "student": deleted_student}
    raise HTTPException(status_code=404, detail="Student not found")

