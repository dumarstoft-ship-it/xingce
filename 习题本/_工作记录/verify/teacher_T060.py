# 验算 T060：相邻两次成 90° 的最短间隔（枚举一天内所有直角时刻）
import sys
from fractions import Fraction as F
times = []
for target in (90, 270):
    k = 0
    while True:
        t = (target + 360 * k) / F(11, 2)
        if t >= 24 * 60:
            break
        times.append(t)
        k += 1
times.sort()
gap = min(b - a for a, b in zip(times, times[1:]))
options = {'A': F(30), 'B': F(315, 10), 'C': F(322, 10), 'D': F(327, 10)}
best = min(options, key=lambda k: abs(options[k] - gap))
print(f'最短间隔={gap}≈{float(gap):.3f}分钟', file=sys.stderr)
print(best)
