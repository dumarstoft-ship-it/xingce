# T265 飞镖板：阴影面积/板面积，哪种最接近 60%
import math
r = 1.0
tri_in_circle = 3 * math.sqrt(3) / 4 * r**2          # 圆内接正三角形
tri_out_circle = 3 * math.sqrt(3) * r**2             # 圆外切正三角形（内切圆半径 r）
sq_in_circle = 2 * r**2                              # 圆内接正方形
sq_out_circle = 4 * r**2                             # 圆外切正方形
circle = math.pi * r**2
p = {
    "A": tri_in_circle / circle,    # 圆板，阴影为内接正三角形
    "B": circle / tri_out_circle,   # 正三角形板，阴影为内切圆
    "C": sq_in_circle / circle,     # 圆板，阴影为内接正方形
    "D": circle / sq_out_circle,    # 正方形板，阴影为内切圆
}
best = min(p, key=lambda k: abs(p[k] - 0.60))
print(best)
