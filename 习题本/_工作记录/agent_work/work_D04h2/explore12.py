# need 12 search: price p, var v, fixed F, target cost-margin r (profit / total cost)
from fractions import Fraction as Fr
import math
res = []
for r in (Fr(1,5), Fr(1,4)):
    for p in range(30, 121):
        for v in range(10, p):
            if v == 30 and p == 50: continue
            denom = p - v*(1+r)             # per-unit net increase
            if denom <= 0: continue
            for Fw in [x/2 for x in range(8, 61)]:  # F in 万元, 4..30 step 0.5
                F = Fr(int(Fw*2*10000), 2)
                Q = F*(1+r)/denom                  # correct
                Qvar = F/(p - v - r*v)             # denominator only variable cost (forgot r*F)
                Qfix = F*(1+r)/(p - v)             # denominator only fixed cost (forgot r*v*Q)
                sales_den = p - v - r*p
                Qsale = F/sales_den if sales_den > 0 else None   # profit/revenue
                Qbe = F/(p - v)
                vals = [Q, Qvar, Qfix, Qbe] + ([Qsale] if Qsale else [])
                if all(x.denominator == 1 for x in vals) and Q % 100 == 0 and Q <= 20000 and Q >= 2000:
                    res.append((float(r), p, v, float(Fw), int(Q), int(Qvar), int(Qfix), int(Qsale) if Qsale else None, int(Qbe)))
print(len(res))
for x in res[:400]:
    print(x)
