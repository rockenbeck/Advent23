import re
from collections import defaultdict
import sys
import random
import math
import numpy as np
import heapq
import bisect 

from input19 import *

test19="""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

def day19(sIn):
    # ought to wrap these in a mapify fn

    wfs = {}

    sWf,sParts = sIn.split('\n\n')

    for line in sWf.split('\n'):
        ia = line.find('{')
        assert ia > 0
        name = line[:ia]
        sRules = line[ia+1:-1]
        rules = []
        for s in sRules.split(','):
            if ':' in s:
                sCond,dest = s.split(':')
                var = sCond[0]
                comp = sCond[1]
                val = int(sCond[2:])
            else:
                var = None
                comp = None
                val = None
                dest = s
            rules.append((var,comp,val,dest))
        wfs[name] = rules

    accepts = 0

    for line in sParts.split('\n'):
        vals = {}
        for s in line[1:-1].split(','):
            var,val = s.split('=')
            vals[var] = int(val)

        name = "in"

        while True:
            rules = wfs[name]
            ok = False
            for rule in rules[:-1]:
                valCur = vals[rule[0]]
                valComp = rule[2]
                if rule[1] == '<':
                    ok = valCur < valComp
                else:
                    assert rule[1] == '>'
                    ok = valCur > valComp
                if ok:
                    name = rule[3]
                    break
            if not ok:
                name = rules[-1][3]
            if name == 'A':
                accepts += sum(vals.values())
                break
            elif name == 'R':
                break
            
    print(f"accepts = {accepts}")

# day19(test19)
# day19(input19)


def count(vals, wfs, name, iRule,depth):
    if depth > 30:
        print("deep")
    if name == 'A':
        sum = math.prod(map(lambda r: r[1]-r[0], vals))
        return sum
    elif name == 'R':
        return 0
    
    rules = wfs[name]

    sum = 0

    if iRule < len(rules) - 1:
        rule = rules[iRule]
        ivar = "xmas".find(rule[0])
        (nMin,nMax) = vals[ivar]

        nMinPass,nMaxPass = nMin,nMax
        valComp = rule[2]
        if rule[1] == '<':
            nMaxPass = valComp
            nMin = valComp
        else:
            assert rule[1] == '>'
            nMinPass = valComp+1
            nMax = valComp+1
        
        if nMaxPass > nMinPass:
            valsPass = vals.copy()
            valsPass[ivar] = (nMinPass,nMaxPass)
            sum = count(valsPass, wfs, rule[3], 0,depth+1)

        if nMax <= nMin:
            return sum
        
        vals = vals.copy()
        vals[ivar] = (nMin,nMax)

        iRuleNext = iRule + 1
        
    else:
        name = rules[-1][3]
        iRuleNext = 0

    sum += count(vals, wfs, name, iRuleNext, depth+1)

    return sum

# real 167409079868000
# mine 167474394229030

def day19b(sIn):
    # ought to wrap these in a mapify fn

    wfs = {}

    sWf,sParts = sIn.split('\n\n')

    for line in sWf.split('\n'):
        ia = line.find('{')
        assert ia > 0
        name = line[:ia]
        sRules = line[ia+1:-1]
        rules = []
        for s in sRules.split(','):
            if ':' in s:
                sCond,dest = s.split(':')
                var = sCond[0]
                comp = sCond[1]
                val = int(sCond[2:])
            else:
                var = None
                comp = None
                val = None
                dest = s
            rules.append((var,comp,val,dest))
        wfs[name] = rules

    accepts = 0

    vals = [(1,4001), (1,4001), (1,4001), (1,4001)]

    accepts = count(vals, wfs, "in", 0, 0)
            
    print(f"accepts = {accepts}")


# day19b(test19)
day19b(input19)

test19b = """in{x>1:R,s<2:A,R}

"""
# day19b(test19b)
