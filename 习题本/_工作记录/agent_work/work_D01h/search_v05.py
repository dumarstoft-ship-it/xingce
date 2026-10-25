# Targeted search for need 5 (two units of unequal size, two-layer ratio merge).
from fractions import Fraction as F
from math import gcd, lcm
from itertools import product

FR = [F(1,2),F(1,3),F(2,3),F(1,4),F(3,4),F(1,5),F(2,5),F(3,5)]
def rat(x, y):
    r = F(x) / F(y); return (r.numerator, r.denominator)

pairs = [(a,b) for a in range(1,6) for b in range(1,6) if gcd(a,b)==1]
layer1 = []
for (a1,b1),(a2,b2),(a,b) in product(pairs, pairs, [(a,b) for a in range(1,14) for b in range(1,14) if gcd(a,b)==1 and a+b<=20]):
    s1, s2, s = F(a1,a1+b1), F(a2,a2+b2), F(a,a+b)
    if not (s2 < s < s1): continue
    R = (s - s2) / (s1 - s)
    if R == 1 or R == F(a1+b1, a2+b2): continue
    if R.numerator > 4 or R.denominator > 4: continue
    if (a1,b1)==(3,1) and (a2,b2)==(1,1) and (a,b)==(13,7): continue  # example of the need
    layer1.append(((a1,b1),(a2,b2),(a,b),R))
print('layer1 candidates', len(layer1))
for L in layer1: print('  ', L[0], L[1], L[2], 'size', L[3])

out = []
for (a1,b1),(a2,b2),(a,b),R in layer1:
    s1, s2 = F(a1,a1+b1), F(a2,a2+b2)
    for f1,g1,f2,g2 in product(FR, repeat=4):
        if len({f1,g1,f2,g2}) < 4: continue
        def att(Rr):
            return rat(Rr*s1*f1 + s2*f2, Rr*(1-s1)*g1 + (1-s2)*g2)
        cor, eq, pa = att(R), att(F(1)), att(F(a1+b1, a2+b2))
        rev = (cor[1], cor[0])
        if len({cor, eq, pa, rev}) < 4: continue
        if max(cor) > 9 or max(eq) > 19 or max(pa) > 19: continue
        # minimal integer headcounts: 甲 = R.num*m, 乙 = R.den*m, all subgroup counts integers
        m = 1
        while True:
            A, B = R.numerator*m, R.denominator*m
            vals = [A*s1, A*(1-s1), B*s2, B*(1-s2), A*s1*f1, A*(1-s1)*g1, B*s2*f2, B*(1-s2)*g2]
            if all(v.denominator == 1 for v in vals): break
            m += 1
        out.append((A+B, (a1,b1),(a2,b2),(a,b),R,(f1,g1,f2,g2),cor,eq,pa,A,B))
out.sort(key=lambda t: (max(t[6]), t[0]))
print('total', len(out))
for t in out[:80]:
    tot,(a1,b1),(a2,b2),(a,b),R,fr,cor,eq,pa,A,B = t
    print(f'甲{a1}:{b1} 乙{a2}:{b2} 合{a}:{b} 规模甲:乙={R} f甲={fr[0]},{fr[1]} f乙={fr[2]},{fr[3]} 正确{cor} 等大{eq} 份加{pa} 最小人数甲{A}乙{B}')
