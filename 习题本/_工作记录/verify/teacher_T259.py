# T259 半径 1 的圆上 A→B 弦长 1，B→C 弦长 2，求 AC 的最小可能值所在范围（枚举所有位置）
import math
pts = lambda th: (math.cos(th), math.sin(th))
dist = lambda p, q: math.hypot(p[0]-q[0], p[1]-q[1])
vals = []
A = pts(0.0)                                    # 由对称性固定 A
for sgnB in (1, -1):
    thB = sgnB * 2 * math.asin(1 / 2)           # 弦长 = 2 sin(θ/2)
    B = pts(thB)
    for sgnC in (1, -1):
        thC = thB + sgnC * 2 * math.asin(min(1.0, 2 / 2))
        C = pts(thC)
        assert abs(dist(B, C) - 2) < 1e-9
        vals.append(dist(A, C))
m = min(vals)
ranges = {"A": (0, 1), "B": (1, 1.3), "C": (1.3, 1.6), "D": (1.6, 2.0001)}
hits = [k for k, (lo, hi) in ranges.items() if lo < m < hi]
assert len(hits) == 1, (m, hits)
print(hits[0])
