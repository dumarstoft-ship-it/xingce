# real 2026ZJA-63: 1~10 中随机选两个数，最大公约数为 1 的概率
from fractions import Fraction as F
from itertools import combinations
from math import gcd
sets = list(combinations(range(1, 11), 2))
ans = F(sum(1 for a, b in sets if gcd(a, b) == 1), len(sets))
opts = {'A': F(2, 3), 'B': F(31, 45), 'C': F(11, 15), 'D': F(7, 9)}
hit = [L for L, v in opts.items() if v == ans]
assert len(hit) == 1, (ans, hit)
print('P =', ans)
print(hit[0])
