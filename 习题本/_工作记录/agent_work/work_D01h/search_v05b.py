from fractions import Fraction as F
from itertools import product
FR = [F(1,2),F(1,3),F(2,3),F(1,4),F(3,4),F(1,5),F(2,5),F(3,5)]
def rat(x, y):
    r = F(x) / F(y); return (r.numerator, r.denominator)
L1 = [((4,1),(1,1),(3,2)), ((4,1),(1,1),(7,3)), ((3,1),(1,2),(1,1)), ((2,1),(1,3),(1,1)), ((2,1),(1,1),(5,3)), ((3,1),(1,1),(11,5)), ((4,1),(2,3),(7,3)), ((5,1),(1,2),(1,1))]
for (a1,b1),(a2,b2),(a,b) in L1:
    s1, s2, s = F(a1,a1+b1), F(a2,a2+b2), F(a,a+b)
    R = (s - s2) / (s1 - s)
    print('=== 甲', (a1,b1), '乙', (a2,b2), '合', (a,b), '规模甲:乙', R, '份加', F(a1+b1,a2+b2))
    rows = []
    for f1,g1,f2,g2 in product(FR, repeat=4):
        if len({f1,g1,f2,g2}) < 4: continue
        def att(Rr): return rat(Rr*s1*f1 + s2*f2, Rr*(1-s1)*g1 + (1-s2)*g2)
        cor, eq, sw, pa = att(R), att(F(1)), att(1/R), att(F(a1+b1,a2+b2))
        rev = (cor[1], cor[0])
        d = [eq, sw, rev]
        if len({cor, *d}) < 4: continue
        if max(cor) > 9 or max(max(x) for x in d) > 20: continue
        m = 1
        while True:
            A, B = R.numerator*m, R.denominator*m
            vals = [A*s1, A*(1-s1), B*s2, B*(1-s2), A*s1*f1, A*(1-s1)*g1, B*s2*f2, B*(1-s2)*g2]
            if all(v.denominator == 1 for v in vals): break
            m += 1
        rows.append((max(cor)+max(max(x) for x in d), f'f甲={f1},{g1} f乙={f2},{g2} 正确{cor} 等大{eq} 规模反{sw} 份加{pa} 人数甲{A}乙{B}'))
    rows.sort()
    for r in rows[:12]: print('  ', r[1])
