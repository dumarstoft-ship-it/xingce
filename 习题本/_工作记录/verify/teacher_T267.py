# T267 12:15–13:15 随机开始午睡，时长 0–60 分钟随机，14:00 之后起床的概率
from fractions import Fraction as F
T = 60                       # 入睡时刻 x∈[0,60]（12:15 起算），时长 y∈[0,60]
target = 105                 # 14:00 距 12:15 为 105 分钟
leg = 2 * T - target         # x+y>105 在正方形右上角截出的等腰直角三角形直角边
p = F(leg * leg, 2) / (T * T)
N = 1200
cnt = sum(1 for i in range(N) for j in range(N) if (i + .5) * T / N + (j + .5) * T / N > target)
assert abs(cnt / N**2 - float(p)) < 0.002
options = {"A": F(1, 16), "B": F(1, 32), "C": F(1, 48), "D": F(1, 64)}
hits = [k for k, v in options.items() if v == p]
assert len(hits) == 1, (p, hits)
print(hits[0])
