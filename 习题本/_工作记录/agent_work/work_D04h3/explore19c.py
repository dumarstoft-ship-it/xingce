# specific newsvendor search: above-mode optimum, N = 30, curated (p, c, s)
from itertools import product
from fractions import Fraction as Fr
import sys

def profit(q, d, p, c, s):
    sold = min(q, d)
    return p * sold + s * (q - sold) - c * q

cfgs = [(15, 9, 6), (16, 10, 7), (14, 8, 5), (12, 8, 6), (2, 1, 0.5), (3, 1.5, 0.75), (9, 5, 3), (8, 5, 3.5), (6, 4, 3)]
levels_sets = [[40, 50, 60, 70], [80, 100, 120, 140], [200, 250, 300, 350], [30, 40, 50, 60]]
for p, c, s in cfgs:
    crit = (c - s) / (p - s)
    for N in (30,):
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
                near = min(levels, key=lambda q: abs(q - mean))
                if abs(mean - near) * 2 == (levels[1] - levels[0]): continue
                tot = [sum(fr * profit(q, d, p, c, s) for d, fr in zip(levels, freq)) for q in levels]
                best = max(tot)
                arg = [q for q, t in zip(levels, tot) if t == best]
                if len(arg) != 1: continue
                qs = arg[0]
                if qs != levels[2]: continue          # want optimum at 3rd level
                if mode != levels[1] or near != levels[1]: continue  # mode & mean point at 2nd level
                st = sorted(tot)
                gaps = [b - a for a, b in zip(st, st[1:])]
                if min(gaps) < 0.04 * max(abs(t) for t in tot): continue
                if any(t != int(t) for t in tot): continue
                # median
                srt = sorted(sum([[q] * fr for q, fr in zip(levels, freq)], []))
                med = (srt[N // 2 - 1] + srt[N // 2]) / 2
                found.append((freq, float(mean), med, [int(t) for t in tot]))
            print((p, c, s), 'crit', round(crit, 3), levels, len(found))
            for x in found[:15]:
                print('    ', x)
