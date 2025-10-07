from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

#instance
app= FastAPI()

#pydantic model for validation
class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: int

# in memory database
employees =[
    {"id": 1, "name": "Rahul", "department": "Consulting", "salary": 840000},
    {"id": 2, "name": "Priya", "department": "Tax", "salary": 900000},
    {"id": 3, "name": "Riya", "department": "Audit", "salary": 700000},
]

#bonus_task
@app.get("/employees/count")
def count_employees():
    return {"no. of employees" : len(employees)}

@app.get("/employees")
def get_all_employee():
    return{"Employees" : employees}

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    for e in employees:
        if e["id"] ==employee_id:
            return e
    raise HTTPException(status_code=404, detail="Employee not found")

#-----------post--------------
@app.post("/employees", status_code=201)
def add_employees(employee: Employee):
    for e in employees:
        if e["id"] == employee.id:
            raise HTTPException(status_code=400, detail=f"Employee with ID {employee.id} already exists.")

    employees.append(employee.dict())
    return {"message": "Employee added successfully", "employees": employees}

#--------------PUT-----------------------
@app.put("/employees/{employee_id}")
def update_employee(employee_id : int, updated_employee: Employee ):
    for i, e in enumerate(employees):
        if e["id"]== employee_id:
            employees[i] = updated_employee.dict()
            return {"message": "employee updated successfully", "employee": updated_employee}
    raise HTTPException(status_code=404, detail="Employee not found")


#----------------------delete--------------
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    for i, e in enumerate(employees):
        if e["id"] == employee_id:
            deleted = employees.pop(i)
            return {"message": "Employee deleted successfully", "employee": deleted}
    raise HTTPException(status_code=404, detail="Employee not found")