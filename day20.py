import re
from collections import defaultdict
from collections import deque
import sys
import random
import math
import numpy as np
import heapq
import bisect 

from input20 import *

test20="""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

test20b="""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""


class Node:
    def __init__(self, s):
        self.s = s

        sname,soutputs = s.split(" -> ")
        if sname[0] == '%':
            self.type = '%'
            self.name = sname[1:]
            self.onoff = False
        elif sname[0] == '&':
            self.type = '&'
            self.name = sname[1:]
            self.mpInHilo = {}
        elif sname == "broadcaster":
            self.type = 'b'
            self.name = sname
        else:
            self.type = 'o'
            self.name = sname

        self.inputs = set()
        self.outputs = soutputs.split(", ")

    def __repr__(self):
        return repr((self.type, self.name, self.outputs))




def day20(sIn):
    mp = {}

    for line in sIn.split('\n'):
        node = Node(line)
        mp[node.name] = node

    for node in mp.values():
        for name in node.outputs:
            if name in mp:
                nodeOut = mp[name]
                if nodeOut.type == '&':
                    nodeOut.mpInHilo[node.name] = "low"

    # print(mp)

    cHigh = 0
    cLow = 0

    pulses = deque()
    for i in range(0,1000):
        pulses.append(("button","broadcaster","low"))
        while len(pulses) > 0:
            sfrom,sto,hilo = pulses.pop()

            if i == 0:
                print(f"{sfrom} -{hilo}-> {sto}")
            
            if hilo == "high":
                cHigh += 1
            else:
                cLow += 1

            if sto not in mp:
                continue # output node

            node = mp[sto]

            if node.type == 'b':
                for nout in node.outputs:
                    pulses.append((sto,nout,hilo))
            elif node.type == '%':
                if hilo == "low":
                    node.onoff = "off" if node.onoff == "on" else "on"
                    out = "high" if node.onoff == "on" else "low"
                    for nout in node.outputs:
                        pulses.append((sto,nout,out))
            elif node.type == '&':
                node.mpInHilo[sfrom] = hilo
                out = "low"
                for hl in node.mpInHilo.values():
                    if hl != "high":
                        out = "high"
                        break
                for nout in node.outputs:
                    pulses.append((sto,nout,out))
            elif node.type == 'o':
                pass
            else:
                assert False
                    
    print(f"total pulses = {cHigh} * {cLow} = {cHigh * cLow}")



# day20(test20b)
# day20(input20)

def show(mp, name, indent):
    if len(indent) > 30:
        print(f"{indent}...")
        exit(0)
    node = mp[name]
    print(f"{indent}{node.type}{node.name}")
    for input in node.inputs:
        show(mp, input, indent+" ")

def allinsr(mp, node, ins):
    if node in ins:
        return
    ins.add(node)
    for n in node.inputs:
        allinsr(mp, n, ins)

def allins(mp, name):
    ins = set()
    allinsr(mp, name, ins)
    return sorted(map(lambda node : node.name, ins))

def pruned(mp, limits):
    mp = {k:v for k,v in mp.items() if k in limits}
    for node in mp.values():
        node.outputs = list(filter(lambda n : n in limits, node.outputs))
    return mp

def day20b(sIn, limits):
    mp = {}

    for line in sIn.split('\n'):
        node = Node(line)
        mp[node.name] = node

    # add implicit output nodes
    imps = set()
    for node in mp.values():
        for nameOut in node.outputs:
            if nameOut not in mp:
                imps.add(nameOut)
    for name in imps:
        mp[name] = Node(f"{name} -> ")

    if len(limits) > 0:
        mp = pruned(mp, limits)

    # convert names to nodes
    for node in mp.values():
        node.outputs = [mp[n] for n in node.outputs if n in mp]

    for node in mp.values():
        for nodeOut in node.outputs:
            nodeOut.inputs.add(node)
            if nodeOut.type == '&':
                nodeOut.mpInHilo[node] = True

    # for node in mp.values():
    #     if node.type == '&':
    #         print(node.name, node.mpInHilo.keys())
    # show(mp, "dr", "")

    # for name in sorted(mp.keys()):
    #     node = mp[name]
    #     print(f"{node.type}{node.name} <- {[n.name for n in node.inputs]} -> {[n.name for n in node.outputs]}")

    # for n in mp["dr"].inputs:
    #     print(f"{n.name} <- all in {allins(mp, n)}")

    nodeRx = mp["rx"]

    cButton = 0

    mpInHiPrev = {}
    mpInLoop = {}

    trace = []
    # trace = [4026,4027]
    pulses = deque()    
    while True:
        pulses.append((None,mp["broadcaster"],True))
        cButton += 1
        if cButton in trace:
            print(f"cButton = {cButton}")

        cLowRx = 0

        while len(pulses) > 0:
            nodeFrom,node,hilo = pulses.popleft()

            if cButton in trace:
                print(f"{nodeFrom.name if nodeFrom else 'none'} -{hilo}-> {node.name}")

            if node == nodeRx and hilo:
                print(f"rx low {cButton}")
                cLowRx += 1
    
            if node.type == 'b':
                for nout in node.outputs:
                    pulses.append((node,nout,hilo))
            elif node.type == '%':
                if hilo:
                    out = node.onoff
                    node.onoff = not node.onoff
                    for nout in node.outputs:
                        pulses.append((node,nout,out))
            elif node.type == '&':
                node.mpInHilo[nodeFrom] = hilo
                out = True not in node.mpInHilo.values() # NOR gate
                for nout in node.outputs:
                    pulses.append((node,nout,out))
            elif node.type == 'o':
                pass
            else:
                assert False

        # if cButton in trace:
        #     node = mp["dr"]
        #     for n,hilo in node.mpInHilo.items():
        #         if not hilo:
        #             if n in mpInHiPrev:
        #                 loop = cButton - mpInHiPrev[n]
        #                 if n in mpInLoop:
        #                     assert mpInLoop[n] == loop
        #                 else:
        #                     mpInLoop[n] = loop
        #                 print(f"{n.name} cycles at {mpInHiPrev[n]} with len {loop}")
        #             mpInHiPrev[n] = cButton

        # node = mp["cs"]
        # print(f"{[(n.name, hilo) for n,hilo in node.mpInHilo.items()]}")

        n = 0
        for name in reversed(["pj", "pr", "zl", "pm", "kk", "tc", "hn", "pq", "tl", "vn", "ls", "jd"]):
            hilo = mp[name].onoff
            n = n * 2 + (1 if hilo else 0)
        print(f"n = {n} = {n:b}b")

        node = mp["dr"]
        if False in node.mpInHilo.values():
            print(f"{cButton}: {node.mpInHilo}")
        
        if cButton % 100000 == 0:
            print(f"{cButton} tick")
        # if cLowRx == 1:
        #     break
        if cButton == 4030:
            break

                    
    print(f"total pushes til rx 1 = {cButton}")


# day20b(input20, [])
# day20b(input20, set(['rx', 'dr','bj', 'bp', 'broadcaster', 'cr', 'fl', 'gg', 'jg', 'jh', 'ng', 'nx', 'ps', 'rz', 'sg', 'st', 'zr']))
# 0 + 3919 * N
day20b(input20, set(['rx', 'dr','broadcaster', 'cs', 'hn', 'jd', 'kk', 'ls', 'pj', 'pm', 'pq', 'pr', 'qb', 'tc', 'tl', 'vn', 'zl']))
# 4027
# day20b(input20, set(['rx', 'dr','broadcaster', 'ch', 'dd', 'dx', 'hc', 'mp', 'qp', 'rm', 'rr', 'tn', 'xs', 'xz', 'zj', 'zn', 'zz']))
# 3917
# day20b(input20, set(['rx', 'dr','broadcaster', 'cg', 'ck', 'hr', 'kd', 'kl', 'km', 'lb', 'lv', 'ns', 'pl', 'qt', 'rj', 'rk', 'xq']))
# 4007

# print(f"3919 * 4027 * 3917 * 4007 = {3919 * 4027 * 3917 * 4007}")

# ng <- all in ['bj', 'bp', 'broadcaster', 'cr', 'fl', 'gg', 'jg', 'jh', 'ng', 'nx', 'ps', 'rz', 'sg', 'st', 'zr']
# qb <- all in ['broadcaster', 'cs', 'hn', 'jd', 'kk', 'ls', 'pj', 'pm', 'pq', 'pr', 'qb', 'tc', 'tl', 'vn', 'zl']
# mp <- all in ['broadcaster', 'ch', 'dd', 'dx', 'hc', 'mp', 'qp', 'rm', 'rr', 'tn', 'xs', 'xz', 'zj', 'zn', 'zz']
# qt <- all in ['broadcaster', 'cg', 'ck', 'hr', 'kd', 'kl', 'km', 'lb', 'lv', 'ns', 'pl', 'qt', 'rj', 'rk', 'xq']


# %bj <- {'jh', 'st'} -> ['gg']
# %bp <- {'jh', 'ps'} -> ['zr']
# bbroadcaster <- set() -> ['ns', 'pj', 'xz', 'sg']
# %cg <- {'lb'} -> ['lv', 'ck']
# %ch <- {'zz'} -> ['dx']
# &ck <- {'rk', 'ns', 'kd', 'xq', 'pl', 'rj', 'cg', 'km', 'hr'} -> ['lb', 'lv', 'ns', 'kl', 'qt']
# %cr <- {'nx'} -> ['jg', 'jh']
# &cs <- {'jd', 'pj', 'pr', 'vn', 'ls', 'pm', 'pq', 'tl', 'kk', 'tc'} -> ['hn', 'pj', 'qb', 'zl']
# %dd <- {'zn'} -> ['dx', 'qp']
# &dr <- {'ng', 'qb', 'mp', 'qt'} -> ['rx']
# &dx <- {'ch', 'xz', 'rr', 'qp', 'rm', 'tn', 'dd', 'zz'} -> ['zj', 'xz', 'mp', 'zn', 'xs', 'hc']
# %fl <- {'rz'} -> ['jh', 'ps']
# %gg <- {'bj'} -> ['jh', 'nx']
# %hc <- {'dx', 'zj'} -> ['tn']
# %hn <- {'cs', 'tc'} -> ['pq']
# %hr <- {'lv'} -> ['ck', 'pl']
# %jd <- {'ls'} -> ['cs']
# %jg <- {'cr'} -> ['jh']
# &jh <- {'rz', 'ps', 'gg', 'jg', 'nx', 'st', 'fl', 'cr', 'sg'} -> ['ng', 'bp', 'zr', 'sg', 'bj']
# %kd <- {'ns'} -> ['rk', 'ck']
# %kk <- {'pm'} -> ['cs', 'tc']
# %kl <- {'rk', 'ck'} -> ['lb']
# %km <- {'rj'} -> ['ck']
# %lb <- {'ck', 'kl'} -> ['cg']
# %ls <- {'vn'} -> ['cs', 'jd']
# %lv <- {'ck', 'cg'} -> ['hr']
# &mp <- {'dx'} -> ['dr']
# &ng <- {'jh'} -> ['dr']
# %ns <- {'broadcaster', 'ck'} -> ['ck', 'kd']
# %nx <- {'gg'} -> ['jh', 'cr']
# %pj <- {'broadcaster', 'cs'} -> ['cs', 'pr']
# %pl <- {'hr'} -> ['ck', 'xq']
# %pm <- {'zl'} -> ['cs', 'kk']
# %pq <- {'hn'} -> ['tl', 'cs']
# %pr <- {'pj'} -> ['zl', 'cs']
# %ps <- {'fl'} -> ['bp', 'jh']
# &qb <- {'cs'} -> ['dr']
# %qp <- {'dd'} -> ['dx', 'zj']
# &qt <- {'ck'} -> ['dr']
# %rj <- {'xq'} -> ['km', 'ck']
# %rk <- {'kd'} -> ['ck', 'kl']
# %rm <- {'rr'} -> ['zz', 'dx']
# %rr <- {'xs'} -> ['rm', 'dx']
# %rz <- {'sg'} -> ['jh', 'fl']
# %sg <- {'broadcaster', 'jh'} -> ['rz', 'jh']
# %st <- {'zr'} -> ['jh', 'bj']
# %tc <- {'kk'} -> ['cs', 'hn']
# %tl <- {'pq'} -> ['vn', 'cs']
# %tn <- {'hc'} -> ['dx', 'xs']
# %vn <- {'tl'} -> ['cs', 'ls']
# %xq <- {'pl'} -> ['rj', 'ck']
# %xs <- {'dx', 'tn'} -> ['rr']
# %xz <- {'broadcaster', 'dx'} -> ['dx', 'zn']
# %zj <- {'dx', 'qp'} -> ['hc']
# %zl <- {'pr', 'cs'} -> ['pm']
# %zn <- {'dx', 'xz'} -> ['dd']
# %zr <- {'jh', 'bp'} -> ['st']
# %zz <- {'rm'} -> ['dx', 'ch']