import math
from fractions import Fraction as F
# 张从丙地正西 X km 处向东，李从丙地正北 Y km 处向南，同时出发，速度 a、b（整数 km/h）
# 1 小时后两人都未到丙地且距离为整数 d1；T2 小时后两人都已过丙地且距离为整数 d2
c = []
for X in range(6, 40):
    for Y in range(4, 40):
        for a in range(2, 16):
            for b in range(1, 16):
                if a == b: continue
                if not (X - a > 0 and Y - b > 0): continue
                d1 = math.hypot(X - a, Y - b)
                if abs(d1 - round(d1)) > 1e-9: continue
                for T2 in [3, 4, 5]:
                    if not (T2 * a > X and T2 * b > Y): continue
                    d2 = math.hypot(T2 * a - X, T2 * b - Y)
                    if abs(d2 - round(d2)) > 1e-9: continue
                    r = F(b, a)
                    late = (F(X, a) - F(Y, b)) * 60
                    if r.denominator <= 5 and late != 0:
                        c.append((X, Y, a, b, str(r), round(d1), T2, round(d2), float(late)))
for x in c[:40]:
    print('西距%d 北距%d 张%d 李%d 李/张=%s 1h距%d T2=%d T2距%d 张比李晚到丙(分)=%.1f' % x)
print(len(c))
