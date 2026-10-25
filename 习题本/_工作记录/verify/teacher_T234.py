# T234 墙角四分之一圆锥谷堆：弧长 6→8，体积不变，高 2→?
from fractions import Fraction as F
arc1, arc2, h1 = F(6), F(8), F(2)
# 弧长 = (1/4)·2πr ∝ r；体积 = (1/4)(1/3)πr²h ∝ r²h
r_ratio = arc2 / arc1
h2 = h1 / r_ratio**2
options = {"A": F(9, 8), "B": F(8, 9), "C": F(9, 16), "D": F(4, 9)}
hits = [k for k, v in options.items() if v == h2]
assert len(hits) == 1, (h2, hits)
print(hits[0])
