# D03-math-1-v04: 全程300千米；乙先行半小时，提速24千米/时后再行2.5小时，与匀速的甲同时到达；甲比乙原速快百分之几
from fractions import Fraction as F

D, T1, T2, DV = 300, F(1, 2), F(5, 2), 24
OPTS = {'A': F(20), 'B': F(25), 'C': F(30), 'D': F(50)}   # 百分数

sols = set()
# 穷举乙的原速度（0.1千米/时步长）与甲的速度（0.1步长），检验两车同时到达
for k in range(1, 2001):
    v = F(k, 10)
    if T1 * v + T2 * (v + DV) != D:
        continue
    for m in range(1, 3001):
        va = F(m, 10)
        if F(D) / va == T1 + T2:            # 甲匀速，到达时间与乙相同
            sols.add((v, va))
assert len(sols) == 1, sols
v, va = sols.pop()
pct = (va - v) / v * 100
hit = [k for k, x in OPTS.items() if x == pct]
assert len(hit) == 1, (pct, hit)
# 干扰项来源
assert (va - v) / va * 100 == OPTS['A']            # 以甲为基准
assert F(DV) / v * 100 == OPTS['C']                # 乙的提速幅度
va_wrong = F(D) / T2                               # 漏掉乙先行的半小时，甲用时算成2.5小时
assert (va_wrong - v) / v * 100 == OPTS['D']
print('乙原速', v, '甲', va, '快', pct, '%')
print(hit[0])
