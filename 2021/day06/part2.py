import re

inputf = "input.txt"
with open(inputf) as f:
    times = [int(x) for x in re.findall("\d+", f.readline())];
record = [0] * 9

for t in times:
    record[t] += 1
for i in range(256):
    next = [0] * 9
    for j in range(1, 9):
        next[j - 1] = record[j]
    next[6] += record[0]
    next[8] += record[0]
    record = next
sum = 0
for i in record:
    sum = sum + i
print(sum)
