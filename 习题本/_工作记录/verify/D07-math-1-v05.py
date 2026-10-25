# D07-math-1-v05: 从正方体上平行于一个面切下厚 0.5 的一片，剩余部分表面积比原来少 24，求原棱长
from fractions import Fraction as F
import math

T, DEC = F(1, 2), 24

def surface(a, b, c):
    return 2 * (a * b + b * c + c * a)

sols = []
for k in range(11, 4001):              # 以 0.05 为步长穷举棱长 x（须大于 0.5）
    x = F(k, 20)
    if surface(x, x, x) - surface(x, x, x - T) == DEC:
        sols.append(x)
assert len(sols) == 1, sols
x = sols[0]
opts = {'A': 4, 'B': 2 * math.sqrt(6), 'C': 6, 'D': 12}
hit = [k for k, v in opts.items() if abs(v - float(x)) < 1e-9]
assert len(hit) == 1, (x, hit)
print('原棱长 =', x)
print(hit[0])
