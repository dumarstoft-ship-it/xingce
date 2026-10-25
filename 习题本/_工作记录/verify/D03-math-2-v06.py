# D03-math-2-v06: three patrol staff on a loop, same start, same direction, 甲 fastest, 丙 slowest.
# 甲 catches 乙 every 24 min, 乙 catches 丙 every 40 min. Every how many minutes does 甲 catch 丙?
# Method: the data only fix speed differences, so try several absolute speeds for 丙 and several loop lengths;
# simulate exactly (step 1/8 min) and read off the interval between successive catches of 甲 on 丙.
from fractions import Fraction as F

OPTIONS = {'A': 15, 'B': 16, 'C': 60, 'D': 64}
results = set()
for L in (F(1), F(120), F(2400)):
    for c in (L / 50, L / 7, L / 3):                  # speed of 丙 (per minute), arbitrary
        v3 = c
        v2 = v3 + L / 40                               # 乙 gains one lap on 丙 every 40 min
        v1 = v2 + L / 24                               # 甲 gains one lap on 乙 every 24 min
        # sanity: simulate the two given intervals as well as the asked one
        def catch_times(va, vb, n, step=F(1, 8)):
            out, t = [], F(0)
            while len(out) < n:
                t += step
                if ((va - vb) * t) % L == 0:
                    out.append(t)
            return out
        assert catch_times(v1, v2, 2) == [24, 48] and catch_times(v2, v3, 2) == [40, 80]
        ct = catch_times(v1, v3, 4)
        gaps = {b - a for a, b in zip([F(0)] + ct, ct)}
        assert len(gaps) == 1
        results |= gaps
assert len(results) == 1
gap = results.pop()
hits = [k for k, v in OPTIONS.items() if v == gap]
assert len(hits) == 1, (gap, hits)
assert 40 - 24 == OPTIONS['B'] and 24 + 40 == OPTIONS['D'] and 1 / (F(1, 24) - F(1, 40)) == OPTIONS['C']
print('甲 catches 丙 every', gap, 'min')
print(hits[0])
