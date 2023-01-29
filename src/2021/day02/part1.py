import re
with open("input.txt") as f:
  lines = [x.split() for x in f.readlines()]
lines = [[a, int(b)] for a, b in lines]

h = 0
v = 0
for l in lines:
  if(l[0] == 'forward'):
    h += l[1]
  if(l[0] == 'up'):
    v -= l[1]
  if(l[0] == 'down'):
    v += l[1]
print(h * v)