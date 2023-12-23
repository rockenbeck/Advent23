import re
from collections import defaultdict
from collections import deque
import sys
import random
import math
import numpy as np
import heapq
import bisect 

from input21 import *

test21="""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

def day21(sIn):
    # ought to wrap these in a mapify fn

    mp = {}

    y = 0
    for line in sIn.split('\n'):
        x = 0
        for ch in line:
            if ch == 'S':
                start = (x,y)
                ch = '.'
            mp[(x,y)] = ch
            x += 1
        y += 1

    xMax = x
    yMax = y

    r = set()
    r.add(start)

    for i in range(0,64):
        rNew = set()
        for xy in r:
            for dxy in [(-1,0),(1,0),(0,-1),(0,1)]:
                xyn = (xy[0] + dxy[0], xy[1] + dxy[1])
                if xyn in mp and mp[xyn] != '#':
                    rNew.add(xyn)
        r = rNew

    s = ""
    for y in range(0,yMax):
        for x in range(0,xMax):
            if (x,y) in r:
                s += 'O'
            else:
                s += mp[(x,y)]
        s += '\n'
    print(s)
    
    print(f"len = {len(r)}")
                    

# day21(test21)
# day21(input21)


def day21b(sIn):
    # ought to wrap these in a mapify fn

    mp = {}

    y = 0
    for line in sIn.split('\n'):
        x = 0
        for ch in line:
            if ch == 'S':
                start = (x,y)
                ch = '.'
            mp[(x,y)] = ch
            x += 1
        y += 1

    xMin = 0
    yMin = 0
    xMax = x
    yMax = y
    xMaxOrig = xMax
    yMaxOrig = yMax

    print(f"max={(xMax,yMax)}")

    r = set()
    r.add(start)

    prev = 0
    for j in range(0,10):
        n = 65 if j == 0 else 131
        for i in range(0,n):
            rNew = set()
            for xy in r:
                for dxy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    xyn = ((xy[0] + dxy[0]), (xy[1] + dxy[1]))
                    # xMin = min(xMin, xyn[0])
                    # xMax = max(xMax, xyn[0]+1)
                    # yMin = min(yMin, xyn[1])
                    # yMax = max(yMax, xyn[1]+1)
                    xylook = ((xy[0] + dxy[0]) % xMaxOrig, (xy[1] + dxy[1]) % yMaxOrig)
                    if mp[xylook] != '#':
                        rNew.add(xyn)
            r = rNew
        print(f"j = {j}, total = {len(r)}, delta={len(r) - prev} = {(len(r) - prev)/3598}")
        # print(f"min={(xMin,yMin)} max={(xMax,yMax)}")
        prev = len(r)

        if j in [0,1] or True:
            s = ""
            # for y in range(yMin,yMax):
                # for x in range(xMin,xMax):
            for y in range(yMin,yMin+3):
                for x in range(xMin + (xMax-xMin)//2 - 10,xMin + (xMax-xMin)//2 + 10):
                    if (x,y) in r:
                        s += 'O'
                    else:
                        s += mp[(x%xMaxOrig,y%yMaxOrig)]
                s += '\n'
            print(s)
    
    print(f"len = {len(r)}")
                    
# day21b(test21)
# day21b(input21)

# 64 steps => 3598

# N = (26501365 - 65) // 131 # 202300 (ha)
# N = 2
# A1 = 3738
# B = (29532 - 4*A) // 4 # = 3645
# print(f"A1 = {A1} A = {A} B = {B}, N = {N}")
# print(f"sum = {A1 + (A+B)*2*(N*N + N)}")

N = (26501365 - 65) // 131 # 202300 (ha)
# N = 2
A1 = 3738
# X = # 4 * (A + B)
# Y = # 4 * (A' + B')
# AN = N(N+2)//4 # for even N
# BN = N*N//4 # for even N
# total = A1 + AN * X + BN * Y

# N = 2, total = 92194, delta=58924 
# N = 4, total = 298218, delta=117708

A2 = 2
B2 = 1
A4 = 6
B4 = 4

# 92194 = A1 + 2*X + Y
# 298218 = A1 + 6*X + 4*Y
# Y = (92194 - A1) - 2*X
# 298218 - A1 = 6X - 8X + 4(92194 - A1)
X = int((4 * (92194 - A1) - (298218 - A1)) / 2)
Y = int((92194 - A1) - 2*X)
print(f"X = {int(X)} Y = {int(Y)}")
AN = N*(N+2)//4 # for even N
BN = N*N//4 # for even N
print(f"AN = {AN} BN = {BN}")

# print(f"A1 = {A1} A = {A} B = {B}, N = {N}")
print(f"sum = {A1 + AN * X + BN * Y}")


# 4A + 4B = 29532
# 8A + 8B = 58924
# AB = 29532 # A + B

# j = 0, total = 3738, delta=3738 = 1.038910505836576
# ..........O.........
# #.#.#....O.O....#...
# ...#....O.O.O.....##

# j = 1, total = 33270, delta=29532 = 8.207893274041133
# .O.O.O.O.O.O.O.O.O.O
# #.#.#.O.O.O.O.O.#.O.
# .O.#.O.O.O.O.O.O.O##

# j = 2, total = 92194, delta=58924 = 16.37687604224569
# O.O.O.O.O.O.O.O.O.O.
# #O#O#O.O.O.O.O.O#O.O
# O.O#O.O.O.O.O.O.O.##

# j = 3, total = 180510, delta=88316 = 24.54585881045025
# .O.O.O.O.O.O.O.O.O.O
# #.#.#.O.O.O.O.O.#.O.
# .O.#.O.O.O.O.O.O.O##

# j = 4, total = 298218, delta=117708 = 32.714841578654806
# O.O.O.O.O.O.O.O.O.O.
# #O#O#O.O.O.O.O.O#O.O
# O.O#O.O.O.O.O.O.O.##

# j = 5, total = 445318, delta=147100 = 40.88382434685936
# .O.O.O.O.O.O.O.O.O.O
# #.#.#.O.O.O.O.O.#.O.
# .O.#.O.O.O.O.O.O.O##