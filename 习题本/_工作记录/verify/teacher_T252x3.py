# T252x3 梯形 ABCD，DC=3AB，EF 为中位线，G=AF∩BE，H=EC∩DF，求 S四边形EGFH : S梯形
from fractions import Fraction as F
def inter(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / den
    return (x1 + t*(x2-x1), y1 + t*(y2-y1))
tri = lambda p, q, r: abs((q[0]-p[0])*(r[1]-p[1]) - (r[0]-p[0])*(q[1]-p[1])) / 2
res = set()
for a, h in [(F(1), F(2)), (F(-1, 2), F(5)), (F(2), F(3))]:
    D = (F(0), F(0)); C = (F(3), F(0)); A = (a, h); B = (a + 1, h)
    E = ((A[0]+D[0])/2, (A[1]+D[1])/2); Fm = ((B[0]+C[0])/2, (B[1]+C[1])/2)
    G = inter(A, Fm, B, E); H = inter(E, C, D, Fm)
    egf, ehf = tri(E, G, Fm), tri(E, H, Fm)
    assert egf / ehf == F(5, 3)                  # 题给 5:3 与图形一致
    res.add((egf + ehf) / ((1 + 3) * h / 2))
assert len(res) == 1, res
r = res.pop()
options = {"A": F(1, 6), "B": F(1, 10), "C": F(4, 13), "D": F(4, 15)}
hits = [k for k, v in options.items() if v == r]
assert len(hits) == 1, (r, hits)
print(hits[0])
