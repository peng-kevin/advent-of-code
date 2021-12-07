import re
with open("input.txt") as f:
  lines = [list(x) for x in f.readlines()]

gamma = ""
epsilon = ""
count = [0] * (len(lines[0]) - 1)
total = len(lines)
length = len(count)
for l in lines:
  for i, c in enumerate(l):
    if(c == '1'):
      count[i] += 1
for c in count:
  if c >= total/2:
    gamma += '1'
    epsilon += '0'
  else:
    gamma += '0'
    epsilon += '1'
print(count)
print(total)
print(gamma)
print(epsilon)
gamma = list(gamma)
epsilon = list(epsilon)

glist = lines
i = 0
while len(glist) > 1:
  n1 = 0
  n0 = 0
  for number in glist:
    if number[i] == '1':
      n1 += 1
    else:
      n0 += 1
  if n1 >= n0:
    gamma = '1'
  else:
    gamma = '0'
  nlist = []
  for l in glist:
    if l[i] == gamma:
      nlist.append(l)
  glist = nlist
  i += 1
print(glist)
for i in glist[0]:
  print(i, sep ="", end="")
print("")

elist = lines
i = 0
while len(elist) > 1:
  n1 = 0
  n0 = 0
  for number in elist:
    if number[i] == '1':
      n1 += 1
    else:
      n0 += 1
  if n0 <= n1:
    epsilon = '0'
  else:
    epsilon = '1'
  nlist = []
  for l in elist:
    if l[i] == epsilon:
      nlist.append(l)
  elist = nlist
  i += 1
print(elist)
for i in elist[0]:
  print(i, sep ="", end="")
print("")