#!/usr/bin/env python3
import re
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} input_file', file=sys.stderr)
        exit(1)

    filename = sys.argv[1]
    with open(filename) as f:
        times = [int(x) for x in re.findall("\d+", f.readline())];
    record = [0] * 9

    for t in times:
        record[t] += 1
    for i in range(80):
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
