# D06-math-1-v08: 一排 9 座随机坐 3 名考生，任意两人之间至少隔 2 个空座的概率
from fractions import Fraction as F
from itertools import permutations
good = total = 0
for pos in permutations(range(9), 3):
    total += 1
    s = sorted(pos)
    good += all(s[i + 1] - s[i] - 1 >= 2 for i in range(2))   # 相邻两人之间空座数 >= 2
ans = F(good, total)
opts = {'A': F(1, 21), 'B': F(5, 42), 'C': F(5, 21), 'D': F(5, 12)}
hit = [L for L, v in opts.items() if v == ans]
assert len(hit) == 1, (ans, hit)
print('P =', ans)
print(hit[0])
