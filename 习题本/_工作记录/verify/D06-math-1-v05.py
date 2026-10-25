# D06-math-1-v05: 1~9 号球一次摸 2 个，号码和为 3 的倍数的概率
from fractions import Fraction as F
from itertools import combinations
sets = list(combinations(range(1, 10), 2))
ans = F(sum(1 for a, b in sets if (a + b) % 3 == 0), len(sets))
opts = {'A': F(1, 12), 'B': F(1, 4), 'C': F(5, 18), 'D': F(1, 3)}
hit = [L for L, v in opts.items() if v == ans]
assert len(hit) == 1, (ans, hit)
print('P =', ans)
print(hit[0])
