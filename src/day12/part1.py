import collections

def dfs(src, dest, used, numpaths, g):
    if src == dest:
        return numpaths + 1
    for adj in g[src]:
        if adj not in used:
            if adj.islower():
                used.append(adj)
            numpaths = dfs(adj, dest, used, numpaths, g)
            if adj.islower():
                used.pop()
    return numpaths

inputf = "input.txt"
with open(inputf) as f:
    lines = f.readlines()
neighbors = collections.defaultdict(list)
for line in lines:
    pair = line.strip().split("-")
    neighbors[pair[0]].append(pair[1])
    neighbors[pair[1]].append(pair[0])
print(dfs("start", "end", ["start"], 0, neighbors))


