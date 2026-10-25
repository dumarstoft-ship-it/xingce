# explore numbers for need #19: newsvendor with discrete demand, choose order level
from itertools import product
from fractions import Fraction as Fr
import random, sys

def profit(q, d, p, c, s):
    sold = min(q, d)
    return p * sold + s * (q - sold) - c * q

N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
levels_sets = [[80, 100, 120, 140], [60, 80, 100, 120], [150, 200, 250, 300], [40, 50, 60, 70], [200, 250, 300, 350]]
pcs = [(p, c, s) for p in range(5, 16) for c in range(2, 12) for s in [0, 0.5, 1, 1.5, 2, 2.5, 3] if s < c < p]
pcs = [t for t in pcs if t not in [(10, 4, 2), (10, 5, 2)]]
res = []
for levels in levels_sets:
    for f in product(range(1, N), repeat=3):
        f4 = N - sum(f)
        if f4 < 1: continue
        freq = list(f) + [f4]
        mode_cnt = max(freq)
        modes = [q for q, fr in zip(levels, freq) if fr == mode_cnt]
        if len(modes) != 1: continue
        mode = modes[0]
        mean = Fr(sum(q * fr for q, fr in zip(levels, freq)), N)
        near = min(levels, key=lambda q: abs(q - mean))
        # tail probabilities
        for p, c, s in pcs:
            tot = [sum(fr * profit(q, d, p, c, s) for d, fr in zip(levels, freq)) for q in levels]
            best = max(tot)
            arg = [q for q, t in zip(levels, tot) if t == best]
            if len(arg) != 1: continue
            qs = arg[0]
            if qs in (mode, near, levels[-1], levels[0]): continue
            st = sorted(tot)
            if min(b - a for a, b in zip(st, st[1:])) < 100: continue
            if any(t != int(t) for t in tot): continue
            res.append((p, c, s, levels, freq, qs, mode, float(mean), near, [int(t) for t in tot]))
print(len(res))
random.seed(3)
for r in random.sample(res, min(80, len(res))):
    print(r)
