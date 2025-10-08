from fastapi.testclient import TestClient
from main import app

client = TestClient(app)  #Arrange

# Arrange ACT Assert -- AAA Pattern
# CICD -- Cont Integration -- Cont Deployment -- checkin -- Build -- Test case -- Deployed to QA Server

# ---------------- TEST 1 ----------------
def test_get_all_employees():
    response = client.get("/employees")  # ACT
    assert response.status_code == 200  #Assert
    assert isinstance(response.json(), list)  #Assert

# ---------------- TEST 2 ----------------
def test_add_employee():
    new_emp = {
        "id": 2,
        "name": "Neha Verma",
        "department": "IT",
        "salary": 60000
    }
    response = client.post("/employees", json=new_emp)
    assert response.status_code == 201
    assert response.json()["name"] == "Neha Verma"

# ---------------- TEST 3 ----------------
def test_get_employee_by_id():
    response = client.get("/employees/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Amit Sharma"

# ---------------- TEST 4 ----------------
def test_get_employee_not_found():
    response = client.get("/employees/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"

#-------------------TEST 5------------------

def test_update_employee():
    updated_emp = {
        "id": 1,
        "name": "Amit Sharma",
        "department": "HR",
        "salary": 75000
    }
    response = client.put("/employees/1", json=updated_emp)
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "employee updated successfully"
    assert data["employee"]["department"] == "HR"
    assert data["employee"]["salary"] == 75000

def test_delete_employee():
    response = client.delete("/employees/1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Employee deleted successfully"
    assert data["employee"]["id"] == 1

def test_delete_employee_not_found():
    response = client.delete("/employees/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"
