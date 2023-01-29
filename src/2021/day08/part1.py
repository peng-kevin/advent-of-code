import re

inputf = "input.txt"
with open(inputf) as f:
    lines = f.readlines()
lines = [x.split("|") for x in lines]
total = 0
sum = 0
for l in lines:
    out = l[1].split()
    for o in out:
        if len(o) == 2 or len(o) == 4 or len(o) == 3 or len(o) == 7:
            sum = sum + 1
print(total)
print(sum)