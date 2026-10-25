# T237 圆锥景观露出 3 米；水深减少 20%，露出体积增加 61/64，求原水深
from fractions import Fraction as F
exposed = F(3)
vol_ratio = 1 + F(61, 64)              # = 125/64
# 相似比 = 体积比开立方（有理数精确开立方）
num, den = vol_ratio.numerator, vol_ratio.denominator
cr = lambda n: round(n ** (1/3))
k = F(cr(num), cr(den)); assert k**3 == vol_ratio
new_exposed = exposed * k
drop = new_exposed - exposed           # 水位下降量
depth = drop / F(20, 100)
options = {"A": F(35, 10), "B": F(375, 100), "C": F(425, 100), "D": F(45, 10)}
hits = [k_ for k_, v in options.items() if v == depth]
assert len(hits) == 1, (depth, hits)
print(hits[0])
