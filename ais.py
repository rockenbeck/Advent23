# https://hack.ainfosec.com
# f1cbf57e-dbaf-4f62-a990-a6e18d2ca542
import math
import heapq

test="""|  2 |   7 |   1 |   3 |   5 |
| 20 |   6 |   8 |   4 |   9 |
|  X |  12 |  19 |  13 |  10 |
| 11 |  18 |  17 |  21 |  23 |
| 16 |  15 |  14 |  22 |  24 |"""
testF="""|  1 |   2 |   3 |   4 |   5 |
|  6 |   7 |   8 |   9 |  10 |
| 11 |  12 |  13 |  14 |  15 |
| 16 |  17 |  18 |  19 |  20 |
| 21 |  22 |  23 |  24 |   X |"""
test2="""|  2 |   1 |   3 |   4 |   5 |
|  6 |   7 |   8 |   9 |  10 |
| 11 |  12 |  13 |  14 |  15 |
| 16 |  17 |  18 |  19 |  20 |
| 21 |  22 |  23 |  24 |   X |""" # unsolveable
test3="""|  2 |   7 |   3 |   4 |   5 |
|  6 |   1 |   8 |   9 |  10 |
| 11 |  12 |  13 |  14 |  15 |
| 16 |  17 |  18 |  19 |  20 |
| 21 |  22 |  23 |  24 |   X |"""


def score(board,xX,yX):
    s = 0
    nWrong = 26
    distWrong = 0

    for y in range(0,5):
        for x in range(0,5):
            n = board[y * 5 + x]
            if n == 25:
                continue

            yT = (n - 1) // 5
            xT = n - 1 - yT * 5

            if x != xT or y != yT:
                if n < nWrong:
                    nWrong = n
                    distWrong = max(abs(x - xX), abs(y - yX))

            # sum of manhattan dist of each tile from target
            s += abs(x - xT) + abs(y - yT)

            # weight lower numbers higher
            # s += ((25-n)*(25-n)) * (abs(x - xT) + abs(y - yT))

            # add factor for how far X is from current pos (go get this one)
            # s += ((5-xT)*(5-yT)) * (abs(x - xT) + abs(y - yT)) * (abs(x - xX) + abs(y - yX))

            # bad cause tiles are TOO sticky
            # s += 100**(25-n) * (abs(x - xT) + abs(y - yT)) * (abs(x - xX) + abs(y - yX))

    s += distWrong
    
    return s

def hash(board):
    s = 0
    for i in range(0,25):
        s = s * 25 + board[i]
    return s

def printboard(board):
    s = ""
    for y in range(0,5):
        for x in range(0,5):
            n = board[y * 5 + x]
            s += f"| {n: <3} "
        s += '|\n'
    print(s)


def loadboard(sIn):
    board = []
    xX,yX = -1,-1
    y = 0
    for line in sIn.split('\n'):
        x = 0
        for i in range(0,5):
            s = line[i * 6 + 2:i * 6 + 4]
            if 'X' in s:
                n = 25
            else:
                n = int(s)
            if n == 25:
                xX,yX = x,y
            board.append(n)
            x += 1
        y += 1
    # print(board, xX, yX, score(board,xX,yX))

    return (board, xX, yX)

def debug(sIn):
    board, xX, yX = loadboard(sIn)
    
    printboard(board)
    print(score(board,xX,yX))

def solve(sIn):
    board, xX, yX = loadboard(sIn)
    
    heap = [(score(board,xX,yX), board, xX, yX, "")]

    best = {hash(board):""}

    sBest = -1

    while True:
        s,board,x,y,moves = heapq.heappop(heap)

        # if sBest < 0 or s < sBest:
        #     sBest = s
        #     print(f"best = {s}, len = {len(heap)}")
        #     printboard(board)
        #     print(moves)

        if s == 0:
            print(f"\n\n")
            chunk = 60
            while len(moves) > chunk:
                print(f"{','.join(moves[0:chunk])}")
                moves = moves[chunk:]
            print(f"{','.join(moves)}\n\n")
            return
        for i in range(0,4):
            dir = "LRUD"[i]
            dx,dy = [(-1,0),(1,0),(0,-1),(0,1)][i]
            xT = x + dx
            yT = y + dy
            if xT < 0 or xT >= 5 or yT < 0 or yT >= 5:
                continue
            boardT = board.copy()
            boardT[y*5+x] = board[yT*5+xT]
            boardT[yT*5+xT] = board[y*5+x]
            hb = hash(boardT)
            if hb in best and len(best[hb]) <= len(moves) + 1:
                continue
            sT = score(boardT,xT,yT) # would be cheaper to just compute delta
            movesT = moves + dir
            best[hb] = movesT
            heapq.heappush(heap, (sT, boardT, xT, yT, movesT))

testx="""| 11 |   6 |   9 |   3 |  10 |
| 17 |   8 |  12 |   5 |   4 |
|  X |   7 |   1 |  13 |  19 |
| 21 |  22 |  16 |   2 |  14 |
| 23 |  18 |  20 |  15 |  24 |"""

# solve(testx)


# hhhhhhh =  Score is 14.285714285714285
# 11h1111
# iiiiiii

# ppppppp = is 14.285714285714285
# 11111p1
# rrrrrrr same
# 1r11111
# uuuuuuu "
# u111111
# 0 same
# 1111110 14.2... else 0
# 6 same 
# 1116111 14

# urh6*p0
# urh6ip0

import random
s = ""
for i in range(0,6):
    s += str(random.randint(0, 9))
print(s)