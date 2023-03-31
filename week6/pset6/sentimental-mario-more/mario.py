from cs50 import get_int

# TODO
height = get_int("Height: ")

while True:
    if height < 1 or height > 8:
        height = get_int("Height: ")
    else:
        break

for i in range(height):
    for j in range(height - i - 1):
        print(" ", end="")
    for j in range(i + 1):
        print("#", end="")
    print("  ", end="")
    for j in range(i):
        print("#", end="")
    print("#")