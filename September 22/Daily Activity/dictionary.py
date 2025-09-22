student={
    "name":"Sneha",
    "age":22,
    "course":"AIML",
    "skills": ["Python","c++", "Sql"]
}
#2 methods to access value
print(student["name"])
print(student.get("age"))

student["grade"]= "A"   #adding
student["age"]= 25      #updating

print(student)

student.pop("course")    #remove by key
del student["grade"]     #delete key
print(student)

#loop for dictionary
for key,value in student.items():
    print(key, ":", value)

#nesting
print(student["skills"][1]) #access nested data