# T123 8幅作品随机分给8位作者（每人一幅），恰好3人拿到本人作品的概率范围
from itertools import permutations
from fractions import Fraction as F

N, K = 8, 3
RANGES = {'A': (F(5, 100), F(10, 100)), 'B': (F(10, 100), F(15, 100)),
          'C': (F(15, 100), F(1)), 'D': (F(0), F(5, 100))}
total = good = 0
for p in permutations(range(N)):
    total += 1
    if sum(p[i] == i for i in range(N)) == K:
        good += 1
prob = F(good, total)
hits = [k for k, (lo, hi) in RANGES.items() if lo < prob < hi]
assert len(hits) == 1
print('P =', prob, float(prob))
print(hits[0])
