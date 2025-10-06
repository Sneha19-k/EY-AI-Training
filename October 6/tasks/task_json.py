import json
import logging

logging.basicConfig(
    filename= 'app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initial list of students
students = [
    {
        "name": "Rahul",
        "age": 21,
        "course": "AI",
        "marks": 85
    },
    {
        "name": "Priya",
        "age": 22,
        "course": "ML",
        "marks": 90
    }
]

# Write to JSON file
with open("student.json", 'w') as f:
    json.dump(students, f, indent=4)

# Read from JSON file
with open("student.json", 'r') as f:
    data = json.load(f)

# Print all student names
print("Student Names:")
for student in data:
    print(student["name"])

# Add a new student
new_student = {
    "name": "Arjun",
    "age": 20,
    "course": ["Data Science"],
    "marks": {"Data science": 78}
}

data.append(new_student)
logging.info("New student added.")


# Write updated data back to JSON
with open("student.json", 'w') as f:
    json.dump(data, f, indent=4)
logging.info("new updated file saved successfully.")

# Confirm and print updated list

print("Updated Student Names:")
for student in data:
    print(student["name"])

