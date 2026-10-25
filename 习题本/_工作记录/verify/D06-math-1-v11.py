# D06-math-1-v11: 三人分别从周一~周五随机选 2、3、4 天，周三(下标 2)恰有两人在的概率
from fractions import Fraction as F
from itertools import combinations, product
days = range(5)
choices = [list(combinations(days, m)) for m in (2, 3, 4)]
good = total = 0
for c in product(*choices):
    total += 1
    good += (sum(2 in x for x in c) == 2)
ans = F(good, total)
opts = {'A': F(24, 125), 'B': F(36, 125), 'C': F(54, 125), 'D': F(58, 125)}
hit = [L for L, v in opts.items() if v == ans]
assert len(hit) == 1, (ans, hit)
print('P =', ans)
print(hit[0])
