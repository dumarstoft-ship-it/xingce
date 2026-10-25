# D06-math-1-v07: 7 个一排车位随机停 3 辆(车辆不同)，恰有两辆相邻且第三辆与它们都不相邻
from fractions import Fraction as F
from itertools import permutations
good = total = 0
for pos in permutations(range(7), 3):        # 3 辆不同的车各占一个车位
    total += 1
    s = sorted(pos)
    adj = sum(1 for i in range(2) if s[i + 1] - s[i] == 1)
    good += (adj == 1)                         # 恰一对相邻(三车连排有 2 对相邻)
ans = F(good, total)
opts = {'A': F(2, 7), 'B': F(18, 35), 'C': F(4, 7), 'D': F(5, 7)}
hit = [L for L, v in opts.items() if v == ans]
assert len(hit) == 1, (ans, hit)
print('P =', ans)
print(hit[0])
