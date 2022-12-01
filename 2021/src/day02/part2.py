import re
with open("input.txt") as f:
  lines = [x.split() for x in f.readlines()]
lines = [[a, int(b)] for a, b in lines]

h = 0
d = 0
aim = 0
for l in lines:
  if(l[0] == 'forward'):
    h += l[1]
    d += aim * l[1]
  if(l[0] == 'up'):
    aim -= l[1]
  if(l[0] == 'down'):
    aim += l[1]
print(h * d)