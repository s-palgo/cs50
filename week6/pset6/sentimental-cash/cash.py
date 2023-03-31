from cs50 import get_float

# TODO
change = get_float("Change owed: ")

while True:
    if change < 0:
        change = get_float("Change owed: ")
    else:
        break

coins = 0

while round(change, 2) > 0.24:
    change = change - 0.25
    coins += 1

while round(change, 2) > 0.09:
    change = change - 0.1
    coins += 1

while round(change, 2) > 0.04:
    change = change - 0.05
    coins += 1

while round(change, 2) > 0:
    change = change - 0.01
    coins += 1

print(coins)