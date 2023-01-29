import re
import math


match = {'(':')', '{':'}', '[':']', '<':'>'}
value = {')':3, ']':57, '}':1197, '>':25137}
inputf = "input.txt"
with open(inputf) as f:
  lines = f.readlines()
total = 0
for l in lines:
  stack = []
  for c in l:
    if c in match.keys():
      stack.append(c)
    if c in match.values():
      if len(stack) == 0 or match[stack.pop()] != c:
        total += value[c]
        break
print(total)