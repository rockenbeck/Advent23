import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input12 import *

test12="""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

def cGroupsA(sSprings, groups):
    # Original code for Part One

    if len(sSprings) == 0:
        if len(groups) > 0:
            return 0
        return 1
    if sSprings[0] == '.':
        return cGroupsA(sSprings[1:], groups)
    if len(groups) == 0:
        for ch in sSprings:
            if ch == '#':
                return 0
        return 1
    if sum(groups) + len(groups) > len(sSprings):
        return 0
    
    cCh = groups[0]
    fOk = True
    for i in range(1,cCh):
        if sSprings[i] == '.':
            fOk = False
            break
    if sSprings[cCh] == '#':
        fOk = False
    cAtStart = 0 if not fOk else cGroupsA(sSprings[cCh+1:], groups[1:])
    if sSprings[0] == '#':
        return cAtStart
    assert sSprings[0] == '?'
    return cAtStart + cGroupsA(sSprings[1:], groups)


def cGroups(s, ls, groups, lg, mp):
    # How many ways can you make the first ls chars of s with the first lg groups in groups?
    # Faster code with cached counts for sub-problems, for Part Two

    if ls == 0:
        return 0 if lg > 0 else 1
    if lg == 0:
        return 0 if '#' in s[0:ls] else 1
    if sum(groups[0:lg]) + lg > ls:
        return 0
    
    # if we've already computed this result, just return it

    if (ls,lg) in mp:
        return mp[(ls,lg)]
    
    c = 0

    # consume . or ? by skipping it

    if s[ls-1] != '#':
        c += cGroups(s, ls - 1, groups, lg, mp)
    
    # consume # or ? by matching first group

    if s[ls-1] != '.':
        cCh = groups[lg-1]
        if ls > cCh:
            if '.' not in s[ls-cCh:ls-1] and s[ls-cCh-1] != '#':
                c += cGroups(s, ls-cCh-1, groups, lg-1, mp)

    # cache result

    mp[(ls,lg)] = c

    return c


def day12(sIn):
    total = 0
    for line in sIn.split('\n'):
        # parse
        sSprings,sGroups = line.split(' ')
        groups=list(map(int, sGroups.split(',')))

        B = True
        if B:
            sSprings = "?".join([sSprings] * 5)
            groups = groups * 5

        # remove leading and trailing '.' and add one more as a sentinel
        #  at each end so we don't have to check some ranges

        while sSprings[0] == '.':
            sSprings = sSprings[1:]
        sSprings = '.' + sSprings
        while sSprings[-1] == '.':
            sSprings = sSprings[:-1]
        sSprings = sSprings + '.'
        
        c = cGroups(sSprings, len(sSprings), groups, len(groups), {})

        total += c

    print(f"total = {total}")

# day12(test12)
day12(input12)