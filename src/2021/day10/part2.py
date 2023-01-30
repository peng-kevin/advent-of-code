#!/usr/bin/env python3
import sys
import re
import math

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} input_file', file=sys.stderr)
    exit(1)

  filename = sys.argv[1]
  match = {'(':')', '{':'}', '[':']', '<':'>'}
  value = {')':1, ']':2, '}':3, '>':4}
  correct = []
  with open(filename) as f:
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
