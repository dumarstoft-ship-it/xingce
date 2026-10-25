"""Self-solve the 4 M01 real questions that have no official answer.
Each is solved by brute force from the stem data, then matched against the 4 options."""
from fractions import Fraction as F

def match(val, opts):
    hits = [k for k, v in opts.items() if F(v) == F(val)]
    assert len(hits) == 1, (val, opts, hits)
    return hits[0]

out = {}
# 2026GD-36: wind 40%, PV 35%, rest biomass; PV - biomass = 120 MW -> total
sol = [T for T in range(1, 100000) if F(35, 100) * T - (1 - F(40, 100) - F(35, 100)) * T == 120]
assert len(sol) == 1
out['2026GD-36'] = (match(sol[0], {'A': 600, 'B': 800, 'C': 1000, 'D': 1200}), sol[0])

# 2026GD-37: Sat clients = 1.5 Sun clients; Sat amount = 80% Sun amount; 40 clients; 720 wan -> Sun avg
sol = []
for sun in range(1, 40):
    sat = 40 - sun
    if 2 * sat != 3 * sun: continue
    for sun_amt10 in range(1, 7200):           # amounts in 0.1 wan
        sun_amt = F(sun_amt10, 10); sat_amt = 720 - sun_amt
        if sat_amt == F(8, 10) * sun_amt: sol.append(sun_amt / sun)
assert len(sol) == 1
out['2026GD-37'] = (match(sol[0], {'A': 15, 'B': 20, 'C': 25, 'D': 10}), sol[0])

# 2026GK-66: jia + yi + bing = 10 ha, jia = 2 yi, bing = yi - 2 -> bing
sol = []
for yi10 in range(1, 101):
    yi = F(yi10, 10); jia = 2 * yi; bing = yi - 2
    if bing > 0 and jia + yi + bing == 10: sol.append(bing)
assert len(sol) == 1
out['2026GK-66'] = (match(sol[0], {'A': 1, 'B': 2, 'C': 3, 'D': 4}), sol[0])

# 2026ZJA-50: 14 tables (singles: 2 players, doubles: 4); doubles players = 1.5 x singles players;
# singles boys 13, doubles boys 15 -> singles girls - doubles girls
sol = []
for s in range(0, 15):
    d = 14 - s
    if 2 * (4 * d) == 3 * (2 * s):
        g_single = 2 * s - 13; g_double = 4 * d - 15
        if g_single >= 0 and g_double >= 0: sol.append(g_single - g_double)
assert len(sol) == 1
out['2026ZJA-50'] = (match(sol[0], {'A': -4, 'B': 4, 'C': -6, 'D': 6}), sol[0])

for k, v in out.items():
    print(k, 'answer', v[0], 'value', v[1])
