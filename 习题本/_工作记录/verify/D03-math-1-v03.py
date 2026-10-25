# D03-math-1-v03: 两车相向，相遇后甲又行16分钟到B站、乙又行25分钟到A站；甲每分钟200米；求A、B间道路长
from fractions import Fraction as F

VA, TA, TB = 200, 16, 25
OPTS = {'A': 4000, 'B': 7200, 'C': 8200, 'D': 9000}

def after_meet_times(vb, D):
    t = F(D) / (VA + vb)                 # 相遇时刻
    return (vb * t) / VA, (VA * t) / vb  # 甲走完乙相遇前的路、乙走完甲相遇前的路

sols = set()
# 穷举乙的速度（每分钟0.1~2000米，步长0.1）；对每个速度由“甲相遇后再行16分钟”确定道路长，再检验乙的25分钟
for k in range(1, 20001):
    vb = F(k, 10)
    D = F(TA * VA) * (VA + vb) / vb
    a, b = after_meet_times(vb, D)
    assert a == TA
    if b == TB:
        sols.add((vb, D))
assert len(sols) == 1, sols
vb, D = sols.pop()
# 用逐分钟模拟复核：两车相向行驶到相遇，再各自走到对方出发地
pa, pb, t = F(0), F(D), 0
while pa < pb:
    pa += VA; pb -= vb; t += 1
assert pa == pb and t == 20
assert (D - pa) / VA == TA and pb / vb == TB
hit = [k for k, v in OPTS.items() if v == D]
assert len(hit) == 1, (D, hit)
# 干扰项来源
assert VA * (TA + TB) == OPTS['C']                    # 16+25 当成甲全程用时
assert VA * (t + TB) == OPTS['D']                     # 误用乙相遇后的25分钟
assert VA * t == OPTS['A']                            # 只求出相遇前甲车走的路程
print('v乙 =', vb, '相遇时刻 =', t, 'D =', D)
print(hit[0])
