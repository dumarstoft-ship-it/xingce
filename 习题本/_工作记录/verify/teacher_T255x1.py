# T255x1（2021青海）圆岛边缘起火，火线是以起火点为圆心的圆弧，烧到岛中心时过火面积占比
import math
r = 1.0
N = 1500
cnt = inside = 0
for i in range(N):
    x = -r + (i + 0.5) * 2 * r / N
    for j in range(N):
        y = -r + (j + 0.5) * 2 * r / N
        if x * x + y * y <= r * r:                 # 岛（圆心在原点）
            inside += 1
            if x * x + (y + r) ** 2 <= r * r:      # 起火点 (0,-r)，火线半径 = r（刚到岛中心）
                cnt += 1
p_num = cnt / inside
p_exact = (2 * math.pi / 3 - math.sqrt(3) / 2) / math.pi
assert abs(p_num - p_exact) < 0.002
options = {"A": 0.45, "B": 0.40, "C": 0.35, "D": 0.30}
best = min(options, key=lambda k: abs(options[k] - p_exact))
print(best)
