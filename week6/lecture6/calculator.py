# using input() which turns the numbers into strings
x = input("x: ")
y = input("y: ")
print(x + y)

# using try + exception to use input() to get the numbers as an int data type
try:
    x = int(input("x: "))
except:
    print("That is not an int!")
    exit()

try:
    y = int(input("y: "))
except:
    print("That is not an int!")
    exit()

print(x + y)



