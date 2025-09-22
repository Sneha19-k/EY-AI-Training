from enum import unique

names= {"Rahul", "kedia", "Priya", "Rahul"}
print(names)

#check presence of data
print("Sneha" in names)      # false
print("Rahul" in names)      # true

set_a={"Sneha", "Rahul"}
set_b={"Rahul", "Priya", "Rama"}
print(set_a | set_b)   #union
print(set_a & set_b)   #intersection
print(set_a - set_b)   #difference

#pass the list to a set
student= ["Rahul", "kedia", "Priya", "Rahul"]
unique_set= set(student)
print(unique_set)