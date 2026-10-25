# D06-math-1-v06: 均匀骰子连掷两次，较大点数恰为 5 的概率
from fractions import Fraction as F
from itertools import product
allc = list(product(range(1, 7), repeat=2))
ans = F(sum(1 for a, b in allc if max(a, b) == 5), len(allc))
opts = {'A': F(1, 4), 'B': F(5, 18), 'C': F(11, 36), 'D': F(25, 36)}
hit = [L for L, v in opts.items() if v == ans]
assert len(hit) == 1, (ans, hit)
print('P =', ans)
print(hit[0])
