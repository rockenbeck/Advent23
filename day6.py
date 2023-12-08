
import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

test6="""Time:      7  15   30
Distance:  9  40  200"""

input6="""Time:        51     92     68     90
Distance:   222   2031   1126   1225"""

input6b="""Time:        51926890
Distance:   222203111261225"""



def day6a(sInput):
    lines = sInput.split("\n")
    times = list(map(int, re.findall("\d+", lines[0].partition(":")[2])))
    dists = list(map(int, re.findall("\d+", lines[1].partition(":")[2])))
    # print(times, dists)

    total = 1
    for i in range(0,len(times)):
        t = times[i]
        d = dists[i]
        a = 1
        b = -t
        c = d+1
        r0 = (-b - math.sqrt(b*b-4*a*c))/(2*a)
        r1 = (-b + math.sqrt(b*b-4*a*c))/(2*a)
        print(r0,r1)
        ways = int(math.floor(r1)) - int(math.ceil(r0)) + 1
        total *= ways

    print(total)

day6a(input6b)



# t = 7
# d = 9

# d+1 = h + (t-h)*h = -h^2 + th
# a = 1
# b = -t
# c = d+1

# r = (-b +- sqrt(b*b - 4 * a * c))/2*a
