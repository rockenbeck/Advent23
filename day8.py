
import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input8 import *

test8a="""RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

test8b="""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

test8c="""LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

class Node:
    def __init__(self, s):
        global mpSNode
        self.s, self.sLeft, self.sRight = re.findall("[A-Z0-9]+", s)

    def __repr__(self):
        return repr((self.s, self.sLeft, self.sRight))


def day8a(sIn):
    mpSNode = {}
    lines = list(sIn.split('\n'))
    inst = lines[0]
    for line in lines[2:]:
        node = Node(line)
        mpSNode[node.s] = node
        
    node = mpSNode['AAA']

    c = 0

    while True:
        for ch in inst:
            c += 1
            if ch == 'R':
                node = mpSNode[node.sRight]
            else:
                assert(ch == 'L')
                node = mpSNode[node.sLeft]
            if node.s == 'ZZZ':
                print(c)
                return
        
# day8a(input8)


def day8b(sIn):
    mpSNode = {}
    lines = list(sIn.split('\n'))
    inst = lines[0]
    for line in lines[2:]:
        node = Node(line)
        mpSNode[node.s] = node
    
    nodes = []
    for node in mpSNode.values():
        if node.s[2] == 'A':
            nodes.append(node)
    
    c = 0

    loop = 0
    # cStart = 0
    # for ch in inst:
    #     cStart += 1
    #     if ch == 'R':
    #         nodes = list(map(lambda node: mpSNode[node.sRight], nodes))
    #     else:
    #         assert(ch == 'L')
    #         nodes = list(map(lambda node: mpSNode[node.sLeft], nodes))
        
    #     allZ = True
    #     for i in range(0,len(nodes)):
    #         node = nodes[i]
    #         if node.s[2] != 'Z':
    #             allZ = False

    #     if allZ:
    #         print(cStart)
    #         return
    
    nodesInit = nodes[:]
    # print(nodesInit)
 
    mpNodeCRepeat = {}

    mpINodeLoop = {}

    mpIRepd = [False] * len(nodes)
    mpICZ = [0] * len(nodes)
    mpIZPrev = [0] * len(nodes)

    while True:
        # for i in range(0,len(nodes)):
        #     if (i,nodes[i]) in mpINodeLoop:
        #         if not mpIRepd[i]:
        #             loopStart = mpINodeLoop[(i,nodes[i])]
        #             print(f"node {i} repeats at loop {loop} with len {loop - loopStart} and {mpICZ[i]} Zs")
        #             mpIRepd[i] = True
        #     else:
        #         mpINodeLoop[(i,nodes[i])] = loop
        for ch in inst:
            # print(list(nodes))
            c += 1
            if ch == 'R':
                nodes = list(map(lambda node: mpSNode[node.sRight], nodes))
            else:
                assert(ch == 'L')
                nodes = list(map(lambda node: mpSNode[node.sLeft], nodes))
            
            allZ = True
            for i in range(0,len(nodes)):
                node = nodes[i]
                if node.s[2] == 'Z':
                    diff = c - mpIZPrev[i]
                    print(f"{i}: c {c} mod {diff} = {c % diff}")
                    #print(f"{nodesInit[i]} leads to {node}")
                    mpIZPrev[i] = c
                else:
                    allZ = False

            if allZ:
                print(c)
                return
        loop += 1
        
# day8b(input8)
# day8b(test8c)

# running above code leads to the surprising result:
# 0: c 134037 mod 14893 = 0
# 1: c 119706 mod 19951 = 0
# 2: c 133194 mod 22199 = 0
# 3: c 132632 mod 16579 = 0
# 4: c 119987 mod 17141 = 0
# 5: c 120830 mod 12083 = 0
# It seems to me this won't be true in general, but only for the specific topology of these examples,
#  where when **A leads to **Z in exactly the length of the instructions, and, both a and z have the
#   same exit nodes so you get a nice repeating loop

def Gcd2(a, b):
    if a == 0:
        return b
    return Gcd2(b % a, a) # BB do this without recursion

def Gcd(lN):
    g = lN[0]
    for n in lN[1:]:
        g = Gcd2(g, n)
    return g

# print(Gcd((9, 12, 120)))
cycles = [14893,19951,22199,16579,17141,12083]
# print(Gcd(cycles)) == 281 == loop length, of course
print(list(map(lambda n: int(n/281), cycles)))

# since loop lengths are all relatively prime (also a surprising coincidence),
#  all we need is the product

def product(l):
    p = 1
    for n in l:
        p *= n
    return p

print(product(list(map(lambda n: int(n/281), cycles))) * 281)

# I find this fairly unsatisfying