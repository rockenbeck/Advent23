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

class Comp:
    def __init__(self, name) -> None:
        self.name = name
        self.edges = [] # one-sided
        self.edgesAll = [] # both sides

    def __repr__(self) -> str:
        return repr((self.name))

    def getGroup(self):
        if self.group:
            group = self.group.getGroup()
            self.group = group
            return group
        return self

def countGroups(comps, exclude = []):
    # Faster to just do DFS from each component?

    for comp in comps.values():
        comp.group = None
        comp.cInGroup = 1

    for comp in comps.values():
        group = comp.getGroup()

        for other in comp.edges:
            if (comp, other) in exclude:
                continue

            groupOther = other.getGroup()

            if groupOther != group:
                groupOther.group = group
                group.cInGroup += groupOther.cInGroup

    groups = []
    for comp in comps.values():
        if comp.group == None:
            groups.append(comp.cInGroup)

    return groups

#                 ntq: p=14, ND=1, L=9, H=14, edges=[jqt, hfx, bvb, xhk]
#               hfx: p=13, ND=2, L=9, H=14, edges=[xhk, rhn, bvb, pzl, ntq]
#             xhk: p=12, ND=3, L=9, H=14, edges=[jqt, hfx, rhn, bvb, ntq]
#           jqt: p=11, ND=4, L=9, H=14, edges=[rhn, xhk, nvd, ntq]
#         rhn: p=10, ND=5, L=9, H=14, edges=[jqt, xhk, bvb, hfx]
#       bvb: p=9, ND=6, L=2, H=14, edges=[cmg, rhn, xhk, hfx, ntq]
#                 lsr: p=8, ND=1, L=0, H=8, edges=[rsh, pzl, lhk, rzs, frs]
#               lhk: p=7, ND=2, L=0, H=8, edges=[cmg, nvd, lsr, frs]
#             frs: p=6, ND=3, L=0, H=8, edges=[rsh, qnr, lhk, lsr]
#           rsh: p=5, ND=4, L=0, H=8, edges=[frs, pzl, lsr, rzs]
#         pzl: p=4, ND=5, L=0, H=8, edges=[rsh, lsr, hfx, nvd]
#       nvd: p=3, ND=6, L=0, H=8, edges=[jqt, cmg, pzl, qnr, lhk]
#     cmg: p=2, ND=13, L=0, H=14, edges=[qnr, nvd, lhk, bvb, rzs]
#   qnr: p=1, ND=14, L=0, H=14, edges=[cmg, nvd, rzs, frs]
# rzs: p=0, ND=15, L=0, H=14, edges=[qnr, cmg, lsr, rsh]

def addPreorderRecursive(comp, exclude, postorder, parent=None, n=0):
    comp.preorder = n
    comp.parent = parent
    n += 1
    comp.ND = 1
    comp.edgesF = []
    comp.edgesExtra = []
    for other in comp.edgesAll:
        if other == comp.parent or (comp,other) in exclude or (other,comp) in exclude:
            continue
        if other.preorder != None: # already visited
            comp.edgesExtra.append(other)
            continue
        comp.edgesF.append(other)
        n = addPreorderRecursive(other, exclude, postorder, comp, n)
        comp.ND += other.ND
    postorder.append(comp)
    return n

def addPreorderNonRecursive(comp, exclude, postorder):
    stack = []
    state = 0

    parent = None
    n = 0

    while True:
        if state == 0:
            comp.preorder = n
            comp.parent = parent
            n += 1
            comp.ND = 1
            comp.edgesF = []
            comp.edgesExtra = []
            i = 0
            state = 1
        if state == 1:
            if i >= len(comp.edgesAll):
                state = 4
            else:
                other = comp.edgesAll[i]
                if other == comp.parent or (comp,other) in exclude or (other,comp) in exclude:
                    state = 3
                elif other.preorder != None: # already visited
                    comp.edgesExtra.append(other)
                    state = 3
                else:
                    comp.edgesF.append(other)

                    # n = addPreorderRecursive(other, exclude, comp, n)
                    stack.append((comp, parent, other, i))
                    parent = comp
                    comp = other
                    state = 0
            continue
        if state == 2:
            comp.ND += other.ND
            state = 3
        if state == 3:
            i += 1
            state = 1
            continue
        if state == 4:
            postorder.append(comp)
            if len(stack) == 0:
                return n
            comp,parent,other,i = stack.pop(-1)
            state = 2
            continue

def tarjanRecursive(comp, exclude, indent=None):
    L = comp.preorder
    H = comp.preorder
    for other in comp.edgesF:
        tarjanRecursive(other, exclude, None if indent==None else indent + "  ")
        L = min(L, other.L)
        H = max(H, other.H)
    for other in comp.edgesExtra:
        L = min(L, other.preorder)
        H = max(H, other.preorder)
    comp.L = L
    comp.H = H
    if indent != None:
        print(f"{indent}{comp.name}: p={comp.preorder}, ND={comp.ND}, L={comp.L}, H={comp.H}, edges={comp.edgesAll}")

def tarjan(comps, exclude, trace=False):
    # Tarjan's bridge-finding algorithm via https://en.wikipedia.org/wiki/Bridge_(graph_theory)

    for comp in comps.values():
        comp.preorder = None # clear "visited"

    rootF = comp
    postorder = []

    # n = addPreorderRecursive(rootF, exclude, postorder)
    n = addPreorderNonRecursive(rootF, exclude, postorder)

    assert n == len(comps) # fully connected to begin with

    # tarjanRecursive(rootF, exclude, "" if trace else None)
    for comp in postorder:
        L = comp.preorder
        H = comp.preorder
        for other in comp.edgesF:
            L = min(L, other.L)
            H = max(H, other.H)
        for other in comp.edgesExtra:
            L = min(L, other.preorder)
            H = max(H, other.preorder)
        comp.L = L
        comp.H = H

    bridges = []
    for w in comps.values():
        v = w.parent
        if v == None:
            continue
        if w.L == w.preorder and w.H < w.preorder + w.ND:
            bridges.append((v, w))
            print(f"bridge from {v.name} to {w.name}")

    return bridges

def day25(sIn):

    comps = {}

    for line in sIn.split('\n'):
        name, sconn = line.split(': ')
        if name not in comps:
            comps[name] = Comp(name)
        
        for name in sconn.split(' '):
            if name not in comps:
                comps[name] = Comp(name)
    
    for line in sIn.split('\n'):
        name, sconn = line.split(': ')
        comp = comps[name]
        
        for nameOther in sconn.split(' '):
            other = comps[nameOther]
            # assert other not in comp.edges
            comp.edges.append(other)

            comp.edgesAll.append(other)
            other.edgesAll.append(comp)

    print(f"groups init = {len(countGroups(comps))}")

    edges = []
    for comp in comps.values():
        for other in comp.edges:
            edges.append((comp, other))

    cEdge = len(edges)
    for i in range(0,cEdge):
        # print(f"i = {i}/{cEdge}")
        for j in range(i + 1, cEdge):
            exclude = []
            exclude.append(edges[i])
            exclude.append(edges[j])
            bridges = tarjan(comps, exclude)

            if j % 10 == 0:
                print(f"i = {i},{j}/{cEdge}, {i*cEdge+j}/{cEdge**2}, bridges = {len(bridges)}")

            if len(bridges) == 0:
                continue

            exclude.append(bridges[0])
            cg = countGroups(comps, exclude)
            assert len(cg) == 2
            print(f"exclude {exclude} => 2 groups = {cg}")
            a,b = cg
            print(f"sizes = {a} * {b} = {a*b}")
            return


# day25(test25)
day25(input25)