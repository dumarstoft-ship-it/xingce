# -*- coding: utf-8 -*-
"""Fresh brute-force solutions for the 4 M01 real questions without official answers,
plus targeted re-checks of real questions flagged in the issue list."""
from fractions import Fraction as F

def pick(val, opts):
    hits = [k for k, v in opts.items() if (v(val) if callable(v) else F(v) == F(val))]
    assert len(hits) == 1, (val, hits)
    return hits[0]

out = {}
# 2026GD-36: wind 40%, PV 35% of total, rest biomass; PV - biomass = 120 MW -> total
sols = [T for T in range(1, 100000) if (F(35, 100) * T).denominator == 1 and (F(25, 100) * T).denominator == 1
        and F(35, 100) * T - (1 - F(40, 100) - F(35, 100)) * T == 120]
assert len(sols) == 1; out['2026GD-36'] = (pick(sols[0], {'A': 600, 'B': 800, 'C': 1000, 'D': 1200}), sols[0])

# 2026GD-37: Sat clients = 1.5 x Sun clients, Sat amount = 80% of Sun amount, 40 clients, 720 (wan) -> Sun average
sols = set()
for sun in range(1, 40):
    sat = 40 - sun
    if F(sat) != F(3, 2) * sun: continue
    for sun_amt10 in range(1, 7201):                    # amounts in 0.1 wan
        sun_amt = F(sun_amt10, 10)
        if 720 - sun_amt == F(8, 10) * sun_amt: sols.add(sun_amt / sun)
assert len(sols) == 1; v = sols.pop(); out['2026GD-37'] = (pick(v, {'A': 15, 'B': 20, 'C': 25, 'D': 10}), v)

# 2026GK-66: total 10 ha, jia = 2 yi, bing = yi - 2 -> bing (search in 0.01 ha)
sols = set()
for yi100 in range(1, 1001):
    yi = F(yi100, 100); jia = 2 * yi; bing = yi - 2
    if bing > 0 and jia + yi + bing == 10: sols.add(bing)
assert len(sols) == 1; v = sols.pop(); out['2026GK-66'] = (pick(v, {'A': 1, 'B': 2, 'C': 3, 'D': 4}), v)

# 2026ZJA-50: 14 tables in use (singles 2 players, doubles 4); doubles players = 1.5 x singles players;
# singles boys 13, doubles boys 15 -> singles girls minus doubles girls
sols = set()
for s in range(0, 15):
    d = 14 - s
    if 4 * d == F(3, 2) * 2 * s:
        gs, gd = 2 * s - 13, 4 * d - 15
        if gs >= 0 and gd >= 0: sols.add(gs - gd)
assert len(sols) == 1; v = sols.pop(); out['2026ZJA-50'] = (pick(v, {'A': -4, 'B': 4, 'C': -6, 'D': 6}), v)
for k, (a, v) in out.items(): print(k, 'answer', a, 'value', v)

# ---- 2021GK-67: value vs the two option orders ----
x = F(1)
sols = set()
for x10 in range(1, 1000):
    x = F(x10, 10)
    s3 = 8 * x; s2 = 7 * x; s1 = s2 / F(14, 10)
    front = s1 + s2 + s3; back = 3 * front; tot = front + back
    s5 = tot / 4; s4 = s5 / F(11, 10); s6 = back - s4 - s5
    if s6 - s5 == 16: sols.add(s6 - s3)
assert len(sols) == 1; v = sols.pop(); print('2021GK-67 value', float(v))
crop_order = {'A': lambda t: t < 100, 'B': lambda t: 100 <= t <= 120, 'C': lambda t: t > 140, 'D': lambda t: 120 < t <= 140}
orig_order = {'A': lambda t: t < 100, 'B': lambda t: 100 <= t <= 120, 'C': lambda t: 120 < t <= 140, 'D': lambda t: t > 140}
print('  crop option order ->', pick(v, crop_order), '| original paper order ->', pick(v, orig_order), '| official key: C')

# ---- 2026CQ-57: restored stem, both readings of the masked clause give the same answer ----
def cq57(child_rule):
    res = set()
    for s in range(1, 68):
        h = 2 * s - 1
        if s + h != 68: continue
        fam = F(2, 3) * h; pairs = h - fam
        assert fam.denominator == 1
        for fm in range(0, int(pairs) + 1):
            for fc in range(0, int(pairs) - fm + 1):
                mc = int(pairs) - fm - fc
                if not child_rule(fam, fm, fc, mc): continue
                child_g = fam + fc + mc
                for cs in range(0, s + 1):
                    if (s - cs) + 1 == cs: res.add(child_g + cs)
    return res
r1 = cq57(lambda fam, fm, fc, mc: 2 * (fam + fc + mc) == (fam + fm + fc) + (fam + fm + mc))   # all group photos
r2 = cq57(lambda fam, fm, fc, mc: 2 * (fc + mc) == (fm + fc) + (fm + mc))                     # two-person photos only
print('2026CQ-57 restored readings ->', r1, r2, '(official A = 52)')

# ---- 2022ZJA-60: two readings ----
by_patients = 900 * F(2, 10) - 200 * F(6, 10)
by_beds = 1000 * F(2, 10) - 1000 * F(6, 10)
print('2022ZJA-60 by patients', by_patients, '(official B=60) | by literal beds', by_beds, '(no option)')

# ---- 2020HB-75 with fractions 2/13, 9/16, 1/3 (from the official solution crop) ----
sols = [T for T in range(100, 3000) if (F(2, 15) * (T - 100) + 100) + (F(9, 25) * (T - 100) + 100) + (F(1, 4) * (T - 90) + 90) == T]
print('2020HB-75 total', sols, '(official A = 850)')

# ---- incoming OCR candidates tagged M01 (answers used in the replacement plan) ----
# 2021HB-63: sold x, unsold y: x+50 = y-50 ; x+150 = 1.5(y-150) -> unsold y
y = [y for y in range(1, 3000) for x in [y - 100] if x + 150 == F(3, 2) * (y - 150)]
print('2021HB-63 unsold', y, '-> C(550)')
# 2021HB-65: wool -> 15 hats or 20 gloves ; pack = 1 hat + 2 gloves
print('2021HB-65 packs', F(60) // (F(60, 15) + 2 * F(60, 20)), '-> C(6)')
# 2022SZ-51: three teams of 30 ; team1 boys = team2 girls ; team3 boys = 2/5 of all boys
res = set()
for b1 in range(0, 31):
    g2 = b1; b2 = 30 - g2
    for b3 in range(0, 31):
        if F(b3) == F(2, 5) * (b1 + b2 + b3): res.add((30 - b1) + g2 + (30 - b3))
print('2022SZ-51 girls', res, '-> B(40)')
# 2026HB-71: (220-40)*0.6 .. (220-40)*0.8
print('2026HB-71 range', (220 - 40) * F(6, 10), (220 - 40) * F(8, 10), '-> B(108-144)')
# 2026JS-56: 3 staff for logistics; 3 men -> hikers 3:5 ; 3 women -> 3:4 ; 2 men 1 woman -> ?
r = [(M, W) for M in range(3, 300) for W in range(3, 300) if 5 * (M - 3) == 3 * W and 4 * M == 3 * (W - 3)]
M, W = r[0]; print('2026JS-56', r, 'ratio', F(M - 2, W - 1), '-> C(11:17)')
# 2026JS-69: 20 S + 10 T = 240/h ; after +20% / +25% : +50 -> S'/T'
r = [(s, t) for s in range(1, 30) for t in range(1, 30) if 20 * s + 10 * t == 240 and 20 * s * F(1, 5) + 10 * t * F(1, 4) == 50]
s, t = r[0]; print('2026JS-69', r, 'ratio', F(s, 1) * F(6, 5) / (t * F(5, 4)), '-> B(2.4)')
