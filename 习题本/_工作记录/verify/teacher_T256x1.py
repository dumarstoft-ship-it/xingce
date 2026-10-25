# T256x1（2025副省）矩形 ABCD，直角梯形 ABEF，DE 交 AB 于 G，AD=240，AF=150，AB=100，求 ADGF 面积（万平方米）
import math
def shoelace(pts):
    return abs(sum(pts[i][0]*pts[(i+1) % len(pts)][1] - pts[(i+1) % len(pts)][0]*pts[i][1] for i in range(len(pts)))) / 2
AD, AF, AB = 240.0, 150.0, 100.0
B = (0.0, 0.0); A = (0.0, AB); D = (AD, AB); C = (AD, 0.0)
vals = set()
for e in (30.0, 80.0, 120.0):                     # BE 未知，任取几种
    E = (-e, 0.0); Fp = (-e, AB + math.sqrt(AF**2 - e**2))
    t = AD / (AD + e)                             # DE 与 x=0 的交点参数
    G = (0.0, AB - t * AB)
    vals.add(round(shoelace([A, D, G, Fp]), 6))
assert len(vals) == 1, vals
area_wan = vals.pop() / 10000
options = {"A": 1.2, "B": 1.3, "C": 1.4, "D": 1.5}
hits = [k for k, v in options.items() if abs(v - area_wan) < 1e-9]
assert len(hits) == 1, (area_wan, hits)
print(hits[0])
