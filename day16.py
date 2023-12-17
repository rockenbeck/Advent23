import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input16 import *



def shootBeam(mp, xMax, yMax, x, y, dir, active):
    if x < 0 or x >= xMax or y < 0 or y >= yMax:
        return
    if (x,y,dir) in active:
        return
    active.add((x,y,dir))

    ch = mp[(x,y)]
    if dir == 'n':
        if ch == '.' or ch == '|':
            shootBeam(mp, xMax, yMax, x, y-1, dir, active)
        elif ch == '/':
            shootBeam(mp, xMax, yMax, x+1, y, 'e', active)
        elif ch == '\\':
            shootBeam(mp, xMax, yMax, x-1, y, 'w', active)
        else:
            assert ch == '-'
            shootBeam(mp, xMax, yMax, x+1, y, 'e', active)
            shootBeam(mp, xMax, yMax, x-1, y, 'w', active)
    elif dir == 's':
        if ch == '.' or ch == '|':
            shootBeam(mp, xMax, yMax, x, y+1, dir, active)
        elif ch == '/':
            shootBeam(mp, xMax, yMax, x-1, y, 'w', active)
        elif ch == '\\':
            shootBeam(mp, xMax, yMax, x+1, y, 'e', active)
        else:
            assert ch == '-'
            shootBeam(mp, xMax, yMax, x+1, y, 'e', active)
            shootBeam(mp, xMax, yMax, x-1, y, 'w', active)
    elif dir == 'e':
        if ch == '.' or ch == '-':
            shootBeam(mp, xMax, yMax, x+1, y, dir, active)
        elif ch == '/':
            shootBeam(mp, xMax, yMax, x, y-1, 'n', active)
        elif ch == '\\':
            shootBeam(mp, xMax, yMax, x, y+1, 's', active)
        else:
            assert ch == '|'
            shootBeam(mp, xMax, yMax, x, y-1, 'n', active)
            shootBeam(mp, xMax, yMax, x, y+1, 's', active)
    else:
        assert dir == 'w'
        if ch == '.' or ch == '-':
            shootBeam(mp, xMax, yMax, x-1, y, dir, active)
        elif ch == '/':
            shootBeam(mp, xMax, yMax, x, y+1, 's', active)
        elif ch == '\\':
            shootBeam(mp, xMax, yMax, x, y-1, 'n', active)
        else:
            assert ch == '|'
            shootBeam(mp, xMax, yMax, x, y-1, 'n', active)
            shootBeam(mp, xMax, yMax, x, y+1, 's', active)
        


def shootBeam2(mp, xMax, yMax, x, y, dir, active):
    while True:
        if x < 0 or x >= xMax or y < 0 or y >= yMax:
            return
        if (x,y,dir) in active:
            return
        active.add((x,y,dir))

        ch = mp[(x,y)]
        if dir == 'n':
            if ch == '.' or ch == '|':
                y -= 1
            elif ch == '/':
                x += 1
                dir = 'e'
            elif ch == '\\':
                x -= 1
                dir = 'w'
            else:
                assert ch == '-'
                shootBeam2(mp, xMax, yMax, x+1, y, 'e', active)
                x -= 1
                dir = 'w'
        elif dir == 's':
            if ch == '.' or ch == '|':
                y += 1
            elif ch == '/':
                x -= 1
                dir = 'w'
            elif ch == '\\':
                x += 1
                dir = 'e'
            else:
                assert ch == '-'
                shootBeam2(mp, xMax, yMax, x-1, y, 'w', active)
                x += 1
                dir = 'e'
        elif dir == 'e':
            if ch == '.' or ch == '-':
                x += 1
            elif ch == '/':
                y -= 1
                dir = 'n'
            elif ch == '\\':
                y += 1
                dir = 's'
            else:
                assert ch == '|'
                shootBeam2(mp, xMax, yMax, x, y-1, 'n', active)
                y += 1
                dir = 's'
        else:
            assert dir == 'w'
            if ch == '.' or ch == '-':
                x -= 1
            elif ch == '/':
                y += 1
                dir = 's'
            elif ch == '\\':
                y -= 1
                dir = 'n'
            else:
                assert ch == '|'
                shootBeam2(mp, xMax, yMax, x, y+1, 's', active)
                y -= 1
                dir = 'n'
            



def day16(sIn):
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

    total = 0

    starts = []
    starts += map(lambda x: (x,0,'s'), range(0,xMax))
    starts += map(lambda x: (x,yMax-1,'n'), range(0,xMax))
    starts += map(lambda y: (0,y,'e'), range(0,yMax))
    starts += map(lambda y: (xMax-1,y,'w'), range(0,yMax))

    for start in starts:
            
        active = set()
        shootBeam2(mp, xMax, yMax, start[0], start[1], start[2], active)

        all = set()
        for x,y,dir in active:
            all.add((x,y))

        # s = ""
        # for y in range(0,yMax):
        #     for x in range(0,xMax):
        #         if mp[(x,y)] != '.':
        #             s += mp[(x,y)]
        #         else:
        #             dirs = []
        #             for dir in ['n', 's', 'e', 'w']:
        #                 if (x,y,dir) in active:
        #                     dirs.append(dir)
        #             if len(dirs) == 0:
        #                 s += '.'
        #             elif len(dirs) == 1:
        #                 s += dirs[0]
        #             else:
        #                 s += str(len(dirs))
        #     s += '\n'
        # print(s)

        on = len(all)
        total = max(on, total)
        
        # print(f"on = {len(all)}")

    print(f"best = {total}")


# day16(test16)
day16(input16)