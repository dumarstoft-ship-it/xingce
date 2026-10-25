# T264 A、B 在公路同侧，距公路 3、7，AB=8.5；公路上选 C 使 AC+BC 最小；
# 货车从 C 出发给两村送货后回到 C，速度 60km/h，最少用时（分钟）
import math
a, b, AB = 3.0, 7.0, 8.5
w = math.sqrt(AB**2 - (b - a)**2)          # 两村沿公路方向的距离
A = (0.0, a); B = (w, b)
dist = lambda p, q: math.hypot(p[0]-q[0], p[1]-q[1])
# 数值求 C（公路 y=0 上）使 AC+BC 最小
xs = [-5 + i * (w + 10) / 400000 for i in range(400001)]
cx = min(xs, key=lambda x: dist((x, 0), A) + dist((x, 0), B))
C = (cx, 0.0)
s = dist(C, A) + dist(C, B)
route = min(dist(C, A) + AB + dist(B, C),            # C→A→B→C
            2 * dist(C, A) + 2 * dist(C, B))           # C→A→C→B→C
minutes = route / 60 * 60
options = {"A": 18, "B": 21, "C": 24, "D": 27}
best = min(options, key=lambda k: abs(options[k] - minutes))
assert abs(options[best] - minutes) < 0.01, minutes
print(best)
