# Independent blind solver for D01 math (M01) questions.
# Every answer is derived from the stem data only (brute force / exact fractions),
# then matched against the four options; we require exactly one match.
import json, sys
from fractions import Fraction as F

QFILE = sys.argv[1]
qs = {q["vid"]: q for q in json.load(open(QFILE, encoding="utf-8"))}

def num(s):
    s = s.strip().replace("%", "")
    return F(s)

res = {}

# ---------- math-1 ----------
# v01: 60 study hours/year; per month 1 live (2h) + 2 tests (0.5 each); rest video, 45 min = 1 study hour.
need = F(60)
per_month_other = 1 * 2 + 2 * F(1, 2)
video_credit_year = need - 12 * per_month_other
video_minutes_month = video_credit_year * 45 / 12
res["D01-math-1-v01"] = video_minutes_month / 60          # hours / month

# v02: brute force over non-holiday hours h (allow halves too)
cands = []
for h2 in range(0, 2000):           # h = h2/2 hours
    h = F(h2, 2)
    raw = 10 * h + 15 * 10
    dep = raw if raw <= 300 else 300 + (raw - 300) / 2
    if dep == 340:
        cands.append(h)
assert len(cands) == 1, cands
res["D01-math-1-v02"] = cands[0]

# v03: brute force export E, import I = E*(1-0.375), E - I = 6000
c = [E + E * F(5, 8) for E in range(1, 200000) if E - E * F(5, 8) == 6000]
assert len(c) == 1
res["D01-math-1-v03"] = c[0]

# v04: brute force longan G, lychee 2G
c = []
for G in range(1, 5000):
    L = 2 * G
    L1, G1 = L * F(7, 10), G * F(1, 2)
    L2, G2 = L1 - 70, G1 - 70
    if G2 > 0 and L2 == 4 * G2:
        c.append(L + G)
assert len(c) == 1, c
res["D01-math-1-v04"] = c[0]

# v05: brute force Shenzhen S
c = []
for S in range(1, 100000):
    G, D, Fs = F(S) / F(5, 4), F(S, 2), F(S) / F(5, 2)
    if G - Fs == 200:
        c.append(S + G + D + Fs)
assert len(c) == 1
res["D01-math-1-v05"] = c[0]

# v06: shares
e = F(30, 100); b = e - F(10, 100); h = 1 - e - b
res["D01-math-1-v06"] = 48 / (h - b)

# v07: brute force contract total T (allow fractional to be safe: step 1/3)
c = []
for t3 in range(1, 6000):
    T = F(t3, 3)
    p1 = T / 3 - 20
    r1 = T - p1
    p2 = r1 * F(3, 5) + 6
    r2 = r1 - p2
    if p1 > 0 and p2 > 0 and r2 == 50:
        c.append(T)
assert len(c) == 1, c
res["D01-math-1-v07"] = c[0]

# v08: enumerate doctors n1 (day1), n2 = 30 - n1; totals T1, T2 = 1.4 T1, T1 + T2 = 480
c = []
for n1 in range(1, 30):
    n2 = 30 - n1
    T1 = F(480) / F(12, 5)
    T2 = T1 * F(7, 5)
    a1, a2 = T1 / n1, T2 / n2
    if a2 == a1 * F(7, 10):
        c.append(a1)
assert len(c) == 1, c
res["D01-math-1-v08"] = c[0]

# v09: unify ratios L:M = 2:3, M:S = 4:5 by brute force over small integer counts
c = set()
for Lc in range(1, 200):
    for Mc in range(1, 200):
        if 3 * Lc != 2 * Mc: continue
        if 5 * Mc % 4: continue
        Sc = 5 * Mc // 4
        wL, wM, wS = Lc * 5 * 2, Mc * 3 * 3, Sc * 2 * 4
        c.add(F(180) * (wL + wM + wS) / wS)
assert len(c) == 1, c
res["D01-math-1-v09"] = c.pop()

# v10: brute force last-year female x
c = []
for x in range(1, 1000):
    f, m = x + 10, 4 * x - 4
    if m > 0 and 2 * f == m:
        c.append(f + m)
assert len(c) == 1
res["D01-math-1-v10"] = c[0]

# v11: brute force k (scale) and d (newcomers per hall)
c = []
for k in range(1, 300):
    for d in range(0, 3000):
        A, B, C = 4 * k + d, 7 * k + d, 11 * k + d
        if 3 * A != 2 * B: continue
        A2, C2 = A + 30, C - 30
        if A2 == B and C2 >= 0:
            c.append(C2)
assert len(c) == 1, c
res["D01-math-1-v11"] = c[0]

# ---------- math-2 ----------
# v01
c = [N for N in range(1, 100000) if N * F(9, 10) * F(6, 10) == 324]
assert len(c) == 1
res["D01-math-2-v01"] = c[0]

# v02: enumerate goods in segments 1-20 (g1), 21-30 (g2 = 9), 31-50 (g3)
c = set()
for g1 in range(0, 21):
    for g3 in range(0, 21):
        g2 = 9
        if F(g1 + g2, 30) == F(70, 100) and F(g2 + g3, 30) == F(80, 100):
            c.add(F(g1 + g2 + g3, 50) * 100)
assert len(c) == 1, c
res["D01-math-2-v02"] = c.pop()

# v03
c = []
for n in range(1, 2000):
    tot = 7 * n + 90
    if 9 * n + 18 == tot:
        for m in range(0, 2000):
            if 6 * (n + m) == tot:
                c.append(m)
assert len(c) == 1
res["D01-math-2-v03"] = c[0]

# v04
c = []
for r in range(2, 2000):
    if 45 * r + 30 == 50 * (r - 1):
        c.append(45 * r + 30)
assert len(c) == 1
res["D01-math-2-v04"] = c[0]

# v05
c = []
for A in range(0, 3601):
    B = 3600 - A
    if A - B != 840: continue
    for x in range(0, A + 1):
        if (B + x) - (A - x) == 160:
            c.append(x)
assert len(c) == 1
res["D01-math-2-v05"] = c[0]

# v06: forward simulation over candidate originals
def sim(N):
    r = F(N)
    for _ in range(3):
        give = r / 2 + 10
        r -= give
        if r < 0: return None
    return r
c = [N for N in range(1, 10000) if sim(N) == 15]
assert len(c) == 1
res["D01-math-2-v06"] = c[0]

# v07: integer point units; tissue t, detergent d, oil o; 2o = 5d, 2d = 3t
c = set()
for t in range(1, 50):
    for d in range(1, 80):
        if 2 * d != 3 * t: continue
        for o in range(1, 200):
            if 2 * o != 5 * d: continue
            pts = 12 * o
            left = pts - 3 * o - 4 * d
            c.add(left // t)
assert len(c) == 1, c
res["D01-math-2-v07"] = c.pop()

# v08
c = []
for b in range(1, 1000):
    for f in range(1, 1000):
        if 4 * b + 3 * f == 960 and 3 * b + 4 * f == 1000:
            c.append(b + f)
assert len(c) == 1
res["D01-math-2-v08"] = c[0]

# v09: enumerate all splits; answer must be invariant
c = set()
for am in range(0, 67):            # jia male
    bm = 66 - am                   # yi male
    for bf in range(0, 55):        # yi female
        af = 54 - bf
        if af < 0: continue
        if am - bf == 9:
            c.add(bm + bf)
assert len(c) == 1, c
res["D01-math-2-v09"] = c.pop()

# v10
paid = {"jia": 1260, "yi": 780, "bing": 420, "ding": 0}
share = F(sum(paid.values()), 4)
res["D01-math-2-v10"] = paid["jia"] - share

# v11
bags = {"jia": 5, "yi": 3, "bing": 0}
eat = F(sum(bags.values()), 3)
price = F(48) / eat               # bing ate `eat` bags and paid 48
res["D01-math-2-v11"] = (bags["jia"] - eat) * price

# ---------- match options ----------
out = {}
ok = True
for vid, val in res.items():
    q = qs[vid]
    hits = [k for k, v in q["options"].items() if num(v) == F(val)]
    out[vid] = {"value": str(val), "hits": hits}
    flag = "" if len(hits) == 1 else "   <-- PROBLEM"
    if len(hits) != 1: ok = False
    print(f"{vid}: value={val}  option(s)={hits}{flag}")
missing = set(qs) - set(res)
print("unsolved:", missing)
print("ALL UNIQUE" if ok and not missing else "CHECK!")
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
