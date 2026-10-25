# D02-math-h-v05  按计划匀速施工可如期完工；前一半工程量效率提高40%，后一半工程量效率降低40%，
# 结果推迟4天。求原计划工期。
from fractions import Fraction as F

OPTS = {'A': 21, 'B': 25, 'C': 30, 'D': 70}
P, DELAY = F(40, 100), 4


def delay(T, t1=None, t2=None):
    """原计划T天、每天完成1份（总量T份）；两半工程量各 T/2 份。t1、t2 为两段实际用时的算法。"""
    half = F(T, 2)
    first = t1(half) if t1 else half / (1 + P)
    second = t2(half) if t2 else half / (1 - P)
    return first + second - T


# 以半天为步长扫描 0.5~1000 天
sols = [F(n, 2) for n in range(1, 2001) if delay(F(n, 2)) == DELAY]
assert len(sols) == 1, sols
T = sols[0]
hits = [k for k, v in OPTS.items() if delay(v) == DELAY]
assert len(hits) == 1 and OPTS[hits[0]] == T, hits

# ---- 干扰项来源核对 ----
scan = lambda **kw: [F(n, 2) for n in range(1, 2001) if delay(F(n, 2), **kw) == DELAY]
assert scan(t1=lambda h: h * (1 - P)) == [OPTS['C']]           # 效率提高40%当成时间减少40%
assert scan(t2=lambda h: h * (1 + P)) == [OPTS['D']]           # 效率降低40%当成时间增加40%
assert DELAY / (1 - (1 + P) * (1 - P)) == OPTS['B']             # 整体效率0.84当成时间增加16%
assert T + DELAY == OPTS['B']                                   # 25 也是实际工期

print('T', T)
print(hits[0])
