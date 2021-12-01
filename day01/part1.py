with open("input.txt") as f:
  lines = [int(x) for x in f.readlines()];
prev = lines[0]
sum = 0
for l in lines[1:]:
  if l > prev:
    sum += 1
  prev = l
print(sum)