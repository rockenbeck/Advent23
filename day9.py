
import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input9 import *

test9="""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

test9b="""1 3 -5"""

def day9(sIn):
    totalA = 0
    totalB = 0
    for line in sIn.split('\n'):
        seq = list(map(int, re.findall("-*\d+", line)))
        
        diffs = [seq]
        
        while True:
            diff = []
            for i in range(1,len(seq)):
                diff.append(seq[i] - seq[i-1])
            if sum(map(lambda n: 0 if n == 0 else 1, diff)) == 0:
                break
            diffs.append(diff)
            seq = diff

        nA = 0
        nB = 0
        for i in range(len(diffs) - 1, -1, -1):
            nA += diffs[i][-1]
            nB = diffs[i][0] - nB

        totalA += nA
        totalB += nB

    print(f"A={totalA} B={totalB}")


#day9(test9b)
day9(input9)
