# real 2026ZJA-55: 向东偏南行 60 千米后左转 90°，再行 45 千米到营地正东方向；保持方向再行 35 千米，求与营地距离
import math

LEG1, LEG2, MORE = 60, 45, 35

def where(theta, u):
    """第一段方向为东偏南 theta；左转 90° 后又行进 u 千米时的位置（营地为原点）"""
    p1 = (LEG1 * math.cos(theta), -LEG1 * math.sin(theta))
    d2 = (math.sin(theta), math.cos(theta))            # 左转 90°
    return (p1[0] + u * d2[0], p1[1] + u * d2[1])

# 二分求 theta：左转后行 45 千米恰到营地正东方向（y=0）
lo, hi = 1e-9, math.pi / 2 - 1e-9
for _ in range(200):
    mid = (lo + hi) / 2
    if where(mid, LEG2)[1] > 0:       # 已越过东西线，说明 theta 偏小
        lo = mid
    else:
        hi = mid
theta = (lo + hi) / 2
p2 = where(theta, LEG2)
assert abs(p2[1]) < 1e-9 and p2[0] > 0
d = math.hypot(*where(theta, LEG2 + MORE))
opts = {'A': 80, 'B': 90, 'C': 100, 'D': 120}
hit = [k for k, v in opts.items() if abs(v - d) < 1e-6]
assert len(hit) == 1, (d, hit)
print('到达正东方向时距营地 ≈', round(p2[0], 6), '；再行 35 千米后距营地 ≈', round(d, 6))
print(hit[0])
