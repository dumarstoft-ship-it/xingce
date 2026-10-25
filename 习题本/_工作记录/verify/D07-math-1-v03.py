# D07-math-1-v03: 半径 0.3 米的圆形机器人贴着 8×5 矩形花坛外沿绕行一周，求中心路程
# 做法：中心轨迹 = 到矩形距离恰为 0.3 的点集；从矩形中心沿各方向二分求出轨迹点，折线求长
import math

L, W, R = 8.0, 5.0, 0.3

def dist_to_rect(x, y):            # 矩形以原点为中心
    dx = max(abs(x) - L / 2, 0.0)
    dy = max(abs(y) - W / 2, 0.0)
    return math.hypot(dx, dy)

def track_point(phi):
    c, s = math.cos(phi), math.sin(phi)
    lo, hi = 0.0, 20.0
    for _ in range(55):
        mid = (lo + hi) / 2
        if dist_to_rect(mid * c, mid * s) < R:
            lo = mid
        else:
            hi = mid
    return (lo * c, lo * s)

N = 40000
pts = [track_point(2 * math.pi * i / N) for i in range(N)]
length = sum(math.dist(pts[i], pts[(i + 1) % N]) for i in range(N))
opts = {'A': 26, 'B': 26 + 0.6 * math.pi, 'C': 28.4, 'D': 26 + 1.2 * math.pi}
hit = [k for k, v in opts.items() if abs(v - length) < 1e-3]
assert len(hit) == 1, (length, hit)
print('中心路程 ≈', round(length, 6))
print(hit[0])
