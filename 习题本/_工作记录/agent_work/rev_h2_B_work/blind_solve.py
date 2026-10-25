#!/usr/bin/env python3
"""Blind independent solver for revh2_B questions (written before opening the key).
Each block derives the answer from the stem data only (brute force / exact arithmetic)."""
from fractions import Fraction as F
from math import ceil

OPTS = {
 "v01": {"A": 45, "B": 59, "C": 80, "D": 180},
 "v04": {"A": 360, "B": 400, "C": 540, "D": 560},
 "v07": {"A": 5, "B": 7, "C": 8, "D": 9},
 "v09": {"A": 28, "B": 40, "C": 55, "D": 60},
 "v12": {"A": 7, "B": 10, "C": 11, "D": 13},
 "v13": {"A": 104, "B": 107, "C": 108, "D": 116},
 "v15": {"A": 1, "B": 2, "C": 6, "D": 8},
 "v17": {"A": 20, "B": 32, "C": 50, "D": 70},
 "D04v08": {"A": 400, "B": 500, "C": 300, "D": 375},
 "D04v09": {"A": 6, "B": 7, "C": 8, "D": 5},
 "D04v12": {"A": 9000, "B": 10000, "C": 12000, "D": 18000},
}

def letter(key, val):
    hits = [k for k, v in OPTS[key].items() if v == val]
    return hits

res = {}

# ---------- D01 v01: two hypothetical transfers ----------
sols = []
for A in range(0, 2001):
    for B in range(0, 2001):
        if A >= 35 and B + 35 == 3 * (A - 35) and B >= 40 and A + 40 == 2 * (B - 40):
            sols.append((A, B))
res["v01"] = sols
print("v01 solutions (A,B):", sols, "-> letter", letter("v01", sols[0][0]))

# ---------- D01 v04: dispatch share 15% -> 10% ----------
sols = []
for N in range(1, 100001):
    d = F(15, 100) * N
    if d.denominator != 1:
        continue
    d2 = d - 10 - 20          # 10 converted (still employed), 20 returned (leave)
    tot2 = N - 20
    if d2 >= 0 and tot2 > 0 and F(d2, tot2) == F(1, 10):
        sols.append(N)
print("v04 N:", sols, "-> letter", letter("v04", sols[0]))

# ---------- D01 v07: capital x months ----------
sols = []
jia = 30 * 12
bing = 80 * len(range(8, 13))       # joins at start of Aug: Aug..Dec
for k in range(1, 13):              # withdraw 40 at start of month k
    yi = sum(80 if m < k else 40 for m in range(1, 13))
    if yi == 2 * bing:
        sols.append(k)
print("v07 month:", sols, "(bing months=%d)" % len(range(8, 13)), "-> letter", letter("v07", sols[0]))

# ---------- D01 v09: percentages ----------
# 2024: Aug=a, Sep=0.6a ; 2025: Aug=b, Sep=0.75b ; (b+0.75b) = 1.4(a+0.6a)
a = F(1)
b = F(14, 10) * (a + F(6, 10) * a) / (1 + F(75, 100))
g = (F(75, 100) * b) / (F(6, 10) * a) - 1
print("v09 growth:", g, float(g) * 100, "% -> letter", letter("v09", int(g * 100)))

# ---------- D01 v12: teacher rotation ----------
sols = set()
for B in range(20, 200):
    A = B - 12
    C = B - 9
    for xj in range(1, 30):          # 甲 group -> 丙
        for xy in range(1, 30):      # 乙 group -> 甲
            xb = 30 - xj - xy        # 丙 group -> 乙
            if xb < 1:
                continue
            if xj > A or xy > B or xb > C:
                continue
            ja = A - xj + xy
            ya = B - xy + xb
            ba = C - xb + xj
            if ja == ya == ba:
                sols.add((xj, xy, xb))
print("v12 (x甲,x乙,x丙):", sorted(sols), "-> letter", letter("v12", sorted(sols)[0][2]))

# ---------- D01 v13: three doubling transfers ----------
sols = []
for a0 in range(0, 201):
    for b0 in range(0, 201 - a0):
        c0 = 200 - a0 - b0
        A, B, C = a0, b0, c0
        ok = True
        # step1: A gives B, C each their own amount
        give = B + C
        if A < give: ok = False
        A, B, C = A - give, 2 * B, 2 * C
        # step2: B gives
        give = A + C
        if ok and B < give: ok = False
        A, B, C = 2 * A, B - give, 2 * C
        # step3: C gives
        give = A + B
        if ok and C < give: ok = False
        A, B, C = 2 * A, 2 * B, C - give
        if ok and 8 * C == 7 * A:
            sols.append((a0, b0, c0, A, B, C))
print("v13 solutions (a0,b0,c0 -> final):", sols)
# also: which options pass only the divisibility test / only the ratio test without nonneg
print("v13 option diagnostics:")
for L, a0 in OPTS["v13"].items():
    k = a0 - 100                      # final A = 8(a0-100)
    fa, fc = 8 * k, 7 * k
    fb = 200 - fa - fc
    # reverse with exact fractions
    A3, B3, C3 = F(fa), F(fb), F(fc)
    A2, B2 = A3 / 2, B3 / 2; C2 = C3 + A2 + B2
    A1, C1 = A2 / 2, C2 / 2; B1 = B2 + A1 + C1
    B0, C0 = B1 / 2, C1 / 2; A0 = A1 + B0 + C0
    print("  ", L, a0, "final", (fa, fb, fc), "init", (A0, B0, C0),
          "integers" if all(x.denominator == 1 for x in (A2, B2, C2, A1, B1, C1, A0, B0, C0)) else "NON-INTEGER",
          "nonneg" if min(fb, B2, B1, B0, C0) >= 0 else "NEGATIVE")

# ---------- D01 v15: trucks ----------
sols = set()
for x in range(1, 60):      # big capacity
    for y in range(1, 60):  # small capacity
        W1 = 5 * (2 * x + 4 * y)
        W2 = 4 * (1 * x + 7 * y)
        if W1 != W2:
            continue
        for n in range(0, 15):
            if 2 * (n * x + (14 - n) * y) == W1:
                sols.add(n)
print("v15 big trucks:", sols, "-> letter", letter("v15", list(sols)[0]))

# ---------- D01 v17: taxi split ----------
sols = []
for d10 in range(1, 2000):     # shared distance in 0.1 km
    d = F(d10, 10)
    r = F(150) / (18 + d + 12)
    jia = r * 18 / 2 + r * d / 3
    bing = r * d / 3 + r * 12 / 2
    if jia - bing == 9:
        sols.append(d)
print("v17 shared km:", sols, "-> letter", letter("v17", int(sols[0])))

# ---------- D04 v08: EOQ with integer batches ----------
def cost_n(n):  # n batches per year, Q = 3000/n
    Q = F(3000, n)
    return 160 * n + 6 * Q / 2
print("D04v08 continuous optimum Q = sqrt(2*3000*160/6) =", (2 * 3000 * 160 / 6) ** 0.5)
cands = []
for n in range(1, 3001):
    cands.append((cost_n(n), n, F(3000, n)))
cands.sort()
print("D04v08 best integer-n (any Q):", [(float(c), n, str(Q)) for c, n, Q in cands[:4]])
div = [(cost_n(n), n, 3000 // n) for n in range(1, 3001) if 3000 % n == 0]
div.sort()
print("D04v08 best with n|3000 (integer bags):", [(float(c), n, Q) for c, n, Q in div[:4]])
for L, Q in OPTS["D04v08"].items():
    n = F(3000, Q)
    print("   option", L, Q, "batches", n, "cost", float(160 * n + 3 * Q))

# ---------- D04 v09: parking ----------
sols = []
for a_ in range(1, 30):
    for b2 in range(1, 200):        # b in 0.5 steps
        b_ = F(b2, 2)
        def fee(hours):
            h = ceil(hours)
            return 3 * min(h, a_) + b_ * max(0, h - a_)
        if fee(4 + F(20, 60)) == 19 and fee(7 + F(35, 60)) == 34:
            # max duration with fee 24: billed hours h with fee 24
            hs = [h for h in range(1, 100) if 3 * min(h, a_) + b_ * max(0, h - a_) == 24]
            sols.append((a_, b_, hs))
print("D04v09 (a,b,billed hours for 24):", sols)

# ---------- D04 v12: cost-profit ratio ----------
def total_cost(n):
    return 120000 + 40 * min(n, 6000) + 30 * max(0, n - 6000)
nmin = None
for n in range(1, 200001):
    C = total_cost(n)
    if F(60 * n - C, C) >= F(1, 5):
        nmin = n
        break
print("D04v12 min n:", nmin, "-> letter", letter("D04v12", nmin))
# check monotonic after nmin
bad = [n for n in range(nmin, 200001) if F(60 * n - total_cost(n), total_cost(n)) < F(1, 5)]
print("D04v12 any failure above nmin:", bad[:5])
