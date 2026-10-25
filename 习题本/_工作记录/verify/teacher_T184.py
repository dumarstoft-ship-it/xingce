# T184 A班40人平均65；B班漏统计2人后平均72，两班整体平均68；B班最高96，最低不低于最高分一半。
# 算上漏统计的2人，B班平均分最少比A班高多少。
from fractions import Fraction as F
from math import ceil

NA, AVG_A, AVG_B0, AVG_ALL, B_MAX, MISS = 40, 65, 72, 68, 96, 2
OPTS = {'A': F(4), 'B': F(9, 2), 'C': F(5), 'D': F(11, 2)}
nb = next(n for n in range(1, 1000) if NA * AVG_A + n * AVG_B0 == (NA + n) * AVG_ALL)   # B班已统计人数
low = ceil(F(B_MAX, 2))                       # 遗漏者最低可能分
avg_b = F(nb * AVG_B0 + MISS * low, nb + MISS)
diff = avg_b - AVG_A
hits = [k for k, v in OPTS.items() if v == diff]
assert len(hits) == 1, (diff, hits)
print('B recorded =', nb, 'B avg min =', float(avg_b), 'diff =', float(diff))
print(hits[0])
