#!/usr/bin/env python3
import re
import math
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} input_file', file=sys.stderr)
        exit(1)

    filename = sys.argv[1]
    with open(filename) as f:
        pos = [int(x) for x in f.read().split(",")]

    a = min(pos)
    b = max(pos)
    best = a
    cost = math.inf
    for i in range(a, b + 1):
        c = 0
        for p in pos:
            d = abs(p - i)
            if d > 0:
                c = c + d * (d + 1)/2
        if c < cost:
            cost = c
            best = i
    print(best)
    print(cost)
