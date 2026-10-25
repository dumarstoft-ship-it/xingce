# targeted newsvendor search with curated prices
from itertools import product
from fractions import Fraction as Fr
import sys

def profit(q, d, p, c, s):
    sold = min(q, d)
    return p * sold + s * (q - sold) - c * q

curated = [
    # (label, p, c, s)
    ('meal15_10_4', 15, 10, 4),
    ('meal16_10_4', 16, 10, 4),
    ('meal15_9_3', 15, 9, 3),
    ('rice8_5_3', 8, 5, 3),
    ('rice9_5_2', 9, 5, 2),
    ('rice8_5_2', 8, 5, 2),
    ('milk10_7_1', 10, 7, 1),
    ('milk12_8_2', 12, 8, 2),
    ('fish30_20_8', 30, 20, 8),
    ('fish25_16_6', 25, 16, 6),
    ('bun3_1_05', 3, 1, 0.5),
    ('flower20_8_2', 20, 8, 2),
    ('cake12_6_3', 12, 6, 3),
    ('cake12_7_2', 12, 7, 2),
]
want = sys.argv[1] if len(sys.argv) > 1 else None
levels_sets = [[80, 100, 120, 140], [60, 80, 100, 120], [100, 120, 140, 160], [40, 50, 60, 70], [50, 60, 70, 80], [30, 40, 50, 60]]
for label, p, c, s in curated:
    if want and label != want: continue
    crit = Fr(c - s) / Fr(p - s) if isinstance(s, int) else Fr(str(c - s)) / Fr(str(p - s))
    out = []
    for N in (20, 30):
        for levels in levels_sets:
            for f in product(range(1, min(N, 16)), repeat=3):
                f4 = N - sum(f)
                if f4 < 1: continue
                freq = list(f) + [f4]
                mode_cnt = max(freq)
                modes = [q for q, fr in zip(levels, freq) if fr == mode_cnt]
                if len(modes) != 1: continue
                mode = modes[0]
                mean = Fr(sum(q * fr for q, fr in zip(levels, freq)), N)
                near = min(levels, key=lambda q: abs(q - mean))
                if abs(mean - near) * 2 == (levels[1] - levels[0]): continue  # ambiguous nearest
                tot = [sum(fr * profit(q, d, p, c, s) for d, fr in zip(levels, freq)) for q in levels]
                best = max(tot)
                arg = [q for q, t in zip(levels, tot) if t == best]
                if len(arg) != 1: continue
                qs = arg[0]
                if qs in (mode, near, levels[-1], levels[0]): continue
                st = sorted(tot)
                if min(b - a for a, b in zip(st, st[1:])) < 150: continue
                if any(t != int(t) for t in tot): continue
                # marginal nets
                marg = [tot[i + 1] - tot[i] for i in range(3)]
                out.append((N, levels, freq, qs, mode, float(mean), near, [int(t) for t in tot], [int(m) for m in marg]))
    print(label, p, c, s, 'crit', float(crit), 'count', len(out))
    # show a few with mode == near (single 'intuition' distractor) and qs below mode
    shown = 0
    for o in out:
        N, levels, freq, qs, mode, mean, near, tot, marg = o
        if mode == near and shown < 12:
            print('   ', o)
            shown += 1
