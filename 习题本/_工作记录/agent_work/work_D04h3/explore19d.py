# above-mode newsvendor search, relaxed
from itertools import product
from fractions import Fraction as Fr

def profit(q, d, p, c, s):
    sold = min(q, d)
    return p * sold + s * (q - sold) - c * q

cfgs = [(6, 3, 2), (9, 3, 1), (13, 4, 1), (8, 3.5, 2), (12, 5, 3), (7, 3, 1), (5, 2, 1), (8, 3, 1), (6, 2.5, 1.5), (4, 1.5, 0.5)]
levels_sets = [[80, 100, 120, 140], [40, 50, 60, 70], [60, 80, 100, 120], [150, 200, 250, 300]]
for p, c, s in cfgs:
    crit = (c - s) / (p - s)
    for N in (20, 30):
        for levels in levels_sets:
            found = []
            for f in product(range(1, 20), repeat=3):
                f4 = N - sum(f)
                if f4 < 1: continue
                freq = list(f) + [f4]
                mode_cnt = max(freq)
                modes = [q for q, fr in zip(levels, freq) if fr == mode_cnt]
                if len(modes) != 1: continue
                mode = modes[0]
                mean = Fr(sum(q * fr for q, fr in zip(levels, freq)), N)
                step = levels[1] - levels[0]
                # mean clearly nearer to level 2 (not within 20% of midpoint)
                if not (levels[1] - step * Fr(3, 10) <= mean <= levels[1] + step * Fr(3, 10)): continue
                if mode != levels[1]: continue
                tot = [sum(fr * profit(q, d, p, c, s) for d, fr in zip(levels, freq)) for q in levels]
                best = max(tot)
                arg = [q for q, t in zip(levels, tot) if t == best]
                if len(arg) != 1 or arg[0] != levels[2]: continue
                st = sorted(tot)
                gaps = [b - a for a, b in zip(st, st[1:])]
                if min(gaps) < 0.025 * max(abs(t) for t in tot): continue
                if any(t != int(t) for t in tot): continue
                srt = sorted(sum([[q] * fr for q, fr in zip(levels, freq)], []))
                med = (srt[N // 2 - 1] + srt[N // 2]) / 2
                found.append((freq, float(mean), med, [int(t) for t in tot]))
            if found:
                print((p, c, s), 'crit', round(crit, 3), 'N', N, levels, len(found))
                for x in found[:8]:
                    print('    ', x)
