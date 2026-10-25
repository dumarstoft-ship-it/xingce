# T256 AD、BC⊥底边，△ACD 等腰直角，AG=DE=CF=t，DF=80，BC=160；阴影=△EGC+△BCF
from fractions import Fraction as F
def tri(p, q, r):
    return abs((q[0]-p[0])*(r[1]-p[1]) - (r[0]-p[0])*(q[1]-p[1])) / 2
DF, BC = F(80), F(160)
areas = set()
for t in [F(1), F(5), F(10), F(20), F(30), F(39)]:   # 动点位置任取（需 t < a）
    a = DF - t                         # AD = DC = a
    D = (F(0), F(0)); C = (a, F(0)); E = (-t, F(0)); Fp = (a + t, F(0))
    A = (F(0), a); G = (F(0), a - t); B = (a, BC)
    areas.add(tri(E, G, C) + tri(B, C, Fp))
assert len(areas) == 1, areas            # 面积与动点无关
area = areas.pop()
options = {"A": F(3200), "B": F(3600), "C": F(4000), "D": F(4800)}
hits = [k for k, v in options.items() if v == area]
assert len(hits) == 1, (area, hits)
print(hits[0])
