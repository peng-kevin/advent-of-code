import collections
from types import MappingProxyType

def printgrid(grid):
    minx = 0
    miny = 0
    maxx = 0
    maxy = 0
    for x, y in grid:
        if x < minx:
            minx = x
        elif x > maxx:
            maxx = x
        if y < miny:
            miny = y
        elif y > maxy:
            maxy = y
    board = []
    for i in range(maxy + 1 - miny):
        board.append([False] * (maxx + 1 - minx))
    for x, y in grid:
        board[y - miny][x - minx] = True
    for row in board:
        for c in row:
            if c:
                print("*", end="")
            else:
                print(" ", end="")
        print("")

inputf = "input.txt"
with open(inputf) as f:
    lines = f.readlines()
grid = collections.defaultdict(lambda: False)
folds = []
for l in lines:
    if l == "\n":
        continue
    if l.split()[0] == "fold":
        f = l.strip().split()[2].split("=")
        f = (f[0], int(f[1]))
        folds.append(f)
    else:
        coord = l.strip().split(",")
        coord = (int(coord[0]), int(coord[1]))
        grid[coord] = True
for fold in folds:
    axis = fold[0]
    val = fold[1]
    newgrid = collections.defaultdict(lambda: False)
    for coord in grid:
        if val:
            if axis == "x" and val < coord[0]:
                newgrid[(2 * val - coord[0], coord[1])] = True
            elif axis == "y" and val < coord[1]:
                newgrid[(coord[0], 2 * val - coord[1])] = True
            else:
                newgrid[coord] = True
    grid = newgrid
printgrid(grid)


