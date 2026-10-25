# T257 A 在 B 正北 x 千米；甲从 A 向南 4km/h，乙从 B 向西 8km/h，20 分钟后相距 x，求 x
from fractions import Fraction as F
t = F(20, 60)
s_jia, s_yi = 4 * t, 8 * t
# (x - s_jia)^2 + s_yi^2 = x^2  ->  -2 s_jia x + s_jia^2 + s_yi^2 = 0
x = (s_jia**2 + s_yi**2) / (2 * s_jia)
assert (x - s_jia)**2 + s_yi**2 == x**2
options = {"A": F(5, 3), "B": F(6), "C": F(3), "D": F(10, 3)}
hits = [k for k, v in options.items() if v == x]
assert len(hits) == 1, (x, hits)
print(hits[0])
