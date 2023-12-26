import re
from collections import defaultdict
from collections import deque
import sys
import random
import math
import numpy as np
import heapq
import bisect 

from input24 import *

test24="""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""


class Stone:
    def __init__(self, s):
        spos,sv =  s.split(" @ ")
        self.x,self.y,self.z = map(int, spos.split(", "))
        self.dx,self.dy,self.dz = map(int, sv.split(", "))

    def __repr__(self):
        return f"{(self.x, self.y, self.z)} {(self.dx, self.dy, self.dz)}"


def day24a(sIn,xMin,xMost):
    # simple part 1 solution

    stones = []
    
    for line in sIn.split('\n'):
        stones.append(Stone(line))

    # print(stones)
        
    yMin,yMost = xMin,xMost
    
    total = 0
    for i in range(0,len(stones)-1):
        stone0 = stones[i]
        N0 = (stone0.dy, -stone0.dx)
        dot0 = stone0.x * N0[0] + stone0.y * N0[1]
        for j in range(i + 1, len(stones)):
            stone1 = stones[j]

            # print(f"A: {stone0} B: {stone1}")

            # p = p1 + d1 * t
            # N0 o p = dot0
            # N0 o p1 + N0 o d1 * t = dot0
            # t = (dot0 - N0 o p1) / N0 o d1

            dot1 = stone1.x * N0[0] + stone1.y * N0[1]
            dotd1 = stone1.dx * N0[0] + stone1.dy * N0[1]
            if dotd1 == 0:
                # print("parallel")
                continue
        
            t1 = (dot0 - dot1) / dotd1

            if t1 < 0.0:
                # print(f"crossed earlier B {p}")
                continue

            p = (stone1.x + stone1.dx * t1, stone1.y + stone1.dy * t1)

            if stone0.dx != 0:
                t0 = (p[0] - stone0.x) / stone0.dx
            else:
                assert stone0.dy != 0
                t0 = (p[1] - stone0.y) / stone0.dy
            
            if t0 < 0.0:
                # print(f"crossed earlier A {p}")
                continue

            if p[0] >= xMin and p[0] <= xMost and p[1] >= yMin and p[1] <= yMost:
                # print(f"inside: {p}")
                total += 1
            else:
                # print(f"outside: {p}")
                ...

    print(f"total = {total}")

            

# day24a(test24,7,27)
# day24a(input24, 200000000000000.0, 400000000000000.0)


def day24b(sIn):
    # gather data about input, hoping to find simplifications

    stones = []
    
    for line in sIn.split('\n'):
        stones.append(Stone(line))

    for i in range(0,len(stones)-1):
        stone0 = stones[i]
        N0 = (stone0.dy, -stone0.dx)
        dot0 = stone0.x * N0[0] + stone0.y * N0[1]
        for j in range(i + 1, len(stones)):
            stone1 = stones[j]

            # print(f"A: {stone0}\nB: {stone1}")

            xc = stone0.dy * stone1.dz - stone0.dz * stone1.dy
            yc = stone0.dz * stone1.dx - stone0.dx * stone1.dz
            zc = stone0.dx * stone1.dy - stone0.dy * stone1.dx
            if xc == 0 and yc == 0 and zc == 0:
                print(f"{i} parallel to {j}")

            dotv01 = stone0.dx * stone1.dx + stone0.dy * stone1.dy + stone0.dz * stone1.dz
            if dotv01 == 0:
                print(f"{i} perpendicular to {j}")

            dotv00 = stone0.dx * stone0.dx + stone0.dy * stone0.dy + stone0.dz * stone0.dz
            dotv11 = stone1.dx * stone1.dx + stone1.dy * stone1.dy + stone1.dz * stone1.dz

            dp01 = (stone1.x - stone0.x, stone1.y - stone0.y, stone1.z - stone0.z)
            dotdv0 = dp01[0] * stone0.dx + dp01[1] * stone0.dy + dp01[2] * stone0.dz
            dotdv1 = dp01[0] * stone1.dx + dp01[1] * stone1.dy + dp01[2] * stone1.dz

            t0 = (dotv00 - dotdv0) / dotv01
            t1 = (dotv11 + dotdv1) / dotv01

            dp = (stone1.x + t1 * stone1.dx - (stone0.x + t0 * stone0.dx), \
                  stone1.y + t1 * stone1.dy - (stone0.y + t0 * stone0.dy), \
                  stone1.z + t1 * stone1.dz - (stone0.z + t0 * stone0.dz))
            s2 = dp[0] * dp[0] + dp[1] * dp[1] + dp[2] * dp[2]
            if s2 < 0.1:
                print(f"{i} meets {j}")

            # # p = p1 + d1 * t
            # # N0 o p = dot0
            # # N0 o p1 + N0 o d1 * t = dot0
            # # t = (dot0 - N0 o p1) / N0 o d1

            # dot1 = stone1.x * N0[0] + stone1.y * N0[1]
            # dotd1 = stone1.dx * N0[0] + stone1.dy * N0[1]
            # if dotd1 == 0:
            #     # print("parallel in xy")
            #     # assert False # not true for main input?
            #     ...
            # else:
            
            #     t1 = (dot0 - dot1) / dotd1

            #     p1 = (stone1.x + stone1.dx * t1, stone1.y + stone1.dy * t1, stone1.z + stone1.dz * t1)

            #     if stone0.dx != 0:
            #         t0 = (p1[0] - stone0.x) / stone0.dx
            #     else:
            #         assert stone0.dy != 0
            #         t0 = (p1[1] - stone0.y) / stone0.dy
                
            #     p0 = (stone0.x + stone0.dx * t0, stone0.y + stone0.dy * t0, stone0.z + stone0.dz * t0)

            #     if abs(p0[2] - p1[2]) < 0.01:
            #         print(f"{i} meets {j}")


def area2(stones, ts):

    stone0,stone1,stone2 = stones[0:3]

    t0,t1,t2 = ts

    p0 = (stone0.x + stone0.dx * t0, stone0.y + stone0.dy * t0, stone0.z + stone0.dz * t0)
    p1 = (stone1.x + stone1.dx * t1, stone1.y + stone1.dy * t1, stone1.z + stone1.dz * t1)
    p2 = (stone2.x + stone2.dx * t2, stone2.y + stone2.dy * t2, stone2.z + stone2.dz * t2)
    p01 = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
    p02 = (p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2])
    cross = (p01[1] * p02[2] - p01[2] * p02[1], \
                p01[2] * p02[0] - p01[0] * p02[2],  \
                p01[0] * p02[1] - p01[1] * p02[0])
    
    a2 = cross[0] * cross[0] + cross[1] * cross[1] + cross[2] * cross[2]
    # actually (area/2)^2
    # return a

    return math.sqrt(a2)

    # normalize by dividing by perimeter
    # p12 = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    # l01 = p01[0] * p01[0] + p01[1] * p01[1] + p01[2] * p01[2]
    # l02 = p02[0] * p02[0] + p02[1] * p02[1] + p02[2] * p02[2]
    # l12 = p12[0] * p12[0] + p12[1] * p12[1] + p12[2] * p12[2]
    # perim = l01 + l02 + l12
    # return 0 if perim == 0 else math.sqrt(a2) / perim

def normalize(vec):
    l = math.sqrt(sum(map(lambda n : n*n, vec)))
    if l == 0:
        norm = vec.copy()
    else:
        norm = list(map(lambda n : n/l, vec))
    return norm

def dot(veca, vecb):
    assert len(veca) == len(vecb)
    return sum(map(lambda i : veca[i] * vecb[i], range(0,len(veca))))

def dist2(veca, vecb):
    d = list(map(lambda i : vecb[i] - veca[i], range(0,len(veca))))
    return dot(d, d)

def dist(veca, vecb):
    return math.sqrt(dist2(veca, vecb))

def sts(ts):
    return ','.join(map(lambda t : f"{t:.4f}", ts))

def solve(scorer, context, tsInit, alg = "gradient descent", dtStep = .001):
    # generic multi-variable solver -- poorly suited for given problem
    # alg = "gradient descent"
    # alg = "axis descent"

    ts = tsInit.copy()

    if alg == "axis descent":
        # what's the real name of this algorithm (one axis/param at a time)?
        # finds min with t1 < 0; how to prevent that?
        # are there local mins != global min? seems that way

        a = scorer(context, ts)

        step = 0

        # while a > 0:
        while True:
            step += 1
            # choose axis
            dts = None
            aMin = None
            for i in range(0,len(ts)):
                for pm1 in [-dtStep,dtStep]:
                    tst = ts.copy()
                    tst[i] = ts[i] + pm1
                    aT = scorer(context, tst)
                    da = aT - a
                    if aMin == None or aT < aMin:
                        aMin = aT
                        dts = [0] * len(ts)
                        dts[i] = pm1

            # print(f"{step}: {sts(ts)} = {a:.6f} -> {sts(dts)}")
            print(f"{step}: {sts(ts)} = {a:.6f}")

            if aMin >= a:
                # local min? (or step too large)
                print(f"Local min")
                break

            # search for min along that axis

            # step in increasingly large steps in that direction until it starts going up

            p = 1
            while True:
                tst = [ts[i] + p * dts[i] for i in range(0,len(ts))]
                aT = scorer(context, tst)
                if aT >= a:
                    break

                a = aT
                ts = tst

                p *= 2
                assert p < 10000000000000000

    elif alg == "gradient descent":
        # fails to find min at 5,3,4 - why?
        # is triangle area wrong thing to minimize?
        # minimum might be near long, thin triangles
        # or multimple minima -- hard to grok shape of space

        a = scorer(context, ts)

        step = 0

        while True:
            # if a < .01:
            #     # local min? (or step too large)
            #     break

            step += 1

            # choose axis
            dts = [0] * len(ts)
            for i in range(0,len(ts)):
                tst = ts.copy()
                tst[i] = ts[i] + dtStep
                aPos = scorer(context, tst)
                tst[i] = ts[i] - dtStep
                aNeg = scorer(context, tst)
                da = aPos - aNeg
                dts[i] = -da

            dts = normalize(dts)

            # print(f"{step}: {sts(ts)} = {a:.6f} -> {sts(dts)}")
            print(f"{step}: {sts(ts)} = {a:.6f}")

            # search for min along that axis

            # step in increasingly large steps in that direction until it starts going up

            p = dtStep
            dec = False
            while True:
                tst = [ts[i] + p * dts[i] for i in range(0,len(ts))]
                aT = scorer(context, tst)
                if aT >= a:
                    break

                dec = True
                a = aT
                ts = tst

                p *= 2
                assert p < 10000000000000000

            if not dec:
                print(f"no decrease")
                break
                    
    # elif alg == "simplex":
    #     tss = [[0,0,0], [1,0,0], [0,1,0], [0,0,1]]
    #     areas = list(map(lambda ts: scorer(context, ts), tss))

    #     print(tss, areas)

    #     while True:
    #         ...

    return ts
        
def day24c(sIn):
    # solve in floats using solver - not well-suited

    stones = []
    
    for line in sIn.split('\n'):
        stones.append(Stone(line))

    # stones[0] = stones[3] # testing with different stones

    # tsInit = [0,0,0]
    # tsInit = [5,3,4] # does stay put, at least?
    tsInit = [4,2,5] # testing -- ends up not at 5,3,4, rather at 4.999000865239925, 2.229716171963779, 3.8080839453914073

    ts = solve(lambda stones, ts: area2(stones, ts), stones, tsInit)

    # given times, solve for x,y,z,dx,dy,dz

    stone0,stone1,stone2 = stones[0:3]
    t0,t1,t2 = ts
    p0 = (stone0.x + stone0.dx * t0, stone0.y + stone0.dy * t0, stone0.z + stone0.dz * t0)
    p1 = (stone1.x + stone1.dx * t1, stone1.y + stone1.dy * t1, stone1.z + stone1.dz * t1)
    p2 = (stone2.x + stone2.dx * t2, stone2.y + stone2.dy * t2, stone2.z + stone2.dz * t2)

    print(f"collide {stone0} at {t0} at {p0}")
    print(f"collide {stone1} at {t1} at {p1}")
    print(f"collide {stone2} at {t2} at {p2}")

    p01 = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
    p02 = (p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2])

    dt01 = t1 - t0
    # v = (p01[0] / dt01, p01[1] / dt01, p01[2] / dt01)
    dt02 = t2 - t0
    v = (p02[0] / dt02, p02[1] / dt02, p02[2] / dt02)
    
    p = (int(p0[0] - t0 * v[0] + 0.5), int(p0[1] - t0 * v[1] + 0.5), int(p0[2] - t0 * v[2] + 0.5))
    print(f"start at {p}")

# day24c(test24)
# day24c(input24)



def dots(stones, ts):
    # bad because as it gets far away, dots tend towards -1
    x,y,z, dx,dy,dz = ts
    score = 0
    for stone in stones:
        dp = normalize([stone.x - x, stone.y - y, stone.z - z])
        dv = normalize([stone.dx - dx, stone.dy - dy, stone.dz - dz])
        score += dot(dp,dv)
    return score

def dists(stones, vec):
    x,y,z, dx,dy,dz = vec[0:6]
    ts = vec[6:]

    score = 0
    for i,t in enumerate(ts):
        p = (x + dx * t, y + dy * t, z + dz * t)
        stone = stones[i] 
        pt = (stone.x + stone.dx * t, stone.y + stone.dy * t, stone.z + stone.dz * t)
        score += dist2(p,pt)

    return score

def day24d(sIn):
    # more attempts at solution using generic gradient-descent solver. Epic fail

    stones = []
    
    for line in sIn.split('\n'):
        stones.append(Stone(line))

    # tsInit = [0,0,0]
    # tsInit = [5,3,4] # does stay put, at least?
    # tsInit = [4,2,5] # testing -- ends up not at 5,3,4, rather at 4.999000865239925, 2.229716171963779, 3.8080839453914073
    # vecInit = [0,0,0,1,1,1,0,0,0] # x,y,z, dx,dy,dz, t0,t1,t2
    # vec = solve(lambda stones, vec: dists(stones, vec), stones, vecInit, dtStep=.01, alg = "axis descent")
    # vec = solve(lambda stones, vec: dists(stones, vec), stones, vecInit, dtStep=.001, alg = "gradient descent")

    vecInit = [0,0,0,1,1,1] # x,y,z, dx,dy,dz
    # vec = solve(lambda stones, vec: dots(stones, vec), stones, vecInit, dtStep=.01, alg = "axis descent")
    vec = solve(lambda stones, vec: dots(stones, vec), stones, vecInit, dtStep=.001, alg = "gradient descent")

    start = list(map(lambda g : int(g + .5), vec[0:3]))
    print(f"start at {start}, sum = {sum(start)}")

# day24d(test24)
# day24d(input24


def solveT0GivenV(dp, v0, v1, v):
    # add extra dummy var k so we have three vals and three equations (x,y,z)
    # (v - v0)t0 - (v-v1)t1 + k = p1 - p0

    dv0 = (v0[0] - v[0], v0[1] - v[1], v0[2] - v[2])
    dv1 = (v1[0] - v[0], v1[1] - v[1], v1[2] - v[2])

    # solve for t0, t1, k using Cramer's rule (ick)
    # denom happens to be cross product

    denom = -dv0[0] * dv1[1] - dv1[0] * dv0[2] - dv0[1] * dv1[2] \
            + dv0[0] * dv1[2] + dv1[0] * dv0[1] + dv1[1] * dv0[2]

    if denom == 0:
        # print("fail denom = 0") # perpendicular
        return None

    kNum = (-dv0[0] * dv1[1] *  dp[2] - dv1[0] *  dp[1] * dv0[2] - dp[0] * dv0[1] * dv1[2] \
           + dv0[0] *  dp[1] * dv1[2] + dv1[0] * dv0[1] *  dp[2] + dp[0] * dv1[1] * dv0[2])
    
    if kNum != 0:
        # print("fail k != 0")
        return None
    
    # k = kNum/denom

    t0 = (-dp[0] * dv1[1] - dv1[0] * dp[2] -  dp[1] * dv1[2] \
         + dp[0] * dv1[2] + dv1[0] * dp[1] + dv1[1] *  dp[2]) / denom
    # t1 = (dv0[0] * dp[1] + dp[0] * dv0[2] + dv0[1] * dp[2] \
    #     - dv0[0] * dp[2] - dp[0] * dv0[1] - dp[1] * dv0[2]) / denom
    
    return t0

def checkPV(stone, p, v):
    ...

def day24e(sIn):
    # finally worked, more or less
    # try all integer v "near" origin, and see whether there's a position which satisfies all constraints

    stones = []
    
    for line in sIn.split('\n'):
        stones.append(Stone(line))

    n = 250 # already tried all out to here
    # n = 0
    nPrev = n - 1

    stone0 = stones[0]
    stone1 = stones[1]
    dp = (stone1.x - stone0.x, stone1.y - stone0.y, stone1.z - stone0.z)
    v0 = (stone0.dx, stone0.dy, stone0.dz)
    v1 = (stone1.dx, stone1.dy, stone1.dz)

    while True:
        print(f"shell {n}")
        iterWhole = range(-n,n+1)
        iterFirstLast = [-n,n]
        for dx in range(-n,n+1):
            for dy in range(-n,n+1):
                if dx >= -nPrev and dx < nPrev + 1 \
                    and dy >= -nPrev and dy < nPrev + 1:
                    iterUse = iterFirstLast
                else:
                    iterUse = iterWhole
                for dz in iterUse:
                    # if dx >= -nPrev and dx < nPrev + 1 \
                    #     and dy >= -nPrev and dy < nPrev + 1 \
                    #     and dz >= -nPrev and dz < nPrev + 1:
                    #     continue # already checked in prev pass -- much faster to not generate at all?

                    v = (dx,dy,dz)
                    # print(f"try {(dx,dy,dz)}")

                    # check whether this v can hit first two stones

                    t0 = solveT0GivenV(dp, v0, v1, v)
                    if t0 == None:
                        continue

                    # check that other pairs match
                    # BB cheaper to check solution against just stonej?

                    t0Ok = t0

                    for j in range(2, len(stones)):
                        stonej = stones[j]

                        # print(f"{(dx,dy,dz)} i={i} j={j}")
                        dpj = (stonej.x - stone0.x, stonej.y - stone0.y, stonej.z - stone0.z)
                        t0 = solveT0GivenV(dpj, v0, (stonej.dx,stonej.dy,stonej.dz), v)
                        if t0 == None:
                            t0Ok = None
                            break
                        if t0 != t0Ok:
                            # print(f"fail t0 doesn't match")
                            t0Ok = None
                            break

                    if t0Ok != None:
                        p = (stone0.x + (v0[0] - v[0]) * t0Ok, stone0.y + (v0[1] - v[1]) * t0Ok, stone0.z + (v0[2] - v[2]) * t0Ok)
                        # print(f"t0 = {t0}, t1 = {t1}, p = {p}")
                        print(f"solution with t0 = {t0Ok} p = {p} v = {(dx,dy,dz)} sum = {p[0] + p[1] + p[2]}")
                        return
                    
        nPrev = n # don't forget to update nPrev like I did, or else it will check N^4 vs
        n += 1


# day24e(test24)
day24e(input24)

# solution with t0 = 137307190534.0 p = (335849990884055.0, 362494628861890.0, 130073711567420.0) v = (-110, -135, 299) sum = 828418331313365.