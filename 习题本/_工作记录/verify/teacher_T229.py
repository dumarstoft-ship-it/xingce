# T229 三视图零件：空心圆锥(无底, r=1, h=2) + 圆环(外半径3, 内半径1)，内外都涂油
import math
r, h = 1.0, 2.0          # 圆锥底面半径、高（主视图中间三角形底 2cm、高 2cm）
R_out = r + 2.0          # 圆环外半径：两侧各伸出 2cm
l = math.hypot(r, h)     # 母线
cone_lateral = math.pi * r * l
ring = math.pi * (R_out**2 - r**2)
total = 2 * (cone_lateral + ring)          # 厚度不计，每个面内外各一次
s5 = math.sqrt(5)
options = {"A": (16 + 2*s5) * math.pi, "B": (18 + 2*s5) * math.pi, "C": 22 * math.pi, "D": 20 * math.pi}
hits = [k for k, v in options.items() if abs(v - total) < 1e-9]
assert len(hits) == 1, hits
print(hits[0])
