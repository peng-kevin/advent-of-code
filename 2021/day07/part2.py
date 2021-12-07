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
        d = abs(p - i)
        if d > 0:
            c = c + d * (d + 1)/2
    if c < cost:
        cost = c
        best = i
print(best)
print(cost)