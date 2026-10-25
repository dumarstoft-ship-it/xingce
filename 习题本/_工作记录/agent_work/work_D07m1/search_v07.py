from fractions import Fraction as F
res = []
for L in range(10, 101, 5):
    for W in range(10, L+1, 5):
        base = L*W
        for a in range(5, 51, 5):
            if a > min(L, W) - 1: continue
            for d in range(2, 50):
                if d >= a: continue
                hfull = F(d*base + a**3, base)
                if hfull >= a:
                    continue
                h = F(d*base, base - a*a)
                if h > a: continue
                rise = h - d
                if rise.denominator != 1: continue
                full_rise = F(a**3, base)
                only_d = F(a*a*d, base)
                hybrid = F(a**3, base - a*a)
                exposed = a - h
                vals = dict(rise=rise, full_rise=full_rise, depth=h, only_d=only_d, hybrid=hybrid, exposed=exposed)
                res.append((L, W, d, a, {k: str(v) for k, v in vals.items()}))
for r in res:
    print(r)
print(len(res))
