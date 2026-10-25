# teacher T133（2015河南）实力相当，7局4胜，甲2:1领先，甲最终获胜的概率
from fractions import Fraction as F
from functools import lru_cache
from math import comb

OPTS = {'A': F(2, 3), 'B': F(3, 4), 'C': F(5, 8), 'D': F(11, 16)}
p, NEED, GAMES = F(1, 2), 4, 7
A0, B0 = 2, 1

@lru_cache(None)
def win(a, b):
    """真实赛制：谁先到4胜比赛就结束"""
    if a == NEED:
        return F(1)
    if b == NEED:
        return F(0)
    return p * win(a + 1, b) + (1 - p) * win(a, b + 1)

P = win(A0, B0)
rest = GAMES - A0 - B0                     # 打满7局的等价算法
P_full = sum(comb(rest, k) * p ** k * (1 - p) ** (rest - k) for k in range(rest + 1) if A0 + k >= NEED)
assert P == P_full
print('P =', P)
hits = [k for k, v in OPTS.items() if v == P]
assert len(hits) == 1, hits
print(hits[0])
