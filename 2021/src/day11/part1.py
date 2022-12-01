inputf = "input.txt"
with open(inputf) as f:
    grid = f.readlines()
grid = [[int(c) for c in row if c.isnumeric()] for row in grid]

def printGrid(grid):
    for r in grid:
        print(r)

def getNeighbors(grid, row, col):
    ncells = [(nrow, ncol) for nrow in (row - 1, row, row + 1) for ncol in (col - 1, col, col + 1) if nrow != row or ncol != col]
    ncells = [(nrow, ncol) for nrow, ncol in ncells if nrow >= 0 and nrow < len(grid) and ncol >= 0 and ncol < len(grid[nrow])]
    return ncells

flashCount = 0
for i in range(100):
    stack = [(row, col) for row in range(len(grid)) for col in range(len(grid[0]))]
    flashed = []
    while stack:
        row, col = stack.pop()
        if (row, col) in flashed:
            continue
        grid[row][col] += 1
        if grid[row][col] > 9:
            flashCount += 1
            flashed.append((row, col))
            grid[row][col] = 0
            stack.extend(getNeighbors(grid, row, col))
print(flashCount)