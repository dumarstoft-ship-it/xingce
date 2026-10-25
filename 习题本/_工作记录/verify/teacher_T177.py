# T177（2022重庆选调）预算400万元，4家平均报价为预算95%；只有甲超过预算；任意2家相差∈[10,100]万元。求甲最高报价。
# 以0.5万元为单位（选项精度）穷举；再以0.25万元为单位复核最大值不变，排除网格造成的偏差。
from fractions import Fraction as F

BUDGET, N, RATE, DMIN, DMAX = 400, 4, F(95, 100), 10, 100
OPTS = {'A': F(440), 'B': F(885, 2), 'C': F(445), 'D': F(895, 2)}


def max_jia(unit):
    u = 1 / unit                       # 每万元的格点数
    tot = int(BUDGET * RATE * N * u)
    bud, dmin, dmax = int(BUDGET * u), int(DMIN * u), int(DMAX * u)
    for a in range(tot, bud, -1):      # 甲必须超过预算
        lo = a - dmax                  # 其余各家与甲相差不超过100
        for b in range(lo, bud + 1):
            for c in range(b + dmin, bud + 1):
                d = tot - a - b - c
                if d < c + dmin or d > bud:
                    continue
                xs = [a, b, c, d]
                if all(dmin <= abs(x - y) <= dmax for i, x in enumerate(xs) for y in xs[i + 1:]):
                    return F(a) / F(u)
    return None


best = max_jia(F(1, 2))
assert max_jia(F(1, 4)) == best
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1, (best, hits)
print('max price of 甲 =', float(best))
print(hits[0])
