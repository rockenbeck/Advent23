
import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input10 import *

test10="""-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

test10b="""7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

def follow(mp, pos, posPrev):
    ch = mp[pos]

    posW = (pos[0] - 1, pos[1])
    posE = (pos[0] + 1, pos[1])
    posN = (pos[0], pos[1] - 1)
    posS = (pos[0], pos[1] + 1)

    if ch == '|':
        posA = posN
        posB = posS
    elif ch == '-':
        posA = posW
        posB = posE
    elif ch == 'L':
        posA = posN
        posB = posE
    elif ch == 'J':
        posA = posN
        posB = posW
    elif ch == '7':
        posA = posW
        posB = posS
    elif ch == 'F':
        posA = posE
        posB = posS
    else:
        return None
        
    if posPrev == posA:
        return posB
    elif posPrev == posB:
        return posA
    else:
        return None

test10c="""FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

def day10(sIn):
    mp = defaultdict(lambda : '.')

    y = 0
    for line in sIn.split('\n'):
        x = 0
        for ch in line:
            mp[(x,y)] = ch
            if ch == 'S':
                posStart = (x,y)
            x += 1
        y += 1

    xMax = x
    yMax = y

    len = 0

    posW = (posStart[0] - 1, posStart[1])
    posE = (posStart[0] + 1, posStart[1])
    posN = (posStart[0], posStart[1] - 1)
    posS = (posStart[0], posStart[1] + 1)

    pos = None
    for posNext in [posW, posE, posN, posS]:
        if follow(mp, posNext, posStart) != None:
            pos = posNext
            break
    assert(posNext != None)

    fN = follow(mp, posN, posStart) != None
    fS = follow(mp, posS, posStart) != None
    fE = follow(mp, posE, posStart) != None
    fW = follow(mp, posW, posStart) != None
    

    if fN and fS:
        mp[posStart] = '|'
    elif fE and fW:
        mp[posStart] = '-'
    elif fN and fE:
        mp[posStart] = 'L'
    elif fN and fW:
        mp[posStart] = 'J'
    elif fW and fS:
        mp[posStart] = '7'
    elif fE and fS:
        mp[posStart] = 'F'

    edge = set()
    edge.add(posStart)

    posPrev = posStart
    len = 1
    while pos != posStart:
        edge.add(pos)
        posNext = follow(mp, pos, posPrev)
        len += 1
        posPrev = pos
        pos = posNext

    print(f"len = {len}, maxdist = {len//2}")

    area = 0
    sDebug = ""
    for y in range(0,yMax):
        fIn = False
        for x in range(0,xMax):
            ch = mp[(x,y)]
            if (x,y) in edge:
                if ch == '|':
                    fIn = not fIn
                elif ch == 'L' or ch == 'F':
                    chFirst = ch
                elif ch == '7':
                    if chFirst == 'L':
                        fIn = not fIn
                elif ch == 'J':
                    if chFirst == 'F':
                        fIn = not fIn
            else:
                if fIn:
                    area += 1
                    ch = "I"
                else:
                    ch = '.'
            sDebug += ch
        sDebug += '\n'

    # print(sDebug)
    
    print(f"area = {area}")

# day10(test10)
# day10(test10b)
# day10(input10)

test10d = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

test10e = """..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
.........."""

day10(input10)