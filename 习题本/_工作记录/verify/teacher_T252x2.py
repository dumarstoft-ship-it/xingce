# T252x2 梯形 ABCD（AB∥CD），CD=2AB=3DF，G=AF∩BD，求 S△ADG / S梯形
from fractions import Fraction as F
def inter(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / den
    return (x1 + t*(x2-x1), y1 + t*(y2-y1))
tri = lambda p, q, r: abs((q[0]-p[0])*(r[1]-p[1]) - (r[0]-p[0])*(q[1]-p[1])) / 2
res = set()
for a, h in [(F(1), F(4)), (F(-2), F(7)), (F(5, 2), F(3))]:      # 不同形状的梯形
    D = (F(0), F(0)); C = (F(6), F(0)); A = (a, h); B = (a + 3, h); Fp = (F(2), F(0))
    G = inter(A, Fp, B, D)
    trap = (3 + 6) * h / 2
    res.add(tri(A, D, G) / trap)
assert len(res) == 1, res
r = res.pop()
options = {"A": F(1, 3), "B": F(4, 15), "C": F(1, 5), "D": F(2, 15)}
hits = [k for k, v in options.items() if v == r]
assert len(hits) == 1, (r, hits)
print(hits[0])
