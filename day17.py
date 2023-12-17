import re
from collections import defaultdict
import sys
import random
import math
import numpy as np
import heapq

from input17 import *


test17="""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

def day17(sIn):
    # ought to wrap these in a mapify fn

    mp = {}

    y = 0
    for line in sIn.split('\n'):
        x = 0
        for ch in line:
            mp[(x,y)] = int(ch)
            x += 1
        y += 1

    xMax = x
    yMax = y

    best = defaultdict(lambda : (100000000, -1, -1))
    heap = []
    heapq.heappush(heap, (0,0,0,''))

    part = 2

    while len(heap) > 0:
        score, x, y, hist = heapq.heappop(heap)
        if x == xMax - 1 and y == yMax - 1:
            print(f"best = {score}")
            break
        for dx,dy,dir,opp in [(-1,0,'<','>'), (1,0,'>','<'), (0,-1,'^','v'), (0,1,'v','^')]:
            if len(hist) > 0 and hist[-1] == opp:
                continue
            if part == 1:
                if len(hist) == 3 and hist[-1] == dir:
                    continue
            else:
                if len(hist) == 10 and hist[-1] == dir:
                    continue
                if len(hist) > 0 and len(hist) < 4 and hist[-1] != dir:
                    continue
                
            xNew = x + dx
            yNew = y + dy
            if xNew < 0 or xNew >= xMax or yNew < 0 or yNew >= yMax:
                continue
            scoreNew = score + mp[(xNew,yNew)]
            if len(hist) == 0 or hist[-1] == dir:
                histNew = hist + dir
            else:
                histNew = dir
            if scoreNew < best[(xNew,yNew,histNew)][0]:
                best[(xNew,yNew,histNew)] = (scoreNew, x, y)
                # print(f"{(score,x,y,hist)} + '{dir}' => {(scoreNew,xNew,yNew,histNew)}")
                heapq.heappush(heap, (scoreNew,xNew,yNew,histNew))

    # this doesn't work with the new best[] format including hist
    # onPath = set()
    # x,y = xMax-1, yMax-1
    # while x != 0 or y != 0:
    #     onPath.add((x,y))
    #     b = best[(x,y)]
    #     x = b[1]
    #     y = b[2]

    # s = ""
    # for y in range(0,yMax):
    #     for x in range(0,xMax):
    #         if (x,y) in onPath:
    #             s += "*"
    #         else:
    #             s += str(mp[(x,y)])
    #     s += '\n'
    # print(s)

# day17(test17)
day17(input17)

