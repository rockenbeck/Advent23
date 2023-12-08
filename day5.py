
import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input5 import *

def readMap(lines, iLine):
    mp = []
    while iLine < len(lines) and len(lines[iLine]) != 0:
        mp.append(list(map(int, lines[iLine].split(' '))))
        iLine += 1

    return iLine, mp

def applyMap(mp, n):
    for (dst, src, c) in mp:
        if n >= src and n < src + c:
            return n - src + dst
    return n

def applyMapToRange(mp, rs):
    rsIn = rs[:]
    rsOut = []

    while len(rsIn):
        nMin,nMax = rsIn[-1]
        del rsIn[-1]

        found = False
        for (dst, src, c) in mp:
            if nMax > src and nMin < src + c:
                if nMin < src:
                    rsIn.append((nMin, src))
                    nMin = src
                if nMax > src + c:
                    rsIn.append((src + c, nMax))
                    nMax = src + c
                rsOut.append((nMin - src + dst, nMax - src + dst))
                found = True
                break

        if not found:
            rsOut.append((nMin, nMax))

    return rsOut

def day5a(sInput):
    lines = sInput.split('\n')
    sSeeds = lines[0].partition(':')[2]
    seeds = list(map(int, re.findall("\d+", sSeeds)))
    # print(list(seeds))

    iLine = 3
    iLine, mpS2S = readMap(lines, iLine)
    # print(mpS2S)

    iLine += 2
    iLine, mpS2F = readMap(lines, iLine)

    iLine += 2
    iLine, mpF2W = readMap(lines, iLine)

    iLine += 2
    iLine, mpW2L = readMap(lines, iLine)

    iLine += 2
    iLine, mpL2T = readMap(lines, iLine)

    iLine += 2
    iLine, mpT2H = readMap(lines, iLine)

    iLine += 2
    iLine, mpH2L = readMap(lines, iLine)

    fA = False

    closest = 10000000000

    if fA:
        for n in seeds:
            n = applyMap(mpS2S, n)
            n = applyMap(mpS2F, n)
            n = applyMap(mpF2W, n)
            n = applyMap(mpW2L, n)
            n = applyMap(mpL2T, n)
            n = applyMap(mpT2H, n)
            n = applyMap(mpH2L, n)
            closest = min(closest, n)
    else:
        for i in range(0, len(seeds), 2):
            rs = [(seeds[i], seeds[i] + seeds[i + 1])]
            for mp in [mpS2S, mpS2F, mpF2W, mpW2L, mpL2T, mpT2H, mpH2L]:
                rs = applyMapToRange(mp, rs)
            for r in rs:
                closest = min(closest, r[0])

    print(f"closest = {closest}")

day5a(input5)