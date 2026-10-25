# T235 圆柱(底半径=2×高) → 半球，体积变为 9/16，求半径比
from fractions import Fraction as F
import math
R = F(4); h = R / 2                    # 任意赋值，比例不变
V_cyl = R**2 * h                       # 省略 π
V_hemi = F(9, 16) * V_cyl              # = (2/3) r^3
r3 = V_hemi * F(3, 2)
r = round(float(r3) ** (1/3), 12)
ratio = r / float(R)
options = {"A": 1/4, "B": 1/3, "C": 2/3, "D": 3/4}
hits = [k for k, v in options.items() if abs(v - ratio) < 1e-9]
assert len(hits) == 1, (ratio, hits)
print(hits[0])
