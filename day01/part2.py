with open("input.txt") as f:
  lines = [int(x) for x in f.readlines()];
prev1 = lines[0]
prev2 = lines[1]
prev3 = lines[2]
sum = 0
for l in lines[1:-2]:
  if prev2 + prev3 + l > prev1 + prev2 + prev3:
    sum += 1
  prev1 = prev2
  prev2 = prev3
  prev3 = l
print(sum)