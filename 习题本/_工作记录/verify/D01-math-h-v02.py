# D01-math-h-v02  助农直播连续4场订单：第二场比第一场少20%，第三场比前两场之和少30单，
# 第四场比第一场的1.5倍多15单；订单最多的一场比最少的一场多50单。求4场订单总数。
from fractions import Fraction as F

OPTS = {'A': 90, 'B': 240, 'C': 342, 'D': 393}
LESS2 = F(20, 100)          # 第二场比第一场少20%
C3 = 30                     # 第三场比前两场之和少30单
K4, D4 = F(3, 2), 15        # 第四场比第一场的1.5倍多15单
GAP = 50                    # 最多比最少多50单
N = 20000


def days(x):
    d1 = F(x)
    d2 = d1 * (1 - LESS2)
    d3 = d1 + d2 - C3
    d4 = K4 * d1 + D4
    return [d1, d2, d3, d4]


def valid(ds):
    return all(d.denominator == 1 and d > 0 for d in ds)


# 穷举第一场订单量x，四场都须为正整数，用实际的最大值、最小值检验
sols = []
for x in range(1, N + 1):
    ds = days(x)
    if valid(ds) and max(ds) - min(ds) == GAP:
        sols.append((x, [int(d) for d in ds]))
assert len(sols) == 1, sols
x, ds = sols[0]
total = sum(ds)
hits = [k for k, v in OPTS.items() if v == total]
assert len(hits) == 1, hits


# 干扰项来源核对：先认定“最多/最少是哪一场”列式求x，却不回代检验
def assumed(imax, imin):
    out = []
    for xx in range(1, N + 1):
        ds2 = days(xx)
        if valid(ds2) and ds2[imax] - ds2[imin] == GAP:
            out.append([int(d) for d in ds2])
    return out


r = assumed(2, 1)                    # 按系数认定第三场最多（最少为第二场）
assert len(r) == 1 and max(r[0]) != r[0][2] and sum(r[0]) == OPTS['D'], r
r = assumed(3, 0)                    # 照搬“第一场最少、第四场最多”
assert len(r) == 1 and min(r[0]) != r[0][0] and sum(r[0]) == OPTS['C'], r
assert max(ds) == OPTS['A']          # 答成订单最多的一场
print('x', x, 'days', ds, 'total', total)
print(hits[0])
