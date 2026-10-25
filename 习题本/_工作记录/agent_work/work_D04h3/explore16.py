# explore numbers for need #16: continuous loss + clearance pricing
from fractions import Fraction as Fr

def nice(x, dec=2):
    return (x * 10**dec).denominator == 1

res = []
for rpct in (5, 10, 20):
    r = Fr(rpct, 100)
    for d in (2, 3):
        keep = (1 - r) ** d
        add = 1 - d * r
        for spct in (60, 70, 75, 80, 90):
            s = Fr(spct, 100)
            for kpct in (40, 50, 60, 70, 80):
                k = Fr(kpct, 100)
                avg = s + (1 - s) * k
                for Rpct in (10, 20, 25, 30, 40, 50):
                    R = Fr(Rpct, 100)
                    for P10 in range(50, 400):          # price in 0.1 yuan
                        P = Fr(P10, 10)
                        c = P * keep * avg / (1 + R)
                        if not nice(c, 2): continue
                        if c < 3: continue
                        E_add = c * (1 + R) / (add * avg)       # loss added, not multiplied
                        E_nodisc = c * (1 + R) / keep           # clearance at full price
                        E_norev = c * (1 + R) / (keep * s)      # clearance revenue forgotten
                        E_sold = c * (1 + R) / (avg)            # ignore loss entirely
                        ds = [E_add, E_nodisc, E_norev]
                        if not all(nice(x, 2) for x in ds): continue
                        vals = sorted(set([P] + ds))
                        if len(vals) < 4: continue
                        res.append((rpct, d, spct, kpct, Rpct, float(P), float(c), [float(x) for x in ds]))
print(len(res))
for x in res[:200]:
    print(x)
