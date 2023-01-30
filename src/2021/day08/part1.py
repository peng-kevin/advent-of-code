#!/usr/bin/env python3
import re
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} input_file', file=sys.stderr)
        exit(1)

    filename = sys.argv[1]
    with open(filename) as f:
        lines = f.readlines()
    lines = [x.split("|") for x in lines]
    total = 0
    sum = 0
    for l in lines:
        out = l[1].split()
        for o in out:
            if len(o) == 2 or len(o) == 4 or len(o) == 3 or len(o) == 7:
                sum = sum + 1
    print(total)
    print(sum)
