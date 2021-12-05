import re

inputf = "input.txt"
with open(inputf) as f:
  lines = [re.findall("(\d+),(\d+) -> (\d+),(\d+)", x)[0] for x in f.readlines()]
lines = [(int(a), int(b), int(c), int(d)) for a, b, c, d in lines if (a == c or b == d)]

overlaps = {}
for a, b, c, d in lines:
  if a == c:
    for i in range(min(b, d), max(b, d) + 1):
      overlaps[(a, i)] = overlaps.setdefault((a, i), 0) + 1
  elif b == d:
    for i in range(min(a, c), max(a, c) + 1):
      overlaps[(i, b)] = overlaps.setdefault((i, b), 0) + 1
overlaps = {k:v for k, v in overlaps.items() if v > 1}
print(len(overlaps))
