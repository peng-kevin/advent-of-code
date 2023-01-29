import re
with open("input.txt") as f:
  lines = [list(x) for x in f.readlines()]

gamma = ""
epsilon = ""
count = [0] * (len(lines[0]) - 1)
total = len(lines)
for l in lines:
  for i, c in enumerate(l):
    if(c == '1'):
      count[i] += 1
for c in count:
  if c > total/2:
    gamma += '1'
    epsilon += '0'
  else:
    gamma += '0'
    epsilon += '1'
print(count)
print(total)
print(gamma)
print(epsilon)