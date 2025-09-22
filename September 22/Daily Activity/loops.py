# for i in range(1,6):
#     print(i)

def multiplication_table(num):
    print(f"multiplication table of {num}")
    for i in range(1, 11):
        print(f"{num} X {i} = {num*i}")

number = int(input("Enter a number: "))
multiplication_table(number)
