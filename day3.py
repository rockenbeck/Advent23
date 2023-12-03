
import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input3 import *


test3="""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

def day3a(sFile):
    mp = defaultdict(lambda: '.')
    y = 0
    for line in sFile.split('\n'):
        x = 0
        for ch in line:
            if ch != '.':
                mp[(x,y)] = ch
            x += 1
        y += 1

    yMax = y
    xMax = x

    # print(mp[(2,0)])

    total = 0
    for y in range(0,yMax):
        n = 0
        fAdj = False
        fWasNum = False
        for x in range(-1,xMax+1):
            fAdj3 = False
            for dY in (-1,0,1):
                if mp[(x,y + dY)] != '.' and not mp[(x,y + dY)].isdigit():
                    fAdj3 = True
            if mp[(x,y)].isdigit():
                fAdj = fAdj or fAdj3
                n = n * 10 + int(mp[(x,y)])
                fWasNum = True
            else:
                if fWasNum:
                    fAdj = fAdj or fAdj3
                    if fAdj:
                        print(n)
                        total += n
                    fWasNum = False
                    n = 0

                fAdj = fAdj3
    
    print(total)

#day3a(input3)


def day3b(sFile):
    mp = defaultdict(lambda: '.')
    y = 0
    for line in sFile.split('\n'):
        x = 0
        for ch in line:
            if ch != '.':
                mp[(x,y)] = ch
            x += 1
        y += 1

    yMax = y
    xMax = x

    # print(mp[(2,0)])

    gears = defaultdict(list)
    for y in range(0,yMax):
        n = 0        
        fWasNum = False
        gearsAdj = set()
        for x in range(-1,xMax+1):
            gears3 = set()
            for dY in (-1,0,1):
                if mp[(x,y + dY)] == '*':
                    gears3.add((x,y+dY))
            if mp[(x,y)].isdigit():
                gearsAdj = gearsAdj.union(gears3)
                n = n * 10 + int(mp[(x,y)])
                fWasNum = True
            else:
                if fWasNum:
                    gearsAdj = gearsAdj.union(gears3)
                    for (xGear,yGear) in gearsAdj:
                        #print(n)
                        gears[(xGear,yGear)].append(n)
                    fWasNum = False
                    n = 0

                gearsAdj = gears3

    total = 0    
    for (x,y),ns in gears.items():
        print ((x,y),ns)
        if len (ns) == 2:
            total += ns[0] * ns[1]
    print(total)

day3b(input3)