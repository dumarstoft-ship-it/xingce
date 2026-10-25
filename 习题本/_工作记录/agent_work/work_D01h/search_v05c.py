from fractions import Fraction as F
from math import gcd
from itertools import product
FR = [F(1,2),F(1,3),F(2,3),F(1,4),F(3,4),F(1,5),F(2,5),F(3,5)]
def rat(x, y):
    r = F(x) / F(y); return (r.numerator, r.denominator)
pairs = [(a,b) for a in range(1,6) for b in range(1,6) if gcd(a,b)==1]
merged = [(a,b) for a in range(1,10) for b in range(1,10) if gcd(a,b)==1 and a+b<=12]
rows = []
for (a1,b1),(a2,b2),(a,b) in product(pairs, pairs, merged):
    if (a1,b1)==(4,1) or ((a1,b1),(a2,b2))==((3,1),(1,1)): continue
    if (a1,b1)==(a2,b2): continue
    s1, s2, s = F(a1,a1+b1), F(a2,a2+b2), F(a,a+b)
    if not (min(s1,s2) < s < max(s1,s2)): continue
    R = (s - s2) / (s1 - s)
    if R == 1 or R.numerator > 3 or R.denominator > 3: continue
    for f1,g1,f2,g2 in product(FR, repeat=4):
        if len({f1,g1,f2,g2}) < 4: continue
        def att(Rr): return rat(Rr*s1*f1 + s2*f2, Rr*(1-s1)*g1 + (1-s2)*g2)
        cor, eq, sw = att(R), att(F(1)), att(1/R)
        rev = (cor[1], cor[0])
        opts = [cor, eq, sw, rev]
        if len(set(opts)) < 4: continue
        if max(cor) > 9 or max(max(x) for x in opts) > 15: continue
        srt = sorted(opts, key=lambda t: F(t[0], t[1]))
        pos = 'ABCD'[srt.index(cor)]
        if pos not in 'CD': continue
        m = 1
        while True:
            A, B = R.numerator*m, R.denominator*m
            vals = [A*s1, A*(1-s1), B*s2, B*(1-s2), A*s1*f1, A*(1-s1)*g1, B*s2*f2, B*(1-s2)*g2]
            if all(v.denominator == 1 for v in vals): break
            m += 1
        score = sum(max(x) for x in opts)
        rows.append((score, pos, f'甲{a1}:{b1} 乙{a2}:{b2} 合{a}:{b} 甲:乙={R} f甲={f1},{g1} f乙={f2},{g2} | 正确{cor} 等大{eq} 规模反{sw} 颠倒{rev} -> {pos}  sorted {srt} 人数甲{A}乙{B}'))
rows.sort()
print(len(rows))
for r in rows[:60]: print(r[2])
