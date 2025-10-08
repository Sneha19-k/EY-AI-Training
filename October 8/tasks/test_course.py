import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


#----------task 1-------------
def test_create_course_success():
    new_course = {
        "id": 2,
        "title": "Advanced Python",
        "duration": 40,
        "fee": 4000,
        "is_active": True
    }
    response = client.post("/courses", json=new_course)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == new_course["id"]
    assert data["title"] == new_course["title"]

def test_create_course_duplicate_id():
    duplicate_course = {
        "id": 1,  # Existing course ID
        "title": "Python Basics Duplicate",
        "duration": 30,
        "fee": 3000,
        "is_active": True
    }
    response = client.post("/courses", json=duplicate_course)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Course ID already exists"

#----task 2-----

@pytest.mark.parametrize("duplicate_id", [1, 2])
def test_create_course_duplicate_id(duplicate_id):
    duplicate_course = {
        "id": duplicate_id,
        "title": f"Duplicate Course {duplicate_id}",
        "duration": 30,
        "fee": 3000,
        "is_active": True
    }
    response = client.post("/courses", json=duplicate_course)
    assert response.status_code == 400
    assert response.json()["detail"] == "Course ID already exists"


