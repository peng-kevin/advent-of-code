#!/usr/bin/env python3
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} input_file', file=sys.stderr)
        exit(1)

    filename = sys.argv[1]
    with open(filename) as f:
        grid = [list(r) for r in f.readlines()]
    grid = [[int(p) for p in r if p.isnumeric()] for r in grid]
    adj = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    total = 0
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
                total += c + 1
    print(total)
