# D07-math-1-v04: 半径 6、水深 9 的圆柱量杯里的水倒入口径 18 的圆锥漏斗恰好装满，求漏斗高
import math

R_CUP, DEPTH = 6, 9
D_FUNNEL = 18
water = math.pi * R_CUP ** 2 * DEPTH
R = D_FUNNEL / 2

def cone_volume(h, n=4000):
    """圆盘法：从尖端到口部，截面半径由 0 线性增大到 R"""
    dz = h / n
    return sum(math.pi * (R * (i + 0.5) / n) ** 2 * dz for i in range(n))

lo, hi = 0.0, 500.0
for _ in range(60):
    mid = (lo + hi) / 2
    if cone_volume(mid) < water:
        lo = mid
    else:
        hi = mid
h = (lo + hi) / 2
opts = {'A': 3, 'B': 4, 'C': 12, 'D': 27}
hit = [k for k, v in opts.items() if abs(v - h) < 1e-3]
assert len(hit) == 1, (h, hit)
print('漏斗高 ≈', round(h, 6))
print(hit[0])
