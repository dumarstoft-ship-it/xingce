# D03-math-1-v13: 甲每小时比乙多4千米；出发2.5小时后甲休息40分钟再按原速骑；乙要在途中追上甲，速度至少多少
from fractions import Fraction as F

DV, RIDE1, REST = 4, F(5, 2), F(40, 60)
OPTS = {'A': F(6), 'B': F(15), 'C': F(19), 'D': F(25)}

def pos_jia(t, va):
    if t <= RIDE1:
        return va * t
    if t <= RIDE1 + REST:
        return va * RIDE1
    return va * (t - REST)

def catches(vb, horizon=200):
    """乙（速度 vb）在 (0, horizon] 小时内是否与甲到达同一位置；位置差分段线性，检查所有折点和细分点"""
    va = vb + DV
    pts = {RIDE1, RIDE1 + REST, F(horizon)}
    pts |= {F(i, 12) for i in range(1, 12 * horizon + 1)}   # 每 5 分钟采样一次
    return any(vb * t >= pos_jia(t, va) for t in pts if t > 0)

# 在 0.01 千米/时的网格上找能追上的最小速度
cands = [F(k, 100) for k in range(1, 5001)]
lo, hi = 0, len(cands) - 1
assert not catches(cands[lo]) and catches(cands[hi])
# 能否追上关于速度单调：先验证单调性（抽样），再二分
for k in range(0, 5000, 50):
    if catches(cands[k]):
        assert all(catches(cands[j]) for j in range(k, min(k + 50, 5000), 7))
while hi - lo > 1:
    mid = (lo + hi) // 2
    if catches(cands[mid]): hi = mid
    else: lo = mid
vmin = cands[hi]
assert catches(vmin) and not catches(vmin - F(1, 100))
ok = [k for k, v in OPTS.items() if catches(v)]
hit = [k for k, v in OPTS.items() if v == vmin]
assert len(hit) == 1, (vmin, hit)
assert min(OPTS[k] for k in ok) == vmin          # “至少”取能追上的最小值
# 干扰项来源
assert F(DV) / REST == OPTS['A']                         # 领先只算1小时的4千米
assert DV * (RIDE1 + REST) / REST == OPTS['C']           # 把休息时间也算进领先时间
assert DV * RIDE1 / F(4, 10) == OPTS['D']                # 40分钟误作0.4小时
print('最低速度', vmin, '能追上的选项', ok)
print(hit[0])
