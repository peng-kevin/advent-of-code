import time

inputf = "sample.txt"

class colors:
    RED = "\033[0;31m"
    YELLOW = "\033[0;33m"
    GREEN = "\033[0;32m"
    RESET = "\033[0m"

# the current set of examples
currentExamples = []
# the current guesses for what the examples correspond to
currentGuesses = []

# the minm

def colorNum(n):
    if n in [0, 6, 2, 3]:
        return colors.YELLOW + str(n) + colors.RESET
    else:
        return colors.GREEN + str(n) + colors.RESET


def printMap(map):
    for wire, match in map.items():
        if len(match) == 0:
            print(f"\u001b[0K{wire} -> {colors.RED}{{}}{colors.RESET}")
        elif len(match) == 1:
            print(f"\u001b[0K{wire} -> {colors.GREEN}{match}{colors.RESET}")
        else:
            print(f"\u001b[0K{wire} -> {match}")

def printProgress(currentGuesses, map, needToClear):
    if needToClear:
        # goes up 8 lines
        print("\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F")
    l = len(currentGuesses)
    output = "\u001b[0K["
    for g in currentGuesses:
        output = output + colorNum(g) + ", "
    for e in currentExamples[l:]:
        output = output + e + ", "
    output = output[:-2] + "]"
    print(output)
    printMap(map)
    time.sleep(1)

def tonum(c):
    return ord(c) - ord('a')

def tochar(n):
    return chr(n + ord('a'))

def completeMap(map):
    return len(map) > 0 and all(len(match) == 1 for _, match in map.items())

def validMap(map):
    return len(map) > 0 and all(len(match) >= 1 for _, match in map.items())



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

def findMap(examples, map, currentGuesses):
    if(len(examples) == 0):
        return map
    example = examples[0]
    if len(example) == 2: # 1
        map1 = updateMap(map.copy(), example, 'cf') # 1
        currentGuesses.append(1)
        printProgress(currentGuesses, map1, True)
        if validMap(map1):
            map1 = findMap(examples[1:], map1.copy(), currentGuesses.copy())
        if completeMap(map1):
            return map1
        return {}
    elif len(example) == 4: # 4
        map1 = updateMap(map.copy(), example, 'bcdf') # 4
        currentGuesses.append(4)
        printProgress(currentGuesses, map1, True)
        if validMap(map1):
            map1 = findMap(examples[1:], map1.copy(), currentGuesses.copy())
        if completeMap(map1):
            return map1
        return {}
    elif len(example) == 3: # 7
        map1 = updateMap(map.copy(), example, 'acf') # 7
        currentGuesses.append(7)
        printProgress(currentGuesses, map1, True)
        if validMap(map1):
            map1 = findMap(examples[1:], map1.copy(), currentGuesses.copy())
        if completeMap(map1):
            return map1
        return {}
    elif len(example) == 7: # 8
        map1 = updateMap(map.copy(), example, 'abcdefg') # 8
        currentGuesses.append(8)
        printProgress(currentGuesses, map1, True)
        if validMap(map1):
            map1 = findMap(examples[1:], map1.copy(), currentGuesses.copy())
        if completeMap(map1):
            return map1
        return {}
    elif len(example) == 6: # 0, 6 9
        map1 = updateMap(map.copy(), example, 'abcefg') # 0
        currentGuesses.append(0)
        printProgress(currentGuesses, map1, True)
        if validMap(map1):
            map1 = findMap(examples[1:], map1.copy(), currentGuesses.copy())
            if completeMap(map1):
                return map1
        map2 = updateMap(map.copy(), example, 'abdefg') # 6
        currentGuesses[-1] = 6
        printProgress(currentGuesses, map2, True)
        if validMap(map2):
            map2 = findMap(examples[1:], map2.copy(), currentGuesses.copy())
            if completeMap(map2):
                return map2
        map3 = updateMap(map.copy(), example, 'abcdfg') # 9
        currentGuesses[-1] = 9
        printProgress(currentGuesses, map3, True)
        if validMap(map3):
            map3 = findMap(examples[1:], map3.copy(), currentGuesses.copy())
            if completeMap(map3):
                return map3
            return map3
        return {}
    elif len(example) == 5: # 2 3 5
        map1 = updateMap(map.copy(), example, 'acdeg') # 2
        currentGuesses.append(2)
        printProgress(currentGuesses, map1, True)
        if validMap(map1):
            map1 = findMap(examples[1:], map1.copy(), currentGuesses.copy())
            if completeMap(map1):
                return map1
        map2 = updateMap(map.copy(), example, 'acdfg') # 3
        currentGuesses[-1] = 3
        printProgress(currentGuesses, map2, True)
        if validMap(map2):
            map2 = findMap(examples[1:], map2.copy(), currentGuesses.copy())
            if completeMap(map2):
                return map2
        map3 = updateMap(map.copy(), example, 'abdfg') # 5
        currentGuesses[-1] = 5
        printProgress(currentGuesses, map3, True)
        if validMap(map3):
            map3 = findMap(examples[1:], map3.copy(), currentGuesses.copy())
            if completeMap(map3):
                return map3
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
    currentExamples = examples.copy()
    printProgress([], map, False)
    map = findMap(examples, map.copy(), [])
    total += decode(l[1].split(), map)
print(total)
