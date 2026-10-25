# D06-math-1-v03: 8 窗口(3 综合 + 5 专项)随机抽 3 个，两类都有的概率
from fractions import Fraction as F
from itertools import combinations
kind = ['Z'] * 3 + ['S'] * 5
sets = list(combinations(range(8), 3))
good = sum(1 for s in sets if len({kind[i] for i in s}) == 2)
ans = F(good, len(sets))
opts = {'A': F(45, 56), 'B': F(23, 28), 'C': F(15, 28), 'D': F(11, 56)}
hit = [L for L, v in opts.items() if v == ans]
assert len(hit) == 1, (ans, hit)
print('P =', ans)
print(hit[0])
