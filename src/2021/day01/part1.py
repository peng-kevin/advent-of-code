#!/usr/bin/env python3
import sys

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} input_file', file=sys.stderr)
    exit(1)

  filename = sys.argv[1]
  with open(filename) as f:
    lines = [int(x) for x in f.readlines()];
  prev = lines[0]
  sum = 0
  for l in lines[1:]:
    if l > prev:
      sum += 1
    prev = l
  print(sum)

