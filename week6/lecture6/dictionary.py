# Reimplementing pset5


# define a hash table (using a set, which is a hash table in Python that takes care of duplicates)
words = set()

# define a function called check
def check(word):
    if word.lower() in words:
        return True
    else:
        return False

def load(dictionary):
    file = open(dictionary, "r")
    for line in file:
        # rstrip strips off the \n character at the end of the line
        word = line.rstrip()
        words.add(word)
    file.close()
    return True

def size():
    return len(words)

def unload():
    return True