from operator import truediv

from pydantic import BaseModel

#define a model (like a scheme)
class Student(BaseModel):
    name: str
    age: int
    email: str
    is_active: bool = True   #be def

#valid data
data={"name" : "Aisha", "age" : 21, "email" : "aisha@example.com"}
student= Student(**data)

print(student)
print(student.name)