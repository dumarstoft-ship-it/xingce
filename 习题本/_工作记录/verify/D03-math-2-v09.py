# D03-math-2-v09: up-escalator. 小王 walks up 24 steps; 小李 (twice 小王's step rate) walks up 40 steps.
# Visible steps when the escalator is stopped?
# Method: for several values of 小王's rate v (only the ratio is given), and for every option N, the escalator
# rate implied by 小王's ride is e = (N-24)/(24/v); keep N only if 小李's ride with that e also gives N.
# Also an independent scan: N = person steps + escalator steps for a grid of e values.
from fractions import Fraction as F

OPTIONS = {'A': 64, 'B': 80, 'C': 96, 'D': 120}
ok = set()
for v in (F(1, 2), F(1), F(3, 2), F(2)):
    t_wang, t_li = 24 / v, F(40) / (2 * v)
    for k, N in OPTIONS.items():
        e = (N - 24) / t_wang
        if e > 0 and 40 + e * t_li == N:
            ok.add(k)
    # scan escalator rates: find e making both rides cover the same number of steps
    sols = [e for e in (F(i, 100) * v for i in range(1, 2001)) if 24 + e * t_wang == 40 + e * t_li]
    assert len(sols) == 1 and 24 + sols[0] * t_wang == 120
assert len(ok) == 1, ok
hit = ok.pop()
# distractors: sum of walked steps; escalator-only steps during 小李's / 小王's ride (e = 4v)
assert 24 + 40 == OPTIONS['A'] and 4 * 20 == OPTIONS['B'] and 4 * 24 == OPTIONS['C']
print(hit)
