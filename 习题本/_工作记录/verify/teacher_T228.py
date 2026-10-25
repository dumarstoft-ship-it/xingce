# T228 正六面体表面积增加96%，棱长增加多少？
import math
area_factor = 1 + 0.96              # 表面积 S=6a^2 变为原来的 1.96 倍
edge_factor = math.sqrt(area_factor)  # 棱长倍数
increase = edge_factor - 1
options = {"A": 0.20, "B": 0.30, "C": 0.40, "D": 0.50}
hits = [k for k, v in options.items() if abs(v - increase) < 1e-9]
assert len(hits) == 1, hits
print(hits[0])
