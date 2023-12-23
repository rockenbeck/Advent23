import re
from collections import defaultdict
import sys
import random
import math
import numpy as np
import heapq
import bisect 

from input18 import *

test18="""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

def day18(sIn):
    mp = {}

    dirs = {'R':(1,0), 'L':(-1,0), 'U':(0,-1), 'D':(0,1)}
    rights = {'R':'D', 'L':'U', 'U':'R', 'D':'L'}
    lefts = {'R':'U', 'L':'D', 'U':'L', 'D':'R'}

    xMin,yMin = 10000,10000
    xMax,yMax = -10000,-10000

    l = []

    x,y = 0,0
    for line in sIn.split('\n'):
        dir,sC,sRgb = line.split(' ')
        c = int(sC)
        dx,dy = dirs[dir]
        l.append((x,y,dir))
        for i in range(0,c):
            x += dx
            y += dy
            mp[(x,y)] = dir
            xMin = min(x,xMin)
            yMin = min(y,yMin)
            xMax = max(x+1,xMax)
            yMax = max(y+1,yMax)
            l.append((x,y,dir))

    # really ugly algorithm
    
    while len(l) > 0:
        lNew = []
        dirPrev = l[-1][2]
        for x,y,dir in l:
            if dir == lefts[dirPrev]:
                dx,dy = dirs[rights[dir]]
                dx2,dy2 = dirs[rights[dirPrev]]
                x2 = x + dx + dx2
                y2 = y + dy + dy2
                if (x2,y2) not in mp:
                    mp[(x2,y2)] = dirPrev
                    lNew.append((x2,y2,dirPrev))

            dx,dy = dirs[rights[dir]]
            x2 = x + dx
            y2 = y + dy
            if (x2,y2) not in mp:
                mp[(x2,y2)] = dir
                lNew.append((x2,y2,dir))

            dirPrev = dir
        l = lNew

    # xMin = xMin + 100
    # yMin = yMin + 100
    # xMax = xMin + 150
    # yMax = yMin + 150
    s = ""
    for y in range(yMin,yMax):
        for x in range(xMin,xMax):
            if (x,y) in mp:
                s += mp[(x,y)]
            else:
                s += '.'
        s += '\n'
    print(s)

    print(f"area = {len(mp)}")

# day18(test18)
# day18(input18)



def day18b(sIn):
    mp = {}

    dirs = {'R':(1,0), 'L':(-1,0), 'U':(0,-1), 'D':(0,1)}
    rights = {'R':'D', 'L':'U', 'U':'R', 'D':'L'}
    lefts = {'R':'U', 'L':'D', 'U':'L', 'D':'R'}

    corners = [] # add/remove,x,y

    part1 = False
    l = []
    for line in sIn.split('\n'):
        dir,sC,sRgb = line.split(' ')
        if part1:
            c = int(sC)
        else:
            c = int(sRgb[2:7], 16)
            dir = "RDLU"[int(sRgb[7])]

        assert c != 0
        l.append((dir,c))

    # print(l)

    x,y = 0,0
    dirPrev = l[-1][0]
    for dir,c in l:
        if dirPrev == 'L' and dir == 'U':
            corners.append(("remove",x,y+1))
        elif dirPrev == 'L' and dir == 'D':
            corners.append(("add",x,y+1))
        elif dirPrev == 'U' and dir == 'R':
            corners.append(("add",x,y))
        elif dirPrev == 'U' and dir == 'L':
            corners.append(("add",x,y+1))
        elif dirPrev == 'R' and dir == 'D':
            corners.append(("add",x,y))
        elif dirPrev == 'R' and dir == 'U':
            corners.append(("remove",x,y))
        elif dirPrev == 'D' and dir == 'L':
            corners.append(("remove",x,y+1))
        elif dirPrev == 'D' and dir == 'R':
            corners.append(("remove",x,y))
        else:
            assert False

        dx,dy = dirs[dir]
        x += c * dx
        y += c * dy

        dirPrev = dir

    corners.sort(key=lambda edge: edge[2])

    # print(corners)

    edges = [] 
    
    yCur = corners[0][2]

    total = 0
    for ar,x,y in corners:
        if yCur < y:
            dy = y - yCur
            # print(edges, dy)
            assert len(edges) & 1 == 0
            for i in range(0,len(edges),2):
                xMin,xMost = edges[i],edges[i+1]
                total += dy * (xMost - xMin + 1)
        yCur = y
        if ar == "add":
            bisect.insort(edges, x)
        else:
            assert ar == "remove"
            i = bisect.bisect(edges, x)
            assert edges[i-1] == x
            del(edges[i-1])
        
    assert len(edges) == 0

    print(f"area = {total}")


# day18b(test18)
day18b(input18)
