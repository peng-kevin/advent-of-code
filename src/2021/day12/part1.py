#!/usr/bin/env python3
import sys
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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} input_file', file=sys.stderr)
        exit(1)

    filename = sys.argv[1]
    with open(filename) as f:
        lines = f.readlines()
    neighbors = collections.defaultdict(list)
    for line in lines:
        pair = line.strip().split("-")
        neighbors[pair[0]].append(pair[1])
        neighbors[pair[1]].append(pair[0])
    print(dfs("start", "end", ["start"], 0, neighbors))


