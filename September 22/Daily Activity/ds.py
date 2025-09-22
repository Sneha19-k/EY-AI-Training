#list
numbers= [50,40,30,20,10]

print(numbers[0]) #first element
print(numbers[-1]) #last element

numbers.append(80)
numbers.insert(2,45)
#remove
numbers.remove(50)
numbers.pop()
print(numbers)

#-------------------------------tuple------------

colours= ("red", "green", "blue")
print(colours[0])
print(colours[1])

# print(colours[0]= "pink") #immutable

#--------------------------------dictionary-------------
student={
    "name":"Sneha",
    "age":22,
    "city": "Kol"
}
print(student["name"])
print(student.get("age"))
