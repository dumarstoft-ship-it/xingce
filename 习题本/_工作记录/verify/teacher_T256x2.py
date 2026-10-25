# T256x2 两个相邻正方形，大正方形 ABCD 周长 40，连接 A、C、F，求阴影 △AFC 面积
from fractions import Fraction as F
a = F(40) / 4
tri = lambda p, q, r: abs((q[0]-p[0])*(r[1]-p[1]) - (r[0]-p[0])*(q[1]-p[1])) / 2
vals = set()
for s in (F(2), F(5), F(7), F(19, 2)):            # 小正方形边长任取
    D = (F(0), F(0)); A = (F(0), a); C = (a, F(0)); Fp = (-s, s)
    vals.add(tri(A, Fp, C))
assert len(vals) == 1, vals
area = vals.pop()
options = {"A": 40, "B": 50, "C": 55, "D": 60}
hits = [k for k, v in options.items() if v == area]
assert len(hits) == 1, (area, hits)
print(hits[0])
