from cs50 import get_string

# TODO
text = get_string("Text: ")

letters = 0
words = 0
sentences = 0

for char in text:
    if char == ' ':
        words += 1
    elif char == '.' or char == '!' or char == '?':
        sentences += 1
    elif char.isalpha():
        letters += 1
    else:
        continue

words += 1

L = 100 * letters / words
S = 100 * sentences / words
index = 0.0588 * L - 0.296 * S - 15.8
level = round(index)

if level >= 1 and level < 16:
    print(f"Grade {level}")
elif level < 1:
    print("Before Grade 1")
else:
    print("Grade 16+")