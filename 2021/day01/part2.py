with open("input.txt") as f:
  lines = [int(x) for x in f.readlines()]
prev = lines[0]
sum = 0
for a, b in zip(lines[:-3], lines[3:]):
  if b > a:
    sum += 1
print(sum)