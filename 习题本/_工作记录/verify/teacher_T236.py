# T236 帐篷屋顶：底 4×3，高 1，上棱 2（平行于长边、居中）。用水平截面积分求体积
from fractions import Fraction as F
a, b, c, H = F(4), F(3), F(2), F(1)
# 高度 z 处的截面：长 a-(a-c)z/H，宽 b(1-z/H)，A(z) 为二次多项式，用 Simpson 公式精确积分
def A(z):
    return (a - (a - c) * z / H) * (b * (1 - z / H))
V = H / 6 * (A(0) + 4 * A(H / 2) + A(H))
# 割补法交叉验证：中间三棱柱 + 两端四棱锥
V2 = F(1, 2) * b * H * c + F(1, 3) * (a - c) * b * H
assert V == V2
options = {"A": F(5), "B": F(11), "C": F(12), "D": F(24)}
hits = [k for k, v in options.items() if v == V]
assert len(hits) == 1, (V, hits)
print(hits[0])
