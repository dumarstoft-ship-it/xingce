# real 2026GK-73: 随机选 3 人，张、李中只有 1 人被选中的概率 = 2 人均被选中概率的 30 倍，求总人数
from fractions import Fraction as F
from itertools import combinations
sols = []
for N in range(5, 61):
    one = both = 0
    for s in combinations(range(N), 3):       # 0 = 张立, 1 = 李磊
        k = (0 in s) + (1 in s)
        one += (k == 1)
        both += (k == 2)
    if both and F(one, both) == 30:
        sols.append(N)
assert len(sols) == 1, sols
opts = {'A': 15, 'B': 17, 'C': 29, 'D': 33}
hit = [L for L, v in opts.items() if v == sols[0]]
assert len(hit) == 1
print('N =', sols[0])
print(hit[0])
