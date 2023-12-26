import re
from collections import defaultdict
from collections import deque
import sys
import random
import math
import numpy as np
import heapq
import bisect 

from input23 import *

test23="""#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

def day23(sIn):
    mp = {}

    yStart = 0
    
    yMax = len(sIn.split('\n'))
    y = 0
    for line in sIn.split('\n'):
        x = 0
        for ch in line:
            mp[(x,y)] = ch
            if y == 0 and ch == '.':
                xStart = x
            if y == yMax - 1 and ch == '.':
                xEnd = x
            x += 1
        y += 1

    xMax = x
    assert yMax == y
    yEnd = yMax - 1

    heap = []
    heap.append((0,xStart,yStart,[]))

    mpLongest = defaultdict(lambda : 1)

    while len(heap) > 0:
        l,x,y,path = heapq.heappop(heap)
        if l < mpLongest[(x,y)]:
            mpLongest[(x,y)] = l
        else:
            # continue
            pass # try 'em all
    
        if x == xEnd and y == yEnd:
            continue
        ch = mp[(x,y)]
        if ch == '.' or True:
            ds = [(0,1), (0,-1), (1,0), (-1,0)]
        elif ch == '<':
            ds = [(-1,0)]
        elif ch == '>':
            ds = [(1,0)]
        elif ch == '^':
            ds = [(0,-1)]
        else:
            assert ch == 'v'
            ds = [(0,1)]

        for dx,dy in ds:
            xT = x + dx
            yT = y + dy
            if yT < yStart:
                continue
            if mp[(xT,yT)] == '#':
                continue
            if (xT,yT) in path:
                continue
            heapq.heappush(heap, (l-1,xT,yT,path + [(xT,yT)]))

    print(f"longest = {-mpLongest[(xEnd,yEnd)]}")


# day23(test23)
# day23(input23)


def printPath(mp,path):
    xMax,yMax = 0,0
    for x,y in mp.keys():
        xMax = max(xMax,x+1)
        yMax = max(yMax,y+1)
    
    s = ""
    for y in range(0,yMax):
        for x in range(0,xMax):
            if (x,y) in path:
                s += 'O'
            else:
                s += mp[(x,y)]
        s += '\n'
    print(s)


def longestRecursive(mp,x,y,xEnd,yEnd,path):
    # OK for short, stack overflow for longer

    if x == xEnd and y == yEnd:
        lLongest = len(path)
    else:
        path.add((x,y))

        lLongest = -1
        d = 0
        while d < 4:
            dx,dy = [(0,1), (0,-1), (1,0), (-1,0)][d]
            xT = x + dx
            yT = y + dy
            if yT >= 0 and mp[(xT,yT)] != '#' and (xT,yT) not in path:
                l = longestRecursive(mp,xT,yT,xEnd,yEnd,path)
                if l > lLongest:
                    lLongest = l
            d += 1

        path.remove((x,y))

    return lLongest


def longestNonRecursive(mp,xStart,yStart,xEnd,yEnd,path):
    # no stack problems, fast, but not fast enough for large problem

    stack = []
    x,y = xStart,yStart
    d = 0

    next = {}

    n = 0
    while True:
        n += 1

        if d == 0 and x == xEnd and y == yEnd:
            lLongest = len(path)
        else:
            if d == 0:
                path.add((x,y))
                # print(f"{n}:\n")
                # printPath(mp,path)
                lLongest = -1

            cont = False
            while d < 4:
                dx,dy = [(0,1), (0,-1), (1,0), (-1,0)][d]
                xT = x + dx
                yT = y + dy
                if yT >= 0 and mp[(xT,yT)] != '#' and (xT,yT) not in path:
                    stack.append((x,y,d,lLongest))
                    x,y,d = xT,yT,0
                    cont = True
                    break
                d += 1
            if cont:
                continue
            path.remove((x,y))

        # return
        ret = False
        while True:
            if len(stack) == 0:
                ret = True
                break

            l = lLongest
            x,y,d,lLongest = stack.pop(-1)
            if l > lLongest:
                lLongest = l
                next[(x,y)] = d
            d += 1
            if d < 4:
                break

            path.remove((x,y))
            # print(f"{n}:\n")
            # printPath(mp,path)
            # ...

        if ret:
            break

    path = set()
    x,y = xStart,yStart
    while y != yEnd:
        path.add((x,y))
        d = next[(x,y)]
        dx,dy = [(0,1), (0,-1), (1,0), (-1,0)][d]
        x += dx
        y += dy

    return lLongest,path

def longestNonRecursive2(mp,xStart,yStart,xEnd,yEnd):
    # OK for short, stack overflow for longer
    # Is this cleaner? Kinda verbose. Trying to find a nice pattern for doing a manual stack

    path = set()
    stack = []
    x,y = xStart,yStart
    state = "enter"

    while True:
        if state == "enter":
            if x == xEnd and y == yEnd:
                lLongest = len(path)
                state = "return"
            else:
                path.add((x,y))
                lLongest = -1
                d = 0
                state = "loop1"
                # fall through
        if state == "loop1":
            dx,dy = [(0,1), (0,-1), (1,0), (-1,0)][d]
            xT = x + dx
            yT = y + dy
            if yT >= 0 and mp[(xT,yT)] != '#' and (xT,yT) not in path:
                stack.append((x,y,d,lLongest))
                x,y = xT,yT
                state = "enter"
                continue
            state = "loop2"
        if state == "loop2":
            d += 1
            if d < 4:
                state = "loop1"
                continue
            path.remove((x,y))
            state = "return"
        if state == "return":
            if len(stack) == 0:
                break

            l = lLongest
            x,y,d,lLongest = stack.pop(-1)
            if l > lLongest:
                lLongest = l
            state = "loop2"
                
    return lLongest



class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.edges = []

    def __repr__(self):
        return repr((self.x, self.y, list(map(lambda e: (e[0].x, e[0].y, e[1]), self.edges))))
    
def longestGraph(mp,xStart,yStart,xEnd,yEnd):
    # reduce map to graph, do exhaustive depth-first search on graph

    nodes = {}

    # find nodes

    for x,y in mp.keys():
        node = None
        if x == xStart and y == yStart:
            node = Node(x,y)
            nodeStart = node
        elif x == xEnd and y == yEnd:
            node = Node(x,y)
            nodeEnd = node
        elif mp[(x,y)] != '#':
            cAdj = 0
            for dx,dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                xT = x + dx
                yT = y + dy
                if mp[(xT,yT)] != '#':
                    cAdj += 1
            if cAdj > 2:
                node = Node(x,y)
        if node:
            nodes[(x,y)] = node

    print(f"Nodes:")
    printPath(mp,nodes)

    # build edges

    for node in nodes.values():
        x,y = node.x,node.y
        for dx,dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            xT = x + dx
            yT = y + dy
            if yT >= yStart and yT <= yEnd and mp[(xT,yT)] != '#':
                l = 1
                xPrev,yPrev = x,y
                foundNode = False
                while True:
                    if (xT,yT) in nodes:
                        nodeT = nodes[(xT,yT)]
                        node.edges.append((nodeT, l))
                        # BB better to add both ends of edge here?
                        break

                    xNext,yNext = None,None
                    for dxT,dyT in [(0,1), (0,-1), (1,0), (-1,0)]:
                        x2 = xT + dxT
                        y2 = yT + dyT
                        if (x2,y2) != (xPrev,yPrev):
                            if y2 >= yStart and y2 <= yEnd and mp[(x2,y2)] != '#':
                                xNext,yNext = x2,y2
                                break
                    assert xNext != None
                    xPrev,yPrev = xT,yT
                    xT,yT = xNext,yNext
                    l += 1

    # search edges
    
    l = longestGraphRecursive(nodes,nodeStart,nodeEnd,set(),0)
    return l


def longestGraphRecursive(nodes,node,nodeEnd,path,l):
    if node == nodeEnd:
        lLongest = l
    else:
        path.add(node)

        lLongest = -1
        for nodeT,dl in node.edges:
            if nodeT not in path:
                lT = longestGraphRecursive(nodes,nodeT,nodeEnd,path,l + dl)
                if lT > lLongest:
                    lLongest = lT

        path.remove(node)

    return lLongest

def day23b(sIn):
    mp = {}

    yStart = 0
    
    yMax = len(sIn.split('\n'))
    y = 0
    for line in sIn.split('\n'):
        x = 0
        for ch in line:
            mp[(x,y)] = ch
            if y == 0 and ch == '.':
                xStart = x
            if y == yMax - 1 and ch == '.':
                xEnd = x
            x += 1
        y += 1

    xMax = x
    assert yMax == y
    yEnd = yMax - 1

    # l = longestRecursive(mp,xStart,yStart,xEnd,yEnd,set())
    # l,path = longestNonRecursive(mp,xStart,yStart,xEnd,yEnd,set())
    # printPath(mp,path)
    l = longestNonRecursive2(mp,xStart,yStart,xEnd,yEnd)
    # l = longestGraph(mp,xStart,yStart,xEnd,yEnd)

    print(f"longest = {l}")


            
day23b(test23)
# day23b(input23)


test23c="""#.#####
#.....#
#.....#
#..#..#
#.....#
#####.#"""

# day23b(test23c)
