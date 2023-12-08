
import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input7 import *

test7="""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

def nCardRank(ch):
    # order = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    order = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
    return order.index(ch)

class Hand:
    def __init__(self, s):

        self.s = s

        aCh = sorted(list(s))

        mpChC = defaultdict(lambda: 0)
        for ch in aCh:
            mpChC[ch] = mpChC[ch] + 1

        if mpChC['J'] > 0 and mpChC['J'] < 5:
            cMax = 0
            for (ch,c) in mpChC.items():
                if ch != 'J' and c > cMax:
                    chMax = ch
                    cMax = c
            aCh = sorted(list(s.replace('J', chMax)))

        eq01 = aCh[0] == aCh[1]
        eq12 = aCh[1] == aCh[2]
        eq23 = aCh[2] == aCh[3]
        eq34 = aCh[3] == aCh[4]
        
        if eq01 and eq12 and eq23 and eq34:
            type = 0 # five of a kind
        elif (eq01 and eq12 and eq23) or (eq12 and eq23 and eq34):
            type = 1 # four of a kind
        elif (eq01 and eq12 and eq34) or (eq01 and eq23 and eq34):
            type = 2 # full house
        elif (eq01 and eq12) or (eq12 and eq23) or (eq23 and eq34):
            type = 3 # three of a kind
        elif (eq01 and (eq23 or eq34)) or (eq12 and eq34):
             type = 4 # two pair
        elif eq01 or eq12 or eq23 or eq34:
             type = 5 # one pair
        else:
             type = 6 # high card

        self.key = [type] + list(map(nCardRank, list(s)))

    def __repr__(self):
        return repr((self.s, self.key))

def day7a(sIn):
    hands = []
    for line in sIn.split('\n'):
        sHand,sBid = line.split(' ')
        # print(sHand, sBid)

        hands.append((Hand(sHand), int(sBid)))

    hands.sort(key=lambda p: p[0].key, reverse=True)   
    # print(hands)

    total = 0
    for i in range(0,len(hands)):
        print(hands[i], i+1, hands[i][1])
        total += (i+1) * hands[i][1]

    print(total)

day7a(input7)