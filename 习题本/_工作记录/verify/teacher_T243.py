# T243 水箱 60×40×30，水深 15；放入棱长 20 的正方体铁块，再提起 6cm，水位下降多少
from fractions import Fraction as F
Lx, Ly, Hb, h0 = F(60), F(40), F(30), F(15)
a = F(20)
S, s = Lx * Ly, a * a
W = S * h0                                  # 水的体积

def level(bottom):
    """铁块底部离箱底 bottom 时的水位（铁块顶在 bottom+a）"""
    # 分段：水位在铁块底以下 / 铁块之间 / 铁块顶以上
    if W <= S * bottom:
        return W / S
    h = bottom + (W - S * bottom) / (S - s)
    if h <= bottom + a:
        return h
    return (W + s * a) / S

h1 = level(F(0))
assert h1 < a                                # 未没过铁块
h2 = level(F(6))
drop = h1 - h2
options = {"A": F(3, 2), "B": F(2), "C": F(1), "D": F(6, 5)}
hits = [k for k, v in options.items() if v == drop]
assert len(hits) == 1, (h1, h2, drop, hits)
print(hits[0])
