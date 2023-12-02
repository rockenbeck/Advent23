import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input1 import *

def day1a(s):
    total = 0
    for line in s.split('\n'):
        while not line[0].isdigit():
            line = line[1:]
        while not line[-1].isdigit():
            line = line[:-1]
        sNum = line[0] + line[-1]
        total += int(sNum)
    print(total)

test1 = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

#day1a(input1)

digits = {'zero':0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9,
          '0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9}

def digitStart(s):
    for (sDigit,n) in digits.items():
        if s.startswith(sDigit):
            return n
    return None

def digitEnd(s):
    for (sDigit,n) in digits.items():
        if s.endswith(sDigit):
            return n
    return None

def day1b(s):
    total = 0
    for line in s.split('\n'):
        while digitStart(line) is None:
            line = line[1:]
        while digitEnd(line) is None:
            line = line[:-1]
        total += 10 * digitStart(line) + digitEnd(line)
    print(total)

test1b="""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

# day1b(input1)

