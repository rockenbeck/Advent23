import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input14 import *


test14="""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


def day14(sIn):
    # ought to wrap these in a mapify fn

    mp = {}

    y = 0
    for line in sIn.split('\n'):
        x = 0
        for ch in line:
            mp[(x,y)] = ch
            x += 1
        y += 1

    xMax = x
    yMax = y

    hist = {}

    for i in range(1,1000000):
        # roll north

        for x in range(0,xMax):
            yOpen = None
            for y in range(0,yMax):
                if mp[(x,y)] == '#':
                    yOpen = None
                else:
                    if yOpen == None:
                        yOpen = y
                    if mp[(x,y)] == 'O':
                        if yOpen < y:
                            mp[(x,yOpen)] = 'O'
                            mp[(x,y)] = '.'
                        yOpen += 1
        
        # roll west

        for y in range(0,yMax):
            xOpen = None
            for x in range(0,xMax):
                if mp[(x,y)] == '#':
                    xOpen = None
                else:
                    if xOpen == None:
                        xOpen = x
                    if mp[(x,y)] == 'O':
                        if xOpen < x:
                            mp[(xOpen,y)] = 'O'
                            mp[(x,y)] = '.'
                        xOpen += 1
        
        # roll south

        for x in range(0,xMax):
            yOpen = None
            for y in range(yMax-1,-1,-1):
                if mp[(x,y)] == '#':
                    yOpen = None
                else:
                    if yOpen == None:
                        yOpen = y
                    if mp[(x,y)] == 'O':
                        if yOpen > y:
                            mp[(x,yOpen)] = 'O'
                            mp[(x,y)] = '.'
                        yOpen -= 1
        
        # roll east

        for y in range(0,yMax):
            xOpen = None
            for x in range(xMax-1,-1,-1):
                if mp[(x,y)] == '#':
                    xOpen = None
                else:
                    if xOpen == None:
                        xOpen = x
                    if mp[(x,y)] == 'O':
                        if xOpen > x:
                            mp[(xOpen,y)] = 'O'
                            mp[(x,y)] = '.'
                        xOpen -= 1
        
        s = ""
        for y in range(0,yMax):
            for x in range(0,xMax):
                s += mp[(x,y)]
            s += '\n'
        # print(s)

        if s in hist:
            print(f"cycle from iter {i} to {hist[s]}")
            l = i - hist[s]
            print(f"iter 1000000000 same as iter {(1000000000 - hist[s]) % l + hist[s]}")
            return
        
        hist[s] = i

        total = 0
        for y in range(0,yMax):
            for x in range(0,xMax):
                if mp[(x,y)] == 'O':
                    # print(f"add {yMax - y}")
                    total += yMax - y

        print(f"total at iter {i} = {total}")

# day14(test14)
day14(input14)
