from fractions import Fraction as Fr
N, U_ONLY, UT_ONLY, NONE = 80, 14, 10, 18
rest = N - U_ONLY - UT_ONLY - NONE
vals=set()
for t in range(rest + 1):
    for r in range(rest - t + 1):
        for ur in range(rest - t - r + 1):
            for tr in range(rest - t - r - ur + 1):
                utr = rest - t - r - ur - tr
                tiller = r + ur + tr + utr
                tractor = t + UT_ONLY + tr + utr
                if tiller == 0 or Fr(tiller,2) != ur + utr: continue
                if Fr(tractor,3) != tr+utr: continue   # without containment, "tractor owners with tiller" = tr+utr
                vals.add(U_ONLY + UT_ONLY + ur + utr)
print('without containment, drone values:', sorted(vals))
