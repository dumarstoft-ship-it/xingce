import math
from fractions import Fraction as F
def isq(v):
    r = math.isqrt(int(v)) if float(v).is_integer() else None
    return r is not None and r*r == v
for t in [F(1),F(3,2),F(2),F(5,2),F(3),F(4),F(5)]:
    for X in range(4, 41):
        if X <= 2*t: continue
        S = 4*t*X
        # (a) x^2 = S
        a = math.sqrt(S)
        # (d) x^2 + 4 t x = S
        d = -2*float(t) + math.sqrt(4*float(t)**2 + float(S))
        c = S/4
        e = (-4*float(t) + math.sqrt(16*float(t)**2 + 8*float(S)))/4  # 2x^2+4tx=S
        tags = []
        if abs(a-round(a))<1e-9: tags.append(f"a={round(a)}")
        if abs(d-round(d))<1e-9: tags.append(f"d={round(d)}")
        if abs(e-round(e))<1e-9: tags.append(f"e={round(e)}")
        if tags:
            print(f"t={t} X={X} S={S} c={c} a={a:.3f} d={d:.3f} e={e:.3f}", tags)
