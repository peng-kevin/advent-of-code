#!/usr/bin/env python3
import re
import sys

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} input_file', file=sys.stderr)
    exit(1)

  filename = sys.argv[1]
  with open(filename) as f:
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
