import re
import math


match = {'(':')', '{':'}', '[':']', '<':'>'}
value = {')':1, ']':2, '}':3, '>':4}
inputf = "input.txt"
correct = []
with open(inputf) as f:
  lines = f.readlines()
total = []
for l in lines:
  stack = []
  valid = True
  score = 0
  for c in l:
    if c in match.keys():
      stack.append(c)
    if c in match.values():
      if len(stack) == 0 or match[stack.pop()] != c:
        valid = False
        break
  if valid:
    stack.reverse()
    for s in stack:
      score = score * 5 + value[match[s]]
    total.append(score)
total.sort()
print(total[len(total)//2])
