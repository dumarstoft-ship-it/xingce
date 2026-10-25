# T256x3（2025天津）矩形 ABCD，ADEF 为矩形，BD 交 EF 于 O，AF=600，FE=400，求 △COD 面积（万平方米）
from fractions import Fraction as F
AF, FE = F(600), F(400)
tri = lambda p, q, r: abs((q[0]-p[0])*(r[1]-p[1]) - (r[0]-p[0])*(q[1]-p[1])) / 2
vals = set()
for L in (F(700), F(800), F(1200), F(3000)):      # AB 总长未知，任取
    D = (F(0), F(0)); A = (F(0), FE); B = (L, FE); C = (L, F(0)); E = (AF, F(0))
    O = (AF, FE * AF / L)                           # BD 上 x=AF 处
    vals.add(tri(C, O, D))
assert len(vals) == 1, vals
area_wan = vals.pop() / 10000
options = {"A": 12, "B": 15, "C": 16, "D": 18}
hits = [k for k, v in options.items() if v == area_wan]
assert len(hits) == 1, (area_wan, hits)
print(hits[0])
