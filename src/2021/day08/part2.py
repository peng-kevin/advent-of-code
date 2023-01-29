import re

inputf = "input.txt"

def tonum(c):
    return ord(c) - ord('a')

def tochar(n):
    return chr(n + ord('a'))

def completeMap(map):
    return len(map) > 0 and all(len(match) == 1 for _, match in map.items())

def validMap(map):
    return len(map) > 0 and all(len(match) >= 1 for _, match in map.items())

def printMap(map):
    for wire, match in map.items():
        print(f"{wire} -> {match}")
    print("")

def sevenSegToNum(wires):
    if set(wires) == set('abcefg'):
        return 0
    elif set(wires) == set('cf'):
        return 1
    elif set(wires) == set('acdeg'):
        return 2
    elif set(wires) == set('acdfg'):
        return 3
    elif set(wires) == set('bcdf'):
        return 4
    elif set(wires) == set('abdfg'):
        return 5
    elif set(wires) == set('abdefg'):
        return 6
    elif set(wires) == set('acf'):
        return 7
    elif set(wires) == set('abcdefg'):
        return 8
    elif set(wires) == set('abcdfg'):
        return 9
    print(f"invalid wire{wires}")

def applyMap(wire, map):
    return [min(map[w]) for w in wire]

def decode(wires, map):
    sum = 0
    for w in wires:
        sum *= 10
        sum += sevenSegToNum(applyMap(w, map))
    return sum

# set(lhs) -> set(rhs)
def updateMap(map, lhs, rhs):
    for wire, pos in map.items():
        if wire in lhs:
            map[wire] = map[wire].intersection(set(rhs))
        else:
            map[wire] = map[wire].difference(set(rhs))
    return map

def findMap(examples, map):
    if(len(examples) == 0):
        return map
    example = examples[0]
    if len(example) == 2: # 1
        map1 = updateMap(map.copy(), example, 'cf') # 1
        if validMap(map1):
            map1 = findMap(examples[1:], map1.copy())
        if completeMap(map1):
            return map1
        else:
            return {}
    elif len(example) == 4: # 4
        map1 = updateMap(map.copy(), example, 'bcdf') # 4
        if validMap(map1):
            map1 = findMap(examples[1:], map1.copy())
        if completeMap(map1):
            return map1
        else:
            return {}
    elif len(example) == 3: # 7
        map1 = updateMap(map.copy(), example, 'acf') # c7
        if validMap(map1):
            map1 = findMap(examples[1:], map1.copy())
        if completeMap(map1):
            return map1
        else:
            return {}
    elif len(example) == 7: # 8
        map1 = updateMap(map.copy(), example, 'abcdefg') # 8
        if validMap(map1):
            map1 = findMap(examples[1:], map1.copy())
        if completeMap(map1):
            return map1
        else:
            return {}
    elif len(example) == 6: # 0, 6 9
        map1 = updateMap(map.copy(), example, 'abcefg') # 0
        if validMap(map1):
            map1 = findMap(examples[1:], map1.copy())
        map2 = updateMap(map.copy(), example, 'abdefg') # 6
        if validMap(map2):
            map2 = findMap(examples[1:], map2.copy())
        map3 = updateMap(map.copy(), example, 'abcdfg') # 9
        if validMap(map3):
            map3 = findMap(examples[1:], map3.copy())
        if completeMap(map1):
            return map1
        elif completeMap(map2):
            return map2
        elif completeMap(map3):
            return map3
        else:
            return {}
    elif len(example) == 5: # 2 3 5
        map1 = updateMap(map.copy(), example, 'acdeg') # 2
        if validMap(map1):
            map1 = findMap(examples[1:], map1.copy())
        map2 = updateMap(map.copy(), example, 'acdfg') # 3
        if validMap(map2):
            map2 = findMap(examples[1:], map2.copy())
        map3 = updateMap(map.copy(), example, 'abdfg') # 5
        if validMap(map3):
            map3 = findMap(examples[1:], map3.copy())
        if completeMap(map1):
            return map1
        elif completeMap(map2):
            return map2
        elif completeMap(map3):
            return map3
        else:
            return {}

with open(inputf) as f:
    lines = f.readlines()
lines = [x.split("|") for x in lines]
total = 0
for l in lines:
    map = {}
    for i in range(7):
        map[tochar(i)] = set('abcdefg')
    examples = l[0].split()
    map = findMap(examples, map.copy())
    total += decode(l[1].split(), map)
print(total)
