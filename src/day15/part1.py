from queue import PriorityQueue

inputf = "input.txt"
with open(inputf) as f:
    grid = [[int(c) for c in row.strip()] for row in f.readlines()]
frontier = PriorityQueue()
height = len(grid)
width = len(grid[0])
frontier.put((0, (0, 0)))
cost_so_far = {}
cost_so_far[(0, 0)] = 0

while frontier:
    current = frontier.get()[1]
    if current == (height - 1, width - 1):
        break
    current_cost = cost_so_far[current]
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny = current[0] + dy
        nx = current[1] + dx
        if ny < 0 or ny >= height or nx < 0 or nx >= width:
            continue
        new_cost = current_cost + grid[ny][nx]
        if (ny, nx) not in cost_so_far or new_cost < cost_so_far[(ny, nx)]:
            cost_so_far[(ny, nx)] = new_cost
            frontier.put((new_cost, (ny, nx)))

print(cost_so_far[(height - 1, width - 1)])