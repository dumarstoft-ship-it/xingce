# T255x2（2023浙江C）大圆直径6切矩形三边，小圆直径2切两边，两圆外切，求矩形面积
import math
R, r = 3.0, 1.0
H = 2 * R                                 # 矩形宽 = 大圆直径
# 大圆心 (R, R)；小圆切上边和右边，圆心 (W-r, H-r)；圆心距 = R+r
dy = (H - r) - R
dx = math.sqrt((R + r) ** 2 - dy ** 2)
W = R + dx + r
area = W * H
s3 = math.sqrt(3)
options = {"A": 12 * (2 + s3), "B": 12 * (1 + 2 * s3), "C": 12 * math.sqrt(13), "D": 6 * (3 + math.sqrt(13))}
hits = [k for k, v in options.items() if abs(v - area) < 1e-9]
assert len(hits) == 1, (area, hits)
print(hits[0])
