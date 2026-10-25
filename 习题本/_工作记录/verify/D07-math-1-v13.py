# D07-math-1-v13: 向东偏北行 15 千米后右转 90°，行至营地正东方向时距营地 25 千米；
# 保持方向继续行进，到与营地相距 39 千米还需行进多少千米
import math

LEG1, D_EAST, D_TARGET = 15, 25, 39

def where(theta, u):
    """第一段方向为东偏北 theta；右转 90° 后又行进 u 千米时的位置（营地为原点）"""
    p1 = (LEG1 * math.cos(theta), LEG1 * math.sin(theta))
    d2 = (math.sin(theta), -math.cos(theta))           # 右转 90°
    return (p1[0] + u * d2[0], p1[1] + u * d2[1])

def cross_east(theta):
    """第二段与正东方向射线（y=0, x>0）相交时已走的路程"""
    return LEG1 * math.sin(theta) / math.cos(theta)

# 二分求 theta：到达正东方向时与营地相距 D_EAST 千米
lo, hi = 1e-9, math.pi / 2 - 1e-9
for _ in range(200):
    mid = (lo + hi) / 2
    if where(mid, cross_east(mid))[0] < D_EAST:
        lo = mid
    else:
        hi = mid
theta = (lo + hi) / 2
u0 = cross_east(theta)
assert abs(where(theta, u0)[1]) < 1e-9 and abs(math.hypot(*where(theta, u0)) - D_EAST) < 1e-9

# 继续前进，二分求与营地相距 D_TARGET 千米时第二段的总路程
lo, hi = u0, 10000.0
for _ in range(200):
    mid = (lo + hi) / 2
    if math.hypot(*where(theta, mid)) < D_TARGET:
        lo = mid
    else:
        hi = mid
extra = (lo + hi) / 2 - u0
opts = {"A": 14, "B": 16, "C": 20, "D": 36}
hit = [k for k, v in opts.items() if abs(v - extra) < 1e-6]
assert len(hit) == 1, (extra, hit)
print('转弯后已走 ≈', round(u0, 6), '还需 ≈', round(extra, 6))
print(hit[0])
