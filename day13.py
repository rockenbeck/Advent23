import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input13 import *

test13="""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

class Map:
    def __init__(self, s):
        self.mp = {}

        y = 0
        for line in s.split('\n'):
            x = 0
            for ch in line:
                self.mp[(x,y)] = ch
                x += 1
            y += 1

        self.xMax = x
        self.yMax = y

def reflect(ns):
    for i in range(1,len(ns)):
        for j in range(0,len(ns)):
            if i - j - 1 < 0 or i + j >= len(ns):
                return i
            if ns[i - j - 1] != ns[i + j]:
                break
    
    return None

def day13(sIn):

    total = 0

    for sMap in sIn.split('\n\n'):
        # print(sMap,"\n\n")

        mp = {}

        y = 0
        for line in sMap.split('\n'):
            x = 0
            for ch in line:
                mp[(x,y)] = ch
                x += 1
            y += 1

        xMax = x
        yMax = y

        cols = []
        for x in range(0,xMax):
            n = 0
            for y in range(0,yMax):
                n *= 2
                if mp[(x,y)] == '#':
                    n += 1
            cols.append(n)

        i = reflect(cols)
        if i != None:
            total += i
            continue

        rows = []
        for y in range(0,yMax):
            n = 0
            for x in range(0,xMax):
                n *= 2
                if mp[(x,y)] == '#':
                    n += 1
            rows.append(n)

        i = reflect(rows)
        if i != None:
            total += 100 * i
            continue

        assert False

    print(f"total = {total}")

# day13(test13)
# day13(input13)


def reflectSmudge(ns):
    ret = None
    for i in range(1,len(ns)):
        diff = 0
        for j in range(0,len(ns)):
            if i - j - 1 < 0 or i + j >= len(ns):
                if diff != 0 and diff & (diff - 1) == 0:
                    assert ret==None
                    ret = i
                break
            
            d = ns[i - j - 1] ^ ns[i + j]
            if d != 0 and (diff != 0 or d & (d - 1) != 0):
                break
            diff += d
    
    return ret

def day13b(sIn):

    total = 0

    for sMap in sIn.split('\n\n'):
        # print(sMap,"\n\n")

        mp = {}

        y = 0
        for line in sMap.split('\n'):
            x = 0
            for ch in line:
                mp[(x,y)] = ch
                x += 1
            y += 1

        xMax = x
        yMax = y

        cols = []
        for x in range(0,xMax):
            n = 0
            for y in range(0,yMax):
                n *= 2
                if mp[(x,y)] == '#':
                    n += 1
            cols.append(n)

        i = reflectSmudge(cols)
        if i != None:
            s = " "*(i-1) + "><\n"
            s += sMap
            s += "\n" +" "*(i-1) + "><\n"
            # print(s,"\n\n")
            iOld = reflect(cols)
            assert i != iOld
            total += i
            continue

        rows = []
        for y in range(0,yMax):
            n = 0
            for x in range(0,xMax):
                n *= 2
                if mp[(x,y)] == '#':
                    n += 1
            rows.append(n)

        i = reflectSmudge(rows)
        if i != None:
            s = ""
            for j,line in enumerate(sMap.split('\n')):
                if j == i-1:
                    s += "v"
                elif j == i:
                    s += '^'
                else:
                    s += ' '
                s += line + "\n"
            # print(s,"\n\n")
            iOld = reflect(rows)
            assert i != iOld

            total += 100 * i
            continue

        assert False

    print(f"total = {total}")

test13b="""####.####.#
#..#.#..#.#
#..#.####.#
####.#..#.#
.##.##..##.
######..###
#####.##.##
#..########
......##...
.##........
#####....##
######..###
..#.#.##.#.
######..###
.##...##...
#..#.####.#
######..###"""

test13c=""".#.....
..#####
####..#
...####
##.#..#
#.##..#
.#.#..#
#..####
#.##..#
..##..#
#..####"""

# day13b(test13c)
day13b(input13)

# 25918 was wrong
# 27409 wrong low