#!/usr/bin/env python3
import re
import sys

class Board:
  def __init__(self, grid):
    self.grid = grid

  def isWin(self):
    for row in self.grid:
      if sum(row) == -5:
        return True
    col_t = [sum(x) for x in zip(*self.grid)]
    for c in col_t:
      if c == -5:
        return True
    return False

  def mark(self, val):
    self.grid = [[-1 if x == val else x for x in row] for row in self.grid]

  def score(self):
    scoregrid = [[0 if x == -1 else x for x in row] for row in self.grid]
    return sum(sum(scoregrid, []))

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} input_file', file=sys.stderr)
    exit(1)

  filename = sys.argv[1]
  boards = []
  with open(filename) as f:
    draws = [int(x) for x in f.readline().split(",")]
    boards_str = f.read().split("\n\n")
    for b in boards_str:
      rows = b.split("\n")
      grid = []
      for r in rows:
        grid.append([int(x) for x in r.split()])
      boards.append(Board(grid))

  for d in draws:
    for b in boards:
      b.mark(d)
      if(b.isWin()):
        print("winner:")
        print(b.score() * d)
        exit()
