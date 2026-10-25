# D06-math-1-v13: 综合科 5 人 + 党建科 4 人，每周有放回抽 1 人，3 周中恰 2 周是综合科的概率所在区间
from fractions import Fraction as F
from itertools import product
zonghe = set(range(5))
allc = list(product(range(9), repeat=3))
ans = F(sum(1 for t in allc if sum(x in zonghe for x in t) == 2), len(allc))
ranges = {'A': (F(0), F(3, 10), 'lt'), 'B': (F(3, 10), F(4, 10), 'in'),
          'C': (F(4, 10), F(5, 10), 'in'), 'D': (F(5, 10), F(1), 'gt')}
def inside(x, r):
    lo, hi, t = r
    if t == 'lt': return x < hi
    if t == 'gt': return x > lo
    return lo <= x <= hi
hit = [L for L, r in ranges.items() if inside(ans, r)]
assert len(hit) == 1, (ans, hit)
assert F(4, 10) < ans < F(5, 10) and ans - F(4, 10) > F(1, 100)   # 不贴边界
print('P =', ans, float(ans))
print(hit[0])
