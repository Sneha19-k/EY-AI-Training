from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float

# Sample in-memory "database"
employees = [
    {"id": 1, "name": "Amit Sharma", "department": "HR", "salary": 50000},
]

# GET all employees
@app.get("/employees")
def get_all():
    return employees

# POST a new employee
@app.post("/employees", status_code=201)
def add_employee(employee: Employee):
    employees.append(employee.dict())
    return employee

# GET employee by ID
@app.get("/employees/{emp_id}")
def get_employee(emp_id: int):
    for emp in employees:
        if emp["id"] == emp_id:
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, updated_employee: Employee):
    for i, e in enumerate(employees):
        if e["id"] == employee_id:
            updated_dict = updated_employee.model_dump()
            employees[i] = updated_dict
            return {
                "message": "employee updated successfully",
                "employee": updated_dict
            }
    raise HTTPException(status_code=404, detail="Employee not found")


#----------------------delete--------------
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    for i, e in enumerate(employees):
        if e["id"] == employee_id:
            deleted = employees.pop(i)
            return {"message": "Employee deleted successfully", "employee": deleted}
    raise HTTPException(status_code=404, detail="Employee not found")