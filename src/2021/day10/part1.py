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
  value = {')':3, ']':57, '}':1197, '>':25137}
  with open(filename) as f:
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
