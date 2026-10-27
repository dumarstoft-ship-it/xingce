import itertools
from fractions import Fraction as F

def total(order, t, w):
    c = 0; s = 0
    for i in order:
        c += t[i]; s += w[i] * c
    return s

def hamming(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)

res = []
for t in itertools.combinations(range(2, 10), 4):
    for w in itertools.permutations(range(1, 7), 4):
        n = 4
        allo = list(itertools.permutations(range(n)))
        vals = {o: total(o, t, w) for o in allo}
        best = min(vals.values())
        opts = [o for o in allo if vals[o] == best]
        if len(opts) != 1: continue
        opt = opts[0]
        spt = tuple(sorted(range(n), key=lambda i: t[i]))
        mw = tuple(sorted(range(n), key=lambda i: -w[i]))
        if spt == opt or mw == opt or spt == mw: continue
        if opt[0] in (spt[0], mw[0]): continue
        if hamming(opt, spt) < 3 or hamming(opt, mw) < 3: continue
        S = vals[spt]; M = vals[mw]
        swt = sum(t[i]*w[i] for i in range(n))
        lou = best - swt
        cand = [best, S, M, lou]
        if len(set(cand)) < 4: continue
        if min(S, M) - best < 3: continue
        if abs(S - M) < 2: continue
        if max(S, M) > 220: continue
        # second-worst order total (to see spread)
        res.append((t, w, opt, best, S, M, lou, swt))

print(len(res))
res.sort(key=lambda r: (r[3]))
for r in res[:80]:
    t, w, opt, best, S, M, lou, swt = r
    print('t', t, 'w', w, 'opt', ''.join('ABCD'[i] for i in opt), 'best', best, 'SPT', S, 'maxW', M, 'lou', lou, 'ratios', [str(F(t[i], w[i])) for i in range(4)])
