"""Independent checks of D11 (M11 容斥) real + teacher answers, solved from the stem data."""
from fractions import Fraction as F
from itertools import product
res = {}

def pick(opts, val):
    hits = [k for k, v in opts.items() if v == val]
    assert len(hits) == 1, (opts, val, hits)
    return hits[0]

# 2025GK-69: 60% A, 45% B, both - neither = 2; total?
opts = {'A': 100, 'B': 50, 'C': 40, 'D': 20}
ok = []
for N, k in [(v, k) for k, v in opts.items()]:
    A, B = F(60, 100) * N, F(45, 100) * N
    if A.denominator != 1 or B.denominator != 1: continue
    # find integer neither y >= 0 with both = y+2, both<=min(A,B), union consistent
    for y in range(N + 1):
        both = y + 2
        if both <= min(A, B) and A + B - both == N - y: ok.append(k); break
res['2025GK-69'] = ok

# 2015ZJA-62: days; a both active, b morning-only active, c afternoon-only active, d both inactive
sols = set()
for a, b, c, d in product(range(20), repeat=4):
    if d != 0: continue                      # (4) afternoon inactive -> morning active
    if b + c + d != 7: continue              # (1) days with some inactivity
    if a + c != 5: continue                  # (2) afternoons active
    if a + b != 6: continue                  # (3) mornings active
    sols.add(a + b + c + d)
res['2015ZJA-62'] = [pick({'A': 7, 'B': 8, 'C': 9, 'D': 10}, n) for n in sols]

# 2020SZ1-54 (stem fraction 2/3 restored): eat 90%; banana = 3*sausage; both = 2/3 * only-sausage
sols = set()
for os_ in range(1, 200):
    both = F(2, 3) * os_
    if both.denominator != 1: continue
    sausage = os_ + both; banana = 3 * sausage; ob = banana - both
    eat = ob + both + os_; N = eat / F(9, 10)
    if N.denominator != 1: continue
    sols.add((N - eat) / ob)
res['2020SZ1-54'] = [pick({'A': F(1, 5), 'B': F(3, 10), 'C': F(2, 13), 'D': F(4, 15)}, s) for s in sols]

# 2023GD-35: 200 people; magazine = 1.88 * only-newspaper; neither?
vals = set()
for po in range(1, 201):
    m = F(188, 100) * po
    if m.denominator != 1: continue
    nei = 200 - m - po
    if nei >= 0: vals.add(int(nei))
opts = {'A': 36, 'B': 56, 'C': 76, 'D': 96}
res['2023GD-35'] = [k for k, v in opts.items() if v in vals]

# 2023ZJA-63: 70-79 students; 12% fail both; 2/3 pass English; math pass = eng + 10; both pass?
ans = set()
for N in range(70, 80):
    nf, e = F(12, 100) * N, F(2, 3) * N
    if nf.denominator != 1 or e.denominator != 1: continue
    m = e + 10; both = e + m - (N - nf)
    if 0 <= both <= min(e, m): ans.add(int(both))
res['2023ZJA-63'] = [pick({'A': 31, 'B': 37, 'C': 41, 'D': 44}, a) for a in ans]

# 2021SC2-46: A = 4/13 N, B = 25, both = N/14; min neither
best = None
for N in range(1, 5000):
    A, both = F(4, 13) * N, F(1, 14) * N
    if A.denominator != 1 or both.denominator != 1: continue
    if both > min(A, 25): continue
    nei = N - (A + 25 - both)
    if nei < 0: continue
    best = nei if best is None else min(best, nei)
res['2021SC2-46'] = [pick({'A': 57, 'B': 67, 'C': 114, 'D': 134}, int(best))]

# 2023GK-70: 287; both = 1.21 * only-F; both = only-Y + 76; neither?
ans = set()
for oF in range(1, 288):
    both = F(121, 100) * oF
    if both.denominator != 1: continue
    oY = both - 76
    if oY < 0: continue
    nei = 287 - oF - oY - both
    if nei >= 0: ans.add(int(nei))
res['2023GK-70'] = [pick({'A': 21, 'B': 23, 'C': 25, 'D': 27}, a) for a in ans]

# 2015GK-73: non-standard; surveyed = returned; sent = returned / 0.9
returned = 179 + 146 + 246 - 24 - 2 * 115 + 52
res['2015GK-73'] = [pick({'A': 310, 'B': 360, 'C': 390, 'D': 410}, F(returned) / F(9, 10))]

# T023: 55 all in >=1; 35, 28, 31; triple 6; only one?
S, P, t = 35 + 28 + 31, 55, 6
x2 = S - P - 2 * t  # from x1+x2+t=P, x1+2x2+3t=S
res['T023'] = [pick({'A': 45, 'B': 33, 'C': 29, 'D': 22}, P - x2 - t)]

# 2024SZ-58: 725, 8 none, 360/380/237, triple 60; only one?
S, P, t = 360 + 380 + 237, 725 - 8, 60
x2 = S - P - 2 * t
res['2024SZ-58'] = [pick({'A': 517, 'B': 516, 'C': 515, 'D': 514}, P - x2 - t)]

# 2025JSA-58: 45, none 5, 21/22/19, at least two = 12; triple?
ans = set()
for x2 in range(13):
    t = 12 - x2
    x1 = 40 - 12
    if x1 + 2 * x2 + 3 * t == 62: ans.add(t)
res['2025JSA-58'] = [pick({'A': 7, 'B': 8, 'C': 9, 'D': 10}, a) for a in ans]

# T100: 48, only-one = at-least-two = 4 * triple; tickets?
ans = set()
for t in range(1, 49):
    x1 = 4 * t; x2 = 4 * t - t
    if x1 + x2 + t == 48: ans.add(x1 + 2 * x2 + 3 * t)
res['T100'] = [pick({'A': 48, 'B': 72, 'C': 78, 'D': 84}, a) for a in ans]

# 2020SZS-25: total 15t, standard formula, everyone >=1; only English?
ans = set()
for t in range(1, 30):
    if 17 + 21 + 23 - 7 - 6 - 6 + t == 15 * t: ans.add(17 - 7 - 6 + t)
res['2020SZS-25'] = [pick({'A': 4, 'B': 5, 'C': 6, 'D': 7}, a) for a in ans]

# T101: symbolic check x = 4y + 6 for random a,y
import random
okA = True
for _ in range(50):
    a, y = random.randint(60, 300), random.randint(1, 20)
    # a = 48 + (a-42) + 6y - x - 2y  ->  x = 4y + 6
    x = 48 + (a - 42) + 6 * y - 2 * y - a
    okA &= (x == 4 * y + 6)
res['T101'] = ['A' if okA else '?']

# 2016GK-73: brute force regions; Li knows E & J (maybe F); others know exactly one
ans = set()
for e, f, j in product(range(10), repeat=3):
    if e + f + j != 9: continue
    for li_f in (0, 1):
        E, Fr, J = e + 1, f + li_f, j + 1
        if Fr == E + 4 and Fr == 2 * J: ans.add(e)
res['2016GK-73'] = [pick({'A': 2, 'B': 0, 'C': 3, 'D': 1}, a) for a in ans]

# 2023SZ-57: solve regions
ans = set()
a1, b1, c1, ab = 40 * F(1, 4), 36 * F(1, 4), 35 * F(1, 5), 4
for t in range(0, 36):
    ac = 40 - a1 - ab - t; bc = 36 - b1 - ab - t
    if ac < 0 or bc < 0: continue
    if ac != bc + 3: continue
    if c1 + ac + bc + t != 35: continue
    ans.add(t)
res['2023SZ-57'] = [pick({'A': 15, 'B': 21, 'C': 27, 'D': 33}, a) for a in ans]

# 2025GKD-69: brute force regions
ans = set()
n = 65 - 52; c, abc = 3, 6
for a, b, ab, ac, bc in product(range(53), repeat=5):
    if a + b + c + ab + ac + bc + abc != 52: continue
    notA = b + c + bc + n; hasB = b + ab + bc + abc
    if notA == hasB: ans.add(ab)
res['2025GKD-69'] = [pick({'A': 10, 'B': 13, 'C': 16, 'D': 19}, a) for a in ans]

# 2024GK-73: R subset E; R∩F = R/2; (E∩F) = E/2; triple 50; exactly two 100; exactly one 150
ans = set()
for e, f, r, ef, er, rf, t in product(range(0, 201, 5), range(0, 201, 5), [0], range(0, 101, 5), range(0, 101, 5), [0], [50]):
    # r-only = 0 and R∩F-not-E = 0 since R ⊂ E
    R = er + t
    if 2 * (t) != R: continue                 # half of Russian speakers also French (R∩F = t)
    E = e + ef + er + t
    if 2 * (ef + t) != E: continue            # half of English speakers know French
    if ef + er + rf != 100: continue
    if e + f + r != 150: continue
    ans.add(f + ef + rf + t)
res['2024GK-73'] = [pick({'A': 100, 'B': 200, 'C': 50, 'D': 150}, a) for a in ans]

# 2019GK-65: 100; this year excellent = 1.2 last; (non-excellent share) down 15 points
ans = set()
for x in range(1, 101):
    y = F(12, 10) * x
    if y.denominator != 1 or y > 100: continue
    if (100 - y) == (100 - x) - 15: ans.add(int(x + y - 100))
res['2019GK-65'] = [pick({'A': 55, 'B': 65, 'C': 75, 'D': 85}, a) for a in ans]

# 2015ZJA-64: pairwise incl. triple 31,37,16; some have 3, some have 1; min cannot interview
best = None
for t in range(1, 17):
    atl2 = 31 + 37 + 16 - 2 * t
    rest = 135 - atl2            # only-one + none must be >= 1 (some have only one)
    if rest >= 1: best = rest if best is None else min(best, rest)
res['2015ZJA-64'] = [pick({'A': 51, 'B': 50, 'C': 53, 'D': 52}, best)]

# T104: 60; 40/38/31; triple 18; max none — brute force over regions
best = -1
for ab, ac, bc in product(range(0, 23), range(0, 14), range(0, 14)):
    a = 40 - 18 - ab - ac; b = 38 - 18 - ab - bc; c = 31 - 18 - ac - bc
    if min(a, b, c) < 0: continue
    none = 60 - (a + b + c + ab + ac + bc + 18)
    if none >= 0: best = max(best, none)
res['T104'] = [pick({'A': 14, 'B': 15, 'C': 16, 'D': 18}, best)]

# T105: students 1..100; red every 3 from 1; blue every 4; yellow every 7; count with >=2 flags
cnt = 0
for s in range(1, 101):
    k = ((s - 1) % 3 == 0) + ((s - 1) % 4 == 0) + ((s - 1) % 7 == 0)
    cnt += k >= 2
res['T105'] = [pick({'A': 13, 'B': 14, 'C': 15, 'D': 16}, cnt)]

# 2015GK-72: March 1..31; every 3/5/8 days from day 1; days with no inspection
free = sum(1 for d in range(1, 32) if not ((d - 1) % 3 == 0 or (d - 1) % 5 == 0 or (d - 1) % 8 == 0))
res['2015GK-72'] = [pick({'A': 12, 'B': 13, 'C': 14, 'D': 15}, free)]

# extra (unused) checks
res['T106'] = [pick({'A': 15, 'B': 16, 'C': 17, 'D': 18}, 280 - (60 + 170 + 150 - 22 - 60 - 35))]
res['T166'] = [pick({'A': 46, 'B': 47, 'C': 53, 'D': 54}, sum(1 for i in range(1, 101) if i % 3 and i % 5))]
res['2024JSA-64'] = [pick({'A': 10, 'B': 28, 'C': 62, 'D': 72}, 90 - (108 - 80))]
res['2022GD-33'] = [pick({'A': 16, 'B': 40, 'C': 46, 'D': 54}, 40 + 46 - (80 - 10))]

for k, v in res.items(): print(k, v)
