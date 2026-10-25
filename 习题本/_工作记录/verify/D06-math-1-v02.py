# D06-math-1-v02: 随机选 4 人，小陈、小黄都没选中的概率 = 都被选中概率的 11 倍，求总人数
from fractions import Fraction as F
from itertools import combinations
sols = []
for N in range(6, 41):
    neither = both = total = 0
    for s in combinations(range(N), 4):      # 0 = 小陈, 1 = 小黄
        total += 1
        a, b = 0 in s, 1 in s
        neither += (not a and not b)
        both += (a and b)
    if both and F(neither, total) == 11 * F(both, total):
        sols.append(N)
assert len(sols) == 1, sols
opts = {'A': 14, 'B': 15, 'C': 16, 'D': 17}
hit = [L for L, v in opts.items() if v == sols[0]]
assert len(hit) == 1
print('N =', sols[0])
print(hit[0])
