# T242 圆柱容器(高45)底部有长方体铁块(高15)，6 分钟淹没铁块，再 16 分钟灌满，求铁块:容器体积
from fractions import Fraction as F
q = F(1)                    # 注水速度
H_c, H_i = F(45), F(15)
t1, t2 = F(6), F(16)
S = q * t2 / (H_c - H_i)    # 容器底面积：上面 30cm 用 16 分钟
s = S - q * t1 / H_i        # 铁块底面积：下面 15cm 净截面 S-s 用 6 分钟
ratio = (s * H_i) / (S * H_c)
options = {"A": F(1, 12), "B": F(1, 9), "C": F(1, 6), "D": F(1, 3)}
hits = [k for k, v in options.items() if v == ratio]
assert len(hits) == 1, (ratio, hits)
print(hits[0])
