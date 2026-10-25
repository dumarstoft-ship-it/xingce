# T249x3（2018江苏B）长方形 ABCD，S△ABE=S△ADF=S四边形AECF，求 S△AEF:S△CEF
from fractions import Fraction as F
w, h = F(6), F(9)                       # 任取长宽
S = w * h
# A(0,h) B(w,h) C(w,0) D(0,0)；E 在 BC 上，F 在 DC 上
BE = 2 * (S / 3) / w                    # S△ABE = AB·BE/2 = S/3
DF = 2 * (S / 3) / h                    # S△ADF = AD·DF/2 = S/3
E = (w, h - BE); Fp = (DF, F(0)); A = (F(0), h); C = (w, F(0))
def tri(p, q, r):
    return abs((q[0]-p[0])*(r[1]-p[1]) - (r[0]-p[0])*(q[1]-p[1])) / 2
assert tri(A, E, C) + tri(A, C, Fp) == S / 3          # 四边形 AECF
ratio = tri(A, E, Fp) / tri(C, E, Fp)
options = {"A": F(5, 1), "B": F(5, 2), "C": F(5, 3), "D": F(6, 1)}
hits = [k for k, v in options.items() if v == ratio]
assert len(hits) == 1, (ratio, hits)
print(hits[0])
