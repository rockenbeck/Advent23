import re
from collections import defaultdict
from collections import deque
import sys
import random
import math
import numpy as np
import heapq
import bisect 

from input25 import *

test25="""jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""

def getGroup(mp, name):
    if name not in mp:
        return name
    group = getGroup(mp, mp[name])
    mp[name] = group
    return group

def countGroups(comps, exclude = []):
    mp = {} # name => name of component in same group

    for name,lother in comps.items():
        group = getGroup(mp, name)

        for nameOther in lother:
            if (name, nameOther) in exclude:
                continue

            groupOther = getGroup(mp, nameOther)

            if groupOther != group:
                mp[groupOther] = group

    groups = defaultdict(lambda : 0)
    for name in comps.keys():
        group = name
        while group in mp:
            group = mp[group]
        groups[group] = groups[group] + 1

    return groups
            

def day25(sIn):

    comps = {}

    conns = defaultdict(lambda:0)

    for line in sIn.split('\n'):
        name, sconn = line.split(': ')
        if name not in comps:
            comps[name] = []
        
        for name in sconn.split(' '):
            if name not in comps:
                comps[name] = []
    
    for line in sIn.split('\n'):
        name, sconn = line.split(': ')
        l = comps[name]
        
        for nameOther in sconn.split(' '):
            assert nameOther not in l
            l.append(nameOther)

            conns[name] = conns[name] + 1
            conns[nameOther] = conns[nameOther] + 1

            # lOther = comps[nameOther]
            # assert name not in lOther
            # lOther.append(name)

    print(f"groups init = {len(countGroups(comps))}")

    for name,c in conns.items():
        if c < 4:
            print(f"component {name} has {c} edges")

    edges = []
    for name,lother in comps.items():
        for nameOther in lother:
            edges.append((name, nameOther))

    for i in range(0,len(edges)):
        # print(f"i = {i}/{len(edges)}")
        for j in range(i + 1, len(edges)):
            exclude = set()
            exclude.add(edges[i])
            exclude.add(edges[j])
            cgij = countGroups(comps,exclude)
            print(f"i = {i}/{len(edges)}, j = {j}/{len(edges)}, groups after removing 2 = {len(cgij)}")

            for k in range(j + 1, len(edges)):
                exclude.add(edges[k])
                cg = countGroups(comps, exclude)
                if len(cg) == 2:
                    print(f"exclude {exclude} => 2 groups = {cg}")
                    a,b = list(cg.values())
                    print(f"sizes = {a} * {b} = {a*b}")
                    return
                exclude.remove(edges[k])


# day25(test25)
day25(input25)