# T241 圆锥 h=6√3, r=6，A、B 为底面直径两端，沿侧面最短路程
import math
h, r = 6 * math.sqrt(3), 6.0
l = math.hypot(h, r)                       # 母线
sector = 2 * math.pi * r / l               # 展开扇形圆心角（弧度）
arc_AB = math.pi * r                       # A、B 间底面弧长（半周）
ang = arc_AB / l                           # 在扇形中对应的圆心角
assert ang <= math.pi                      # 展开后可直接连线
dist = 2 * l * math.sin(ang / 2)
options = {"A": 12.0, "B": 12 * math.sqrt(2), "C": 6 * math.pi, "D": 24.0}
hits = [k for k, v in options.items() if abs(v - dist) < 1e-9]
assert len(hits) == 1, (dist, hits)
print(hits[0])
