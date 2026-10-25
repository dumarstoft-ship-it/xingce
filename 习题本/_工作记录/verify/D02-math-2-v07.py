# D02-math-2-v07：甲岸桥单独24小时、乙48小时，原计划同时作业。同时6小时后乙停机维修r小时（甲照常），
# 修好后乙效率降低50%，再一起作业到卸完，比原计划晚3小时。求r。
# 解法：对r按1/4小时枚举，分段精确模拟完工时刻，找出恰好晚3小时的那个r。
from fractions import Fraction as F

OPTIONS = {'A': 1, 'B': 3, 'C': 5, 'D': 9}
rA, rB = F(1, 24), F(1, 48)
t1, drop, late = 6, F(1, 2), 3
plan = 1 / (rA + rB)


def finish(r):
    done = (rA + rB) * t1
    if done >= 1 or done + rA * r >= 1:   # 维修前或维修期间就完工，与题意不符
        return None
    done += rA * r
    rate = rA + rB * (1 - drop)
    return t1 + r + (1 - done) / rate


sols = [F(q, 4) for q in range(1, 200) if finish(F(q, 4)) == plan + late]
assert len(sols) == 1, sols
r = sols[0]
hits = [k for k, v in OPTIONS.items() if v == r]
assert len(hits) == 1
# 干扰项：维修期间漏算甲→1；忽略降效→9；"晚几小时就修几小时"→3
T = plan + late
assert (T - t1) - (1 - (rA + rB) * t1) / (rA + rB * (1 - drop)) == OPTIONS['A']
assert ((rA + rB) * T - 1) / rB == OPTIONS['D']
assert late == OPTIONS['B']
print('原计划', plan, '小时，维修', r, '小时')
print(hits[0])
