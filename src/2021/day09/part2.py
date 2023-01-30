#!/usr/bin/env python3
import math
import sys

class colors:
    RED = "\033[0;31m"
    YELLOW = "\033[0;33m"
    GREEN = "\033[0;32m"
    RESET = "\033[0m"

def printBasin(grid, basin):
    for r in range(len(grid)):
        output = ""
        for c in range(len(grid[r])):
            if (r, c) in basin:
                output += colors.GREEN + str(grid[r][c]) + colors.RESET + " "
            else:
                output += str(grid[r][c]) + " "
        print(output[:-1])


def inBasin(grid, row, col, basin):
    #print(f"check in basin {basin}")
    if grid[row][col] == 9:
        return False
    adj = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    for a in adj:
            nc = col + a[0]
            nr = row + a[1]
            if (nc >= 0 and nc < len(r) and nr >= 0 and nr < len(grid)):
                if grid[nr][nc] < grid[row][col]:
                    #print(f"down flow from {row}, {col} not in basin because {nr}, {nc}")
                    return True
    #print(f"down flow from {row}, {col} in basin")
    return False

def measureBasin(grid, row, col, basin):
    basin.append((row, col))
    adj = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    for a in adj:
            nc = col + a[0]
            nr = row + a[1]
            if (nc >= 0 and nc < len(r) and nr >= 0 and nr < len(grid)):
                if (nr, nc) not in basin and inBasin(grid, nr, nc, basin):
                    basin = measureBasin(grid, nr, nc, basin)
    return basin

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} input_file', file=sys.stderr)
        exit(1)

    filename = sys.argv[1]
    with open(filename) as f:
        grid = [list(r) for r in f.readlines()]
    grid = [[int(p) for p in r if p.isnumeric()] for r in grid]
    for r in grid:
        print(r)
    adj = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    basinSizes = []
    for i, r in enumerate(grid):
        for j, c in enumerate(r):
            lowPoint = True
            for a in adj:
                nc = j + a[0]
                nr = i + a[1]
                if (nc >= 0 and nc < len(r) and nr >= 0 and nr < len(grid) and grid[nr][nc] <= c):
                    lowPoint = False
                    break
            if lowPoint:
                basin = measureBasin(grid, i, j, [])
                printBasin(grid, basin)
                print(len(basin))
                basinSizes.append(len(basin))
                print("-----------")
    basinSizes.sort()
    print(basinSizes)
    print(math.prod(basinSizes[-3:]))
