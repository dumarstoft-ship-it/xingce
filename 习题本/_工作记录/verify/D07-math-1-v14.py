# D07-math-1-v14: 甲在乙北偏东 30° 6 千米，丙在乙南偏东 60° 8 千米，求到三村等距的点到各村的距离
import math

def pos(bearing_deg, dist):
    t = math.radians(bearing_deg)
    return (dist * math.sin(t), dist * math.cos(t))

yi = (0.0, 0.0)
jia = pos(30, 6)
bing = pos(180 - 60, 8)
# 到三点等距：|P-yi|²=|P-jia|²=|P-bing|²，化为两个线性方程求解
(x1, y1), (x2, y2), (x3, y3) = yi, jia, bing
a1, b1, c1 = 2 * (x2 - x1), 2 * (y2 - y1), x2 ** 2 + y2 ** 2 - x1 ** 2 - y1 ** 2
a2, b2, c2 = 2 * (x3 - x1), 2 * (y3 - y1), x3 ** 2 + y3 ** 2 - x1 ** 2 - y1 ** 2
det = a1 * b2 - a2 * b1
P = ((c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det)
r = math.dist(P, yi)
assert abs(math.dist(P, jia) - r) < 1e-9 and abs(math.dist(P, bing) - r) < 1e-9
opts = {'A': 2, 'B': 4.8, 'C': 5, 'D': 10}
hit = [k for k, v in opts.items() if abs(v - r) < 1e-9]
assert len(hit) == 1, (r, hit)
print('等距点', P, '距离 ≈', round(r, 6))
print(hit[0])
