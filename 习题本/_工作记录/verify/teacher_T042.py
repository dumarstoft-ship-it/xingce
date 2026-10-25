# 验算 T042：分三段行驶，最后 40 分钟匀加速，求最后 10 分钟平均速度是计划速度的几倍
import sys
from fractions import Fraction as F
V = F(1)                  # 计划速度（每分钟）
total = V * 120           # 计划 2 小时
s1 = V * 30               # 头 30 分钟按计划速度
s2 = s1                   # 拥堵 50 分钟，路程与前 30 分钟相同
v2 = s2 / 50              # 拥堵段默认匀速
s3 = total - s1 - s2      # 最后 40 分钟的路程
T3 = 40
a = (s3 - v2 * T3) * 2 / (T3 * T3)   # 匀加速，初速 v2
v_at = lambda x: v2 + a * x
assert v_at(0) * T3 + a * T3 * T3 / 2 == s3
last10 = (v_at(30) + v_at(40)) / 2
ratio = last10 / V
if ratio < F(18, 10):
    letter = 'A'
elif ratio < 2:
    letter = 'B'
elif ratio <= F(22, 10):
    letter = 'C'
else:
    letter = 'D'
print(f'末速度={v_at(40)}V，最后10分钟平均={ratio}V={float(ratio)}', file=sys.stderr)
print(letter)
