# teacher T130 母题：5排共40座，小张、小李随机入座，坐同一排的概率（选项为自拟）
from fractions import Fraction as F
from itertools import permutations
from math import comb

OPTS = {'A': F(1, 5), 'B': F(7, 195), 'C': F(7, 39), 'D': F(8, 39)}
ROWS, SEATS = 5, 40
PER = SEATS // ROWS
seats = [(r, c) for r in range(ROWS) for c in range(PER)]
pairs = list(permutations(seats, 2))
P = F(sum(a[0] == b[0] for a, b in pairs), len(pairs))
print('P =', P)
# 干扰项都来自真实错误
assert OPTS['A'] == F(1, ROWS)                          # 只看“排”不看座位
assert OPTS['B'] == F(comb(PER, 2), comb(SEATS, 2))     # 忘乘5排
assert OPTS['D'] == F(PER, SEATS - 1)                   # 张那排仍按8个空位
hits = [k for k, v in OPTS.items() if v == P]
assert len(hits) == 1, hits
print(hits[0])
