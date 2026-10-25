# T255x3（2021内蒙古）边长50的正三角形内三个等圆两两相切且各切一边，求三圆外侧弧总长
import math
a = 50.0
inr = a / (2 * math.sqrt(3))              # 中心到边的距离
# 圆心距中心 2r/√3，且圆心到所切边距离 r：inr = 2r/√3 + r
r = inr / (2 / math.sqrt(3) + 1)
# 数值复核：底边 y=0，中心 (25, inr)，下方圆心 (25, r)
O = (a / 2, inr)
cs = [(O[0] + (2*r/math.sqrt(3)) * math.sin(t), O[1] - (2*r/math.sqrt(3)) * math.cos(t)) for t in (0, 2*math.pi/3, -2*math.pi/3)]
for i in range(3):
    for j in range(i + 1, 3):
        assert abs(math.dist(cs[i], cs[j]) - 2 * r) < 1e-9          # 两两外切
def dist_line(p, q1, q2):
    (x0, y0), (x1, y1), (x2, y2) = p, q1, q2
    return abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1) / math.dist(q1, q2)
V = [(0.0, 0.0), (a, 0.0), (a / 2, a * math.sqrt(3) / 2)]
for c in cs:
    assert min(dist_line(c, V[i], V[(i+1) % 3]) for i in range(3)) - r > -1e-9  # 都在三角形内
    assert abs(min(dist_line(c, V[i], V[(i+1) % 3]) for i in range(3)) - r) < 1e-9  # 各切一边
arc_total = 3 * (300 / 360) * 2 * math.pi * r        # 每圆两切点间内弧 60°，走外侧 300°
options = {"A": 95, "B": 105, "C": 115, "D": 125}
best = min(options, key=lambda k: abs(options[k] - arc_total))
assert abs(options[best] - arc_total) < 2, arc_total
print(best)
