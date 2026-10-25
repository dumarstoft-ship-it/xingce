# D02-math-1-v16  茶园：每亩原有y、每天生长g；甲10亩12人10天，乙15亩20人6天；丙24亩12天恰好采完需几人
from fractions import Fraction as F
OPTS = {'A': 10, 'B': 16, 'C': 24, 'D': 28}

# 每亩所需“人·天”：甲 12*10/10 = y + 10g ；乙 20*6/15 = y + 6g
r1, r2 = F(12 * 10, 10), F(20 * 6, 15)
g = (r1 - r2) / (10 - 6)
y = r1 - 10 * g
assert g > 0 and y > 0
assert 10 * (y + 10 * g) == 12 * 10 and 15 * (y + 6 * g) == 20 * 6
need = 24 * (y + 12 * g) / 12
hits = [k for k, v in OPTS.items() if v == need]
assert len(hits) == 1, (need, hits)

# 逐日模拟核对：need 人第12天末恰好采完，第11天末尚未采完
stock = 24 * y
for day in range(1, 13):
    stock += 24 * g - need
    if day == 11:
        assert stock > 0
assert stock == 0

# 干扰项来源核对
xs = [x for x in [F(k, 10) for k in range(0, 200)] if (12 - x) * 10 == (20 - x) * 6]   # 不按亩折算
assert len(xs) == 1 and (12 - xs[0]) * 10 / 12 + xs[0] == OPTS['A']
assert 24 * r1 / 12 == OPTS['C'] and 24 * r2 / 12 == OPTS['B']                       # 照搬每亩人·天数
print('g', g, 'y', y, 'need', need)
print(hits[0])
