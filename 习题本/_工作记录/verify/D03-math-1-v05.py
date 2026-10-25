# D03-math-1-v05: 全程降速1/6晚到12分钟；先按原速行20千米再降速1/6晚到8分钟；求全程
from fractions import Fraction as F

CUT = F(1, 6)                 # 车速降低 1/6
LATE_ALL, LATE_PART = F(12, 60), F(8, 60)   # 小时
X = 20                        # 先按原速行驶的千米数
OPTS = {'A': 30, 'B': 40, 'C': 50, 'D': 60}

sols = set()
# 穷举全程 S（0.5千米步长，至 300 千米）与原速 v（0.5千米/时步长，至 150）
for s2 in range(1, 601):
    S = F(s2, 2)
    if S <= X:
        continue
    for v2 in range(1, 301):
        v = F(v2, 2)
        slow = v * (1 - CUT)
        t0 = S / v
        if S / slow - t0 != LATE_ALL:
            continue
        if X / v + (S - X) / slow - t0 == LATE_PART:
            sols.add((S, v))
assert len(sols) == 1, sols
S, v = sols.pop()
hit = [k for k, x in OPTS.items() if x == S]
assert len(hit) == 1, (S, hit)
# 干扰项来源
assert X * F(12, 8) == OPTS['A']               # 比例用反：20×12÷8
assert S - X == OPTS['B']                      # 求成后段路程
assert X + X * F(12, 8) == OPTS['C']           # 把 8:12 当成前段:后段
print('S =', S, 'v =', v)
print(hit[0])
