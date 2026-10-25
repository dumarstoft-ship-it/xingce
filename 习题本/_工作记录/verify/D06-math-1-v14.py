# D06-math-1-v14: 每次成功率 0.8，独立执行 4 次，至少 3 次成功的概率
from fractions import Fraction as F
from itertools import product
p = F(8, 10)
ans = F(0)
for outcome in product([1, 0], repeat=4):
    pr = F(1)
    for o in outcome:
        pr *= p if o else 1 - p
    if sum(outcome) >= 3:
        ans += pr
opts = {'A': F(4096, 10000), 'B': F(5120, 10000), 'C': F(8192, 10000), 'D': F(9728, 10000)}
hit = [L for L, v in opts.items() if v == ans]
assert len(hit) == 1, (ans, hit)
print('P =', ans, float(ans))
print(hit[0])
