#!/usr/bin/env python3
import re
import sys

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} input_file', file=sys.stderr)
    exit(1)

  filename = sys.argv[1]

  with open(filename) as f:
    lines = [re.findall("(\d+),(\d+) -> (\d+),(\d+)", x)[0] for x in f.readlines()]
  lines = [(int(x1), int(y1), int(x2), int(y2)) for x1, y1, x2, y2 in lines]
  overlaps = {}
  for x1, y1, x2, y2 in lines:
    x = x1
    y = y1
    while True:
      overlaps[(x, y)] = overlaps.setdefault((x, y), 0) + 1
      if(x == x2 and y == y2):
        break
      if x2 > x1:
        x += 1
      elif x2 < x1:
        x -= 1
      if y2 > y1:
        y += 1
      elif y2 < y1:
        y -= 1
        
  overlaps = {k:v for k, v in overlaps.items() if v > 1}
  print(len(overlaps))
