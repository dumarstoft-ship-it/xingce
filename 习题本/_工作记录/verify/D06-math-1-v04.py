# D06-math-1-v04: 4 人各自从 6 个小组随机报 1 个，至少 2 人同组的概率
from fractions import Fraction as F
from itertools import product
allc = list(product(range(6), repeat=4))
good = sum(1 for t in allc if len(set(t)) < 4)
ans = F(good, len(allc))
opts = {'A': F(5, 18), 'B': F(91, 216), 'C': F(5, 9), 'D': F(13, 18)}
hit = [L for L, v in opts.items() if v == ans]
assert len(hit) == 1, (ans, hit)
print('P =', ans)
print(hit[0])
