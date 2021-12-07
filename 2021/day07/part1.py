import re
import math

inputf = "input.txt"
with open(inputf) as f:
    pos = [int(x) for x in f.read().split(",")]

a = min(pos)
b = max(pos)
best = a
cost = math.inf
for i in range(a, b + 1):
    c = 0
    for p in pos:
        c = c + abs(p - i)
    if c < cost:
        cost = c
        best = i
print(best)
print(cost)