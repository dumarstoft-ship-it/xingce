# T250 灯高：人高 1.6，影长 3.2；前进 1 米后影长 1.6
from fractions import Fraction as F
h, s1, s2, step = F(16, 10), F(32, 10), F(16, 10), F(1)
# 未知：灯高 x、开始时人到灯脚距离 d
# x/h = (d + s1)/s1  ->  d = x*s1/h - s1
# x/h = (d - step + s2)/s2 -> d = x*s2/h - s2 + step
# 线性方程：x*(s1-s2)/h = s1 - s2 + step
x = (s1 - s2 + step) * h / (s1 - s2)
d = x * s1 / h - s1
assert d > step
options = {"A": F(26, 10), "B": F(28, 10), "C": F(32, 10), "D": F(34, 10)}
hits = [k for k, v in options.items() if v == x]
assert len(hits) == 1, (x, hits)
print(hits[0])
