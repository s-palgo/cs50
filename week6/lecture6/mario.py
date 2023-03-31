def main():
    height = get_height()
    for i in range(height):
        print("#")

def get_height():
    # There is no built-in do-while loop in Python.
    # In order to implement the logic of a do while loop, here's what has to be done:
    while True:
        try:
            n = int(input("Height: "))
            if n > 0:
                break
        except ValueError:
            print("That's not an integer! ")
    return n

main()