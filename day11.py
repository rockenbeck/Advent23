
import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input11 import *

test11 = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

def day11(sIn):
    mp = {}

    stars = []

    y = 0
    for line in sIn.split('\n'):
        x = 0
        for ch in line:
            mp[(x,y)] = ch
            if ch == '#':
                stars.append((x,y))
            x += 1
        y += 1

    xMax = x
    yMax = y

    sumX = [0]
    n = 0
    for x in range(0,xMax):
        n += 1
        empty = True
        for y in range(0,yMax):
            if mp[(x,y)] == '#':
                empty = False
                break
        if empty:
            n += 1000000 - 1
        sumX.append(n)

    sumY = [0]
    n = 0
    for y in range(0,yMax):
        n += 1
        empty = True
        for x in range(0,xMax):
            if mp[(x,y)] == '#':
                empty = False
                break
        if empty:
            n += 1000000 - 1
        sumY.append(n)

    total = 0

    for a in range(0,len(stars)):
        xA,yA = stars[a]
        for b in range(a + 1, len(stars)):
            xB,yB = stars[b]
            l = abs(sumX[xB] - sumX[xA]) + abs(sumY[yB] - sumY[yA])
            total += l

    print(f"total = {total}")

day11(input11)


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