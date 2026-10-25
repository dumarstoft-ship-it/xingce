# T237x1（2024河北）圆锥容器口径300mm、深400mm，接雨水深200mm，求日降雨量等级
import math
D_top, H, h_w = 300.0, 400.0, 200.0
R = D_top / 2
r_w = R * h_w / H                                  # 水面半径（相似）
V_w = math.pi * r_w**2 * h_w / 3                   # 雨水体积
w = V_w / (math.pi * R**2)                         # 摊在容器口面积上的水深
levels = {"D": (0.1, 10), "C": (10, 25), "B": (25, 50), "A": (50, 100)}   # D小雨 C中雨 B大雨 A暴雨
hits = [k for k, (lo, hi) in levels.items() if lo <= w < hi]
assert len(hits) == 1, (w, hits)
print(hits[0])
