#!/usr/bin/env python3
import sys
from queue import PriorityQueue

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} input_file', file=sys.stderr)
        exit(1)

    filename = sys.argv[1]
    with open(filename) as f:
        grid = [[int(c) for c in row.strip()] for row in f.readlines()]
    frontier = PriorityQueue()
    height = len(grid)
    width = len(grid[0])
    factor = 5
    frontier.put((0, (0, 0)))
    cost_so_far = {}
    cost_so_far[(0, 0)] = 0

    while frontier:
        current = frontier.get()[1]
        if current == (height * factor - 1, width * factor - 1):
            break
        current_cost = cost_so_far[current]
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny = current[0] + dy
            nx = current[1] + dx
            if ny < 0 or ny >= height * factor or nx < 0 or nx >= width * factor:
                continue
            right_shift = nx // width
            down_shift = ny // height
            grid_cost = (grid[ny % height][nx % width] + right_shift + down_shift - 1) % 9 + 1
            new_cost = current_cost + grid_cost
            if (ny, nx) not in cost_so_far or new_cost < cost_so_far[(ny, nx)]:
                cost_so_far[(ny, nx)] = new_cost
                frontier.put((new_cost, (ny, nx)))

    print(cost_so_far[(height * factor - 1, width * factor - 1)])
