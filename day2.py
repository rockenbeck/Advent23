
import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input2 import *

test2="""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

def day2a(s):
    total = 0
    limits = {'red':12, 'green':13, 'blue':14}
    for line in s.split('\n'):
        (sGame, sColon, sPulls) = line.partition(':')
        fOk = True
        for sPull in sPulls.split(";"):
            for pair in sPull.split(','):
                (sN, sSpace, sColor) = pair.strip().partition(' ')
                # print(int(sN), sColor)
                if int(sN) > limits[sColor]:
                    fOk = False
        if fOk:
            nGame = int(sGame.partition(' ')[2])
            total += nGame
    print(total)

# day2a(input2)

def day2b(s):
    total = 0
    for line in s.split('\n'):
        maxes = defaultdict(int)
        (sGame, sColon, sPulls) = line.partition(':')
        for sPull in sPulls.split(";"):
            for pair in sPull.split(','):
                (sN, sSpace, sColor) = pair.strip().partition(' ')
                # print(int(sN), sColor)
                n = int(sN)
                if n > maxes[sColor]:
                    maxes[sColor] = n
        nGame = int(sGame.partition(' ')[2])
        power = maxes['red'] * maxes['green'] * maxes['blue']
        total += power
    print(total)

day2b(input2)
