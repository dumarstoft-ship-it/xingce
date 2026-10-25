# D03-math-1-v11: 两队相距9千米相向而行，甲队5千米/时；出发15分钟后无人机从甲队起飞，40千米/时在两队间往返，相遇时共飞30千米；求乙队速度
from fractions import Fraction as F

DIST, VA, DELAY, VD, FLY = 9, 5, F(15, 60), 40, 30
OPTS = {'A': 4, 'B': 7, 'C': 9, 'D': 12}

def drone_distance(vb):
    """逐段模拟无人机往返（事件驱动，精确分数），返回两队相遇前无人机飞行的总路程"""
    t = DELAY
    pa, pb = VA * t, DIST - vb * t        # 起飞时两队位置（甲队从0出发，乙队从9出发）
    pd, direction = pa, +1                # 无人机从甲队上空起飞，先飞向乙队
    total = F(0)
    for _ in range(200):
        if pb - pa <= F(1, 10**12):
            break
        if direction > 0:                 # 飞向乙队：相向
            dt = (pb - pd) / (VD + vb)
        else:                             # 飞回甲队：相向
            dt = (pd - pa) / (VD + VA)
        t_meet = (pb - pa) / (VA + vb)    # 剩余的两队相遇时间
        dt = min(dt, t_meet)
        total += VD * dt
        pa += VA * dt; pb -= vb * dt; pd += direction * VD * dt
        direction = -direction
    # 余下极短时间的飞行补齐（两队实际相遇时刻）
    t_total = DIST / F(VA + vb)
    return total, VD * (t_total - DELAY)

sols = set()
for k in range(1, 401):                   # 乙队速度 0.05~20 千米/时，步长 0.05
    vb = F(k, 20)
    exact = VD * (DIST / F(VA + vb) - DELAY)      # 无人机飞行时间 = 相遇时刻 − 起飞时刻
    if exact == FLY:
        sim, _ = drone_distance(vb)
        assert abs(sim - exact) < F(1, 10**6)     # 逐段模拟与整体计算一致
        sols.add(vb)
assert len(sols) == 1, sols
vb = sols.pop()
hit = [k for k, v in OPTS.items() if v == vb]
assert len(hit) == 1, (vb, hit)
# 干扰项来源
t_wrong = F(FLY, VD)                              # 忽略晚起飞的15分钟
assert DIST / t_wrong - VA == OPTS['B']
assert VA + vb == OPTS['C']                       # 求成速度和
assert DIST / t_wrong == OPTS['D']                # 两处都错
print('乙队速度', vb)
print(hit[0])
