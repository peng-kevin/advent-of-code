import re

inputf = "input.txt"
with open(inputf) as f:
  lines = [re.findall("(\d+),(\d+) -> (\d+),(\d+)", x)[0] for x in f.readlines()]
lines = [(int(x1), int(y1), int(x2), int(y2)) for x1, y1, x2, y2 in lines if (x1 == x2 or y1 == y2)]

overlaps = {}
for x1, y1, x2, y2 in lines:
  if x1 == x2:
    for i in range(min(y1, y2), max(y1, y2) + 1):
      overlaps[(x1, i)] = overlaps.setdefault((x1, i), 0) + 1
  elif y1 == y2:
    for i in range(min(x1, x2), max(x1, x2) + 1):
      overlaps[(i, y1)] = overlaps.setdefault((i, y1), 0) + 1
overlaps = {k:v for k, v in overlaps.items() if v > 1}
print(len(overlaps))
