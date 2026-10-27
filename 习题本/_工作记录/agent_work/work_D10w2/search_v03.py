# search data for weighted ordering (Smith's rule) problem
import itertools
from fractions import Fraction as F

def total(order, t, w):
    c = 0; s = 0
    for i in order:
        c += t[i]
        s += w[i] * c
    return s

res = []
for t in itertools.combinations(range(1, 8), 4):
    for wperm in itertools.permutations(range(1, 7), 4):
        w = wperm
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
        S = vals[spt]; M = vals[mw]
        lou = best - sum(t[i]*w[i] for i in range(n))
        # GD-44 habit: SPT order, waiting only
        spt_wait = S - sum(t[i]*w[i] for i in range(n))
        cand = [best, S, M, lou]
        if len(set(cand)) < 4: continue
        # first job of optimum is neither shortest nor heaviest
        first_interesting = opt[0] != spt[0] and opt[0] != mw[0]
        res.append((t, w, opt, best, S, M, lou, spt_wait, first_interesting, sum(t)))

print(len(res))
# prefer: totals moderate, distractors close, first job interesting
def score(r):
    t, w, opt, best, S, M, lou, sw, fi, st = r
    return (not fi, max(S, M) - best, best)
res.sort(key=score)
for r in res[:60]:
    t, w, opt, best, S, M, lou, sw, fi, st = r
    print('t', t, 'w', w, 'opt', [ 'ABCD'[i] for i in opt], 'best', best, 'SPT', S, 'maxW', M, 'lou', lou, 'sptwait', sw, 'first_int', fi, 'ratios', [str(F(t[i], w[i])) for i in range(4)])
