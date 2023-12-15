import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input15 import *

test15="""rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

def day15a(sIn):
    total = 0
    for s in sIn.split(','):
        h = 0
        for ch in s:
            a = ord(ch)
            h += a
            h *= 17
            h = h & 255
        # print(f"{s} becomes {h}")
        total += h
    print(f"total = {total}")

# day15a(test15)
day15a(input15)

def day15b(sIn):

    hashmap = []
    for i in range(0,256):
        hashmap.append([])

    for s in sIn.split(','):
        if s[-1] == '-':
            op = 0
            l = s[:-1]
        else:
            op = 1
            l,f = s.split('=')
            f = int(f)
            
        h = 0
        for ch in l:
            h = ((h + ord(ch)) * 17) & 255
        # print(f"{s} becomes {h}")

        b = hashmap[h]

        if op == 0:
            for i,p in enumerate(b):
                if p[0] == l:
                    del(b[i])
                    break
        else:
            found = False
            for i,p in enumerate(b):
                if p[0] == l:
                    b[i] = (l, f)
                    found = True
                    break

            if not found:
                b.append((l, f))

        # print(list(filter(lambda b: len(b) > 0, hashmap)))
        print(hashmap[0:4])

    total = 0
    for i in range(0,256):
        for j,p in enumerate(hashmap[i]):
            total += (i + 1) * (j + 1) * p[1]
    print(f"total = {total}")

# day15b(test15)
day15b(input15)