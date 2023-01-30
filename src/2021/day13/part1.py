#!/usr/bin/env python3
import sys
import collections

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} input_file', file=sys.stderr)
        exit(1)

    filename = sys.argv[1]
    with open(filename) as f:
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
    axis = folds[0][0]
    val = folds[0][1]
    newgrid = collections.defaultdict(lambda: False)
    for coord in grid:
        if val:
            if axis == "x" and val > coord[0]:
                newgrid[(2 * val - coord[0], coord[1])] = True
            elif axis == "y" and val < coord[1]:
                newgrid[(coord[0], coord[1] - 2 * val)] = True
            else:
                newgrid[coord] = grid[coord]
    print(len(newgrid))

