import time
import sys

delay = 0.05
class colors:
    RED = "\033[0;31m"
    YELLOW = "\033[0;33m"
    GREEN = "\033[0;32m"
    RESET = "\033[0m"

# the current set of examples
currentExamples = []

# the minm

def colorNum(n, width):
    if n in [0, 6, 2, 3]:
        return colors.YELLOW + '{num:{width}}'.format(num=n, width=width) + colors.RESET
    else:
        return colors.GREEN + '{num:{width}}'.format(num=n, width=width) + colors.RESET

def printExamples(examples):
    output = "["
    for e in examples:
        output += e + ", "
    output = output[:-2] + "]"
    print(output)

def printMap(map):
    for wire, match in map.items():
        if len(match) == 0:
            print(f"\u001b[0K{colors.RED}{wire} -> {{}}{colors.RESET}")
        elif len(match) == 1:
            print(f"\u001b[0K{colors.GREEN}{wire} -> {match}{colors.RESET}")
        else:
            print(f"\u001b[0K{wire} -> {match}")

def printProgress(currentGuesses, map, needToClear):
    if needToClear:
        # goes up 8 lines
        print("\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F")
    l = len(currentGuesses)
    if completeMap(map) and l == len(currentExamples):
        # we know that all guesses are currect
        allGreen = True
    else:
        allGreen = False
    output = "\u001b[0K["
    for e, g in zip(currentExamples, currentGuesses):
        if allGreen:
            output = output + colors.GREEN + '{num:{width}}'.format(num=g, width=len(e)) + colors.RESET + ", "
        else:
            output = output + colorNum(g, len(e)) + ", "
    for e in currentExamples[l:]:
        output = output + e + ", "
    output = output[:-2] + "]"
    print(output)
    printMap(map)
    time.sleep(delay)

def printDisplay(map, codes):
    invertedMap = {}
    decodedWires = [{min(map[w]) for w in wires} for wires in codes]
    for k, v in map.items():
        invertedMap[min(v)] = k
    dotRow = " .... "
    row1 = " " + invertedMap['a'] * 4 + " "
    row23 = invertedMap['b'] + "    " + invertedMap['c']
    row4 = " " + invertedMap['d'] * 4 + " "
    row56 = invertedMap['e'] + "    " + invertedMap['f']
    row7 = " " + invertedMap['g'] * 4 + " "
    print(row1, end="  ")
    for wires in decodedWires:
        if 'a' in wires:
            print(colors.GREEN + row1 + colors.RESET, end="")
        else:
            print(dotRow, end="")
        print("  ", end="")
    print("")
    for i in range(2):
        print(row23, end="  ")
        for wires in decodedWires:
            if 'b' in wires:
                print(colors.GREEN + invertedMap['b'] + colors.RESET, end="")
            else:
                print(".", end="")
            print("    ", end="")
            if 'c' in wires:
                print(colors.GREEN + invertedMap['c'] + colors.RESET, end="")
            else:
                print(".", end="")
            print("  ", end="")
        print("")
    print(row4, end="  ")
    for wires in decodedWires:
        if 'd' in wires:
            print(colors.GREEN + row4 + colors.RESET, end="")
        else:
            print(dotRow, end="")
        print("  ", end="")
    print("")
    for i in range(2):
        print(row56, end="  ")
        for wires in decodedWires:
            if 'e' in wires:
                print(colors.GREEN + invertedMap['e'] + colors.RESET, end="")
            else:
                print(".", end="")
            print("    ", end="")
            if 'f' in wires:
                print(colors.GREEN + invertedMap['f'] + colors.RESET, end="")
            else:
                print(".", end="")
            print("  ", end="")
        print("")
    print(row7, end="  ")
    for wires in decodedWires:
        if 'g' in wires:
            print(colors.GREEN + row7 + colors.RESET, end="")
        else:
            print(dotRow, end="")
        print("  ", end="")
    print("")
    time.sleep(delay)

def completeMap(map):
    return len(map) > 0 and all(len(match) == 1 for _, match in map.items())

def validMap(map):
    return len(map) > 0 and all(len(match) >= 1 for _, match in map.items())


# given a set of standard wires, return the corresponding number
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

# given a set of set of wires, decode each and get the combined number
def decode(code, map):
    sum = 0
    for wires in code:
        sum *= 10
        sum += sevenSegToNum(applyMap(wires, map))
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

if len(sys.argv) != 3:
    print(f"usage: python3 {sys.argv[0]} input delay")
    sys.exit(1)
with open(sys.argv[1]) as f:
    lines = f.readlines()
lines = [x.split("|") for x in lines]
try:
    delay = int(sys.argv[2])
except:
    print("delay must be a number")

total = 0
for l in lines:
    map = {}
    for i in range(7):
        map[chr(i + ord('a'))] = set('abcdefg')
    examples = l[0].split()
    currentExamples = examples.copy()
    printExamples(examples)
    printProgress([], map, False)
    map = findMap(examples, map.copy(), [])
    printExamples(l[1].split())
    printDisplay(map, l[1].split())
    print("")
    total += decode(l[1].split(), map)
print(total)
