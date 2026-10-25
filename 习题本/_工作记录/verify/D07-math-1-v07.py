# D07-math-1-v07: 水箱内底 40×30，水深 8；放入棱长 20 的正方体铁块沉底，求水面升高
# 做法：二分水面高度 h，使“水箱中 h 以下的空间 − 铁块占去的部分”恰好等于原有水量
L, W, D0, A = 40, 30, 8, 20
water = L * W * D0

def capacity_below(h):
    return L * W * h - A * A * min(h, A)

lo, hi = 0.0, 1000.0
for _ in range(100):
    mid = (lo + hi) / 2
    if capacity_below(mid) < water:
        lo = mid
    else:
        hi = mid
h = (lo + hi) / 2
rise = h - D0
opts = {'A': 8 / 3, 'B': 4, 'C': 20 / 3, 'D': 12}
hit = [k for k, v in opts.items() if abs(v - rise) < 1e-6]
assert len(hit) == 1, (rise, hit)
print('新水深 ≈', round(h, 6), '升高 ≈', round(rise, 6), '铁块露出水面' if h < A else '铁块被淹没')
print(hit[0])
