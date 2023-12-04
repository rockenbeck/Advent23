
import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input4 import *

test4="""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

def day4a(sFile):
    total = 0
    for line in sFile.split('\n'):
        (sWin, sHave) = line.split(':')[1].split('|')
        
        win = set()
        for s3 in re.findall("\d+", sWin):
            win.add(int(s3))

        points = 0
        for s4 in re.findall("\d+", sHave):
            if int(s4) in win:
                points = 1 if points == 0 else points * 2

        total += points

    print(f"total = {total}")

day4a(input4)

def day4b(sFile):
    total = 0
    mpCardCopies = defaultdict(lambda: 1)

    iCard = 1
    for line in sFile.split('\n'):
        cCard = mpCardCopies[iCard]
        total += cCard

        (sWin, sHave) = line.split(':')[1].split('|')
        win = set()
        for s3 in re.findall("\d+", sWin):
            win.add(int(s3))
        
        matches = 0
        for s4 in re.findall("\d+", sHave):
            if int(s4) in win:
                matches += 1

        for next in range(iCard + 1, iCard + matches + 1):
            mpCardCopies[next] = mpCardCopies[next] + cCard
        
        iCard += 1

    print(f"total = {total}")

day4b(input4)