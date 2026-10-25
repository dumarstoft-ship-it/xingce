# teacher T134（2018重庆）单局甲胜0.6，五局三胜，前两局1:1，甲获胜的概率
from fractions import Fraction as F
from functools import lru_cache
from math import comb

OPTS = {'A': F(9, 25), 'B': F(63, 125), 'C': F(81, 125), 'D': F(101, 125)}
p, NEED, GAMES = F(6, 10), 3, 5
A0, B0 = 1, 1

@lru_cache(None)
def win(a, b):
    if a == NEED:
        return F(1)
    if b == NEED:
        return F(0)
    return p * win(a + 1, b) + (1 - p) * win(a, b + 1)

P = win(A0, B0)
rest = GAMES - A0 - B0
P_full = sum(comb(rest, k) * p ** k * (1 - p) ** (rest - k) for k in range(rest + 1) if A0 + k >= NEED)
assert P == P_full
print('P =', P, '| 漏掉一种“输一赢二”顺序 =', p * p + (1 - p) * p * p)
hits = [k for k, v in OPTS.items() if v == P]
assert len(hits) == 1, hits
print(hits[0])
