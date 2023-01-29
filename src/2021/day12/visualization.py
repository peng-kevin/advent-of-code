import collections
import networkx as nx

def dfs(src, dest, used, numpaths, g):
    if src == dest:
        return numpaths + 1
    for adj in g[src]:
        if used[adj] == 0 or (used[adj] == 1 and 2 not in used.values()):
            if adj.islower():
                used[adj] += 1
            numpaths = dfs(adj, dest, used, numpaths, g)
            if adj.islower():
                used[adj] -= 1
    return numpaths

inputf = "sample.txt"
with open(inputf) as f:
    lines = f.readlines()
graph = nx.Graph()
for line in lines:
    pair = line.strip().split("-")
    graph.add_node(pair[0])
    graph.add_node(pair[1])
    graph.add_edge((pair[0], pair[1]))
    graph.add_edge((pair[1], pair[0]))
used = collections.defaultdict(lambda: 0)
used["start"] = -1
print(dfs("start", "end", used, 0, graph))


