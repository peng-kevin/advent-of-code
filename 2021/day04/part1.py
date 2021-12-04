import re

inputf = "input.txt"

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

boards = []
with open(inputf) as f:
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
