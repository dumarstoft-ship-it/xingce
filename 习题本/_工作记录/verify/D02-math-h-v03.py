# D02-math-h-v03  基坑积水+地下水匀速渗入：10台18小时抽干，14台9小时抽干。
# 先开若干台，抽4小时后调走3台，剩下的又抽2小时恰好抽干。求开始时开动的台数。
from fractions import Fraction as F

OPTS = {'A': 13, 'B': 15, 'C': 16, 'D': 19}
(n1, h1), (n2, h2) = (10, 18), (14, 9)
A_H, K, B_H = 4, 3, 2

# 每台每小时抽水量记为1：原有积水 S + 渗水 x*h = 台数*h
x = F(n1 * h1 - n2 * h2, h1 - h2)
S = n1 * h1 - x * h1
assert x > 0 and S > 0 and S + x * h2 == n2 * h2


def drained_exactly(n, inflow_phase1=True, inflow_phase2=True):
    """逐分钟模拟坑内水量：要求第4+2小时末恰好抽干，且之前一直有水。"""
    if n - K <= 0:
        return False
    w = S
    steps = (A_H + B_H) * 60
    for minute in range(1, steps + 1):
        phase1 = minute <= A_H * 60
        pumps = n if phase1 else n - K
        inflow = x if (inflow_phase1 if phase1 else inflow_phase2) else 0
        w += F(inflow - pumps, 60)
        if minute < steps and w <= 0:
            return False
    return w == 0


sols = [n for n in range(1, 500) if drained_exactly(n)]
assert len(sols) == 1, sols
n = sols[0]
hits = [k for k, v in OPTS.items() if drained_exactly(v)]
assert len(hits) == 1 and OPTS[hits[0]] == n, hits
assert n not in (n1, n2)

# ---- 干扰项来源核对 ----
assert [m for m in range(1, 500) if drained_exactly(m, False, False)] == [OPTS['A']]  # 忘了这6小时新渗入的水
assert [m for m in range(1, 500) if drained_exactly(m, False, True)] == [OPTS['B']]   # 渗水只算后2小时
assert n - K == OPTS['C']                                                              # 答成调走后的台数

print('x', x, 'S', S, 'n', n)
print(hits[0])
