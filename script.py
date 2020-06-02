import os

exCodes = []
filepath1 = os.path.abspath("") + "\\html\\exCodes.txt"
g = open(filepath1, "w")

filepath = os.path.abspath("") + "\\exCode_list.txt"
with open(filepath, encoding = "UTF-8") as f:
    for line in f.readlines():
        key = 0
        for index in range(1, len(line)):
            if line[index] == '(':
                key = index
                break
        code = line[key + 1 : -1]
        g.write(code)
f.close()
g.close()

    