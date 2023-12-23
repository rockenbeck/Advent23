import re
from collections import defaultdict
from collections import deque
import sys
import random
import math
import numpy as np
import heapq
import bisect 

from input22 import *


test22="""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

class Brick:
    def __init__(self, name, p0, p1) -> None:
        self.name = name

        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        dz = p1[2] - p0[2]

        if dx < 0 or dy < 0 or dz < 0:
            p = p0
            p0 = p1
            p1 = p

        self.p0 = p0
        self.x0 = p0[0]
        self.y0 = p0[1]
        self.z0 = p0[2]
        self.p1 = p1
        self.x1 = p1[0]
        self.y1 = p1[1]
        self.z1 = p1[2]

        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        dz = p1[2] - p0[2]

        self.cx = dx + 1
        self.cy = dy + 1
        self.cz = dz + 1

        self.over = []
        self.under = []

    def __repr__(self):
        return repr((self.name, self.p0, self.p1, self.cx, self.cy, self.cz, list(map(lambda b:b.name, self.over)), list(map(lambda b:b.name, self.under))))

def printbricks(bricks):
    xMin,yMin,zMin = 10000000,10000000,10000000
    xMax,yMax,zMax = 0,0,0
    mpX = defaultdict(list)
    mpY = defaultdict(list)
    
    for b in bricks:
        xMin = min(xMin, b.x0)
        yMin = min(yMin, b.y0)
        zMin = min(zMin, b.z0)
        xMax = max(xMax, b.x1+1)
        yMax = max(yMax, b.y1+1)
        zMax = max(zMax, b.z1+1)

        for z in range(b.z0,b.z1+1):
            for x in range(b.x0,b.x1+1):
                mpX[(x,z)].append(b)
            for y in range(b.y0,b.y1+1):
                mpY[(y,z)].append(b)            
    
    s = ""
    for z in range(zMax - 1, zMin - 1, -1):
        for x in range(xMin, xMax):
            if (x,z) in mpX:
                l = mpX[(x,z)]
                if len(l) == 1:
                    s += l[0].name
                else:
                    s += '?'
            else:
                s += '.'
        s += '\n'
    print(s, "\n")

    s = ""
    for z in range(zMax - 1, zMin - 1, -1):
        for y in range(yMin, yMax):
            if (y,z) in mpY:
                l = mpY[(y,z)]
                if len(l) == 1:
                    s += l[0].name
                else:
                    s += '?'
            else:
                s += '.'
        s += '\n'
    print(s, "\n")
        

def day22(sIn):
    bricks = []

    i = 0
    for line in sIn.split('\n'):
        sp0,sp1 = line.split('~')
        p0 = tuple(map(int, sp0.split(',')))
        p1 = tuple(map(int, sp1.split(',')))
        name = chr(i + ord('A'))
        bricks.append(Brick(name,p0,p1))
        i += 1

    # print(bricks)

    # mpXyBricks = defaultdict(list)
    # for brick in bricks:
    #     p = brick.p0
    #     if brick.cx > 0:
    #         for dx in range(0,brick.cx):
    #             mpXyBricks[(p[0] + dx, p[1])].append(brick)
    #     elif brick.cy > 0:
    #         for dy in range(0,brick.cy):
    #             mpXyBricks[(p[0], p[1] + dy)].append(brick)
    #     else:
    #         mpXyBricks[(p[0], p[1])].append(brick)
            
    for b in bricks:
        for bT in bricks:
            if bT == b:
                continue
            if (bT.x0 <= b.x1 and bT.x1 >= b.x0) and (bT.y0 <= b.y1 and bT.y1 >= b.y0):
                # overlap in xy
                if bT.z0 > b.z1:
                    b.under.append(bT)
                else:
                    assert bT.z1 < b.z0 # else penetrating?

    for b in bricks:
        for bT in b.under:
            bT.over.append(b)
        b.settled = False

    # print(bricks)

    # printbricks(bricks)

    # should sort somehow
    while True:
        moved = False

        for b in bricks:
            if b.settled:
                continue
            allset = True
            zMin = 1
            for bT in b.over:
                if not bT.settled:
                    allset = False
                zMin = max(zMin, bT.z1 + 1)
            if allset:
                b.z0 = zMin
                b.z1 = zMin + b.cz - 1
                b.settled = True
                moved = True

        if not moved:
            break

    # printbricks(bricks)
    
    part1 = False
    if part1:
        total = 0
        for b in bricks:
            fall = False
            for bT in b.under:
                if bT.z0 == b.z1 + 1:
                    csup = 0
                    for b2 in bT.over:
                        if bT.z0 == b2.z1 + 1:
                            csup += 1
                    if csup == 1:
                        fall = True
                        break
            if not fall:
                total += 1

        print(f"total removable = {total}")

    else:
        total = 0

        bsort = sorted(bricks, key = lambda b: b.z0)

        for bTest in bricks:
            for b in bricks:
                b.fall = (b == bTest)
            
            cfall = 0
            for b in bsort:
                if b.z0 == 1:
                    assert len(b.over) == 0
                    continue
                anysup = False
                for bT in b.over:
                    if bT.z1 + 1 == b.z0 and not bT.fall:
                        anysup = True
                        break
                if not anysup:
                    b.fall = True
                    cfall += 1
            # print(f"{bTest.name}: {cfall}")

            total += cfall

    print(f"total fall = {total}")    

# day22(test22)
day22(input22)
