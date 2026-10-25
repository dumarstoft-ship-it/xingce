# Blind independent solver for revh2_A (written before opening the key).
# Every answer is computed from the stem data only (brute force where feasible).
from fractions import Fraction as Fr
from itertools import combinations, product

OPTS = {
    "D02-math-h-v01": {"A": 216, "B": 240, "C": 276, "D": 300},
    "D02-math-h-v02": {"A": 4, "B": 5, "C": 6, "D": 12},
    "D04-math-h-v01": {"A": 304, "B": 360, "C": 380, "D": 400},
    "D04-math-h-v02": {"A": Fr(4, 9), "B": Fr(5, 9), "C": Fr(4, 5), "D": Fr(4)},   # 'about 44.4%' etc.
    "D04-math-h-v06": {"A": Fr(3, 2), "B": Fr(5, 2), "C": Fr(15, 4), "D": Fr(15, 2)},
    "D04-math-h-v07": {"A": Fr(2, 5), "B": Fr(1, 2), "C": Fr(1, 5), "D": Fr(1, 4)},
    "D06-math-h-v02": {"A": Fr(63, 100), "B": Fr(1, 10), "C": Fr(343, 1000), "D": Fr(37, 100)},
    "D06-math-h-v08": {"A": Fr(2, 5), "B": Fr(3, 7), "C": Fr(16, 35), "D": Fr(1, 2)},
    "D06-math-h-v09": {"A": Fr(1, 5), "B": Fr(1, 4), "C": Fr(1, 3), "D": Fr(2, 5)},
}

def letters(vid, val, approx=False):
    hits = []
    for k, v in OPTS[vid].items():
        if approx:
            if abs(float(v) - float(val)) < 5e-4:
                hits.append(k)
        elif v == val:
            hits.append(k)
    return hits

res = {}

# ---------- D02-math-h-v01 ----------
# Day 1: each line 210 pieces, start 8:00. 11:30 (t=3.5h) C done, B has 35 left.
# When B done, A has 42 left. Day 2: 690 pieces, A,B start 8:00, C starts 9:00, all finish together.
t1 = Fr(7, 2)
vC = Fr(210) / t1
vB = Fr(210 - 35) / t1
tB = Fr(210) / vB
vA = Fr(210 - 42) / tB
# brute force over finishing time T (in minutes after 8:00) so that allocations sum to 690
sol = []
for Tmin in range(61, 24 * 60):
    T = Fr(Tmin, 60)
    a, b, c = vA * T, vB * T, vC * (T - 1)
    if a + b + c == 690:
        sol.append((T, a, b, c))
print("v01 rates A,B,C =", vA, vB, vC, " solutions:", sol)
assert len(sol) == 1
res["D02-math-h-v01"] = letters("D02-math-h-v01", sol[0][3])
# distractor sources
print("   same start, C share:", Fr(690) * vC / (vA + vB + vC),
      " naive minus one hour:", Fr(690) * vC / (vA + vB + vC) - vC,
      " C*T:", vC * sol[0][0])

# ---------- D02-math-h-v02 ----------
# 45 people, supplies = 45*28 person-days. After x days, 5 return along the same route at same speed
# (needs x days of supply each, taken from current stock). Remaining 40 continue; stock runs out 2 days later
# than originally planned (day 30).
total = 45 * 28
sol = []
for x in range(1, 28):
    stock = total - 45 * x - 5 * x          # after 5 take their return supply
    if stock == 40 * (30 - x):
        sol.append(x)
print("v02 solutions x =", sol)
assert len(sol) == 1
res["D02-math-h-v02"] = letters("D02-math-h-v02", sol[0])
# distractor: forget that returners take supplies
print("   forget return supply:", [x for x in range(1, 28) if total - 45 * x == 40 * (30 - x)])
print("   double return supply :", [x for x in range(1, 28) if total - 45 * x - 10 * x == 40 * (30 - x)])

# ---------- D04-math-h-v01 ----------
# cost: 200 + 10%*200 + 8 = 228; sell at 0.9P; commission = 20% of 0.9P.
# profit >= 20% of total cost (incl. commission). Find minimal list price P.
def ok_price(P, disc=Fr(9, 10), comm=Fr(1, 5), base_incl_comm=True):
    S = P * disc
    cost = Fr(200) + Fr(200) / 10 + 8 + comm * S
    base = cost if base_incl_comm else Fr(228)
    return S - cost >= Fr(1, 5) * base

# exact minimal P (linear) by bisection on Fractions, then confirm with options
lo, hi = Fr(0), Fr(10000)
for _ in range(200):
    mid = (lo + hi) / 2
    if ok_price(mid):
        hi = mid
    else:
        lo = mid
Pmin = Fr(round(float(hi) * 1000), 1000)
print("v01(D04) minimal list price ~", float(hi), " options satisfying:",
      {k: ok_price(Fr(v)) for k, v in OPTS["D04-math-h-v01"].items()})
assert ok_price(Fr(400)) and not ok_price(Fr(400) - Fr(1, 1000))
res["D04-math-h-v01"] = ["D"] if ok_price(Fr(400)) and not ok_price(Fr(39999, 100)) else []
# distractor sources
S_sol = Fr(4, 5) * 0  # placeholder
print("   ignore commission: P =", Fr(228) * Fr(6, 5) / Fr(9, 10),
      " transaction price S =", Fr(400) * Fr(9, 10),
      " ignore discount (sell at P):", Fr(228) * Fr(6, 5) / (1 - Fr(1, 5) - Fr(1, 5) * Fr(1, 5)),
      " base excl. commission:", Fr(228) * Fr(6, 5) / (Fr(9, 10) * (1 - Fr(1, 5))))

# ---------- D04-math-h-v02 ----------
# F = frozen profit 2024 (>0), L = prepared-food loss 2024 (>0).
# 2025: 1.1F - 0.6L = 1.5 (F - L). Find L/F. Solve over a grid of F to be safe.
F = Fr(1)
# 1.1F - 0.6L = 1.5F - 1.5L -> 0.9L = 0.4F
L = (Fr(15, 10) - Fr(11, 10)) * F / (Fr(15, 10) - Fr(6, 10))
assert Fr(11, 10) * F - Fr(6, 10) * L == Fr(3, 2) * (F - L) and F - L > 0
print("v02(D04) L/F =", L / F, float(L / F))
res["D04-math-h-v02"] = letters("D04-math-h-v02", L / F)
print("   sign error (loss x1.4):", (Fr(15, 10) - Fr(11, 10)) / (Fr(15, 10) - Fr(14, 10)),
      " total/F:", 1 - L / F)

# ---------- D04-math-h-v06 ----------
# weekday w, weekend s (daily, before), price p. After: weekday 0.5p*3w, weekend 0.8p*1.25s.
# 5 weekdays + 2 weekend days, weekly revenue +20%.
# 5*1.5w + 2*1.0s = 1.2*(5w + 2s)
w = Fr(1)
s = (Fr(5) * Fr(3, 2) - Fr(6, 5) * 5) * w / (Fr(6, 5) * 2 - 2)
assert 5 * Fr(3, 2) * w + 2 * s == Fr(6, 5) * (5 * w + 2 * s)
print("v06(D04) s/w =", s, float(s))
res["D04-math-h-v06"] = letters("D04-math-h-v06", s / w)
print("   ignore 5:2 days:", (Fr(3, 2) - Fr(6, 5)) / (Fr(6, 5) - 1),
      " 2s/w:", 2 * s)

# ---------- D04-math-h-v07 ----------
# fixed monthly cost K, per-meal food c, Jan n meals. avg = K/n + c.
# March: 1.25n meals, avg = 0.9*(K/n + c). Month X: 2n meals. decrease?
# brute: set n=1, K=1 and solve c.
n, K = Fr(1), Fr(1)
# K/(1.25n) + c = 0.9(K/n + c) -> 0.1c = 0.9K/n - 0.8K/n
c = (Fr(9, 10) * K / n - K / (Fr(5, 4) * n)) / Fr(1, 10)
jan = K / n + c
assert K / (Fr(5, 4) * n) + c == Fr(9, 10) * jan
x2 = K / (2 * n) + c
dec = (jan - x2) / jan
print("v07(D04) c =", c, " decrease =", dec)
res["D04-math-h-v07"] = letters("D04-math-h-v07", dec)

# ---------- D06-math-h-v02 ----------
pairs = list(combinations(range(5), 2))
good = 0
for a, b, cc in product(pairs, repeat=3):
    if set(a) & set(b) and set(a) & set(cc) and set(b) & set(cc):
        good += 1
p = Fr(good, len(pairs) ** 3)
print("v02(D06) P =", p, float(p), " (pairwise P =",
      Fr(sum(1 for a, b in product(pairs, repeat=2) if set(a) & set(b)), 100), ")")
res["D06-math-h-v02"] = letters("D06-math-h-v02", p)
common = sum(1 for a, b, cc in product(pairs, repeat=3) if set(a) & set(b) & set(cc))
print("   all three share a common base:", Fr(common, 1000))

# ---------- D06-math-h-v08 ----------
boxA = ["S"] * 3 + ["H"] * 2
boxB = ["S"] * 2 + ["H"] * 3
num = Fr(0)
moves = list(combinations(range(5), 2))
for mv in moves:
    newB = boxB + [boxA[i] for i in mv]
    num += Fr(newB.count("S"), len(newB)) / len(moves)
print("v08(D06) P(S) =", num)
res["D06-math-h-v08"] = letters("D06-math-h-v08", num)

# ---------- D06-math-h-v09 ----------
subs = list(combinations(range(6), 3))   # 0 = Jia, 1 = Yi
atleast = [t for t in subs if 0 in t or 1 in t]
both = [t for t in subs if 0 in t and 1 in t]
cp = Fr(len(both), len(atleast))
print("v09(D06) P(both | at least one) =", cp, " uncond P(both)=", Fr(len(both), len(subs)),
      " P(both | Jia) =", Fr(len(both), len([t for t in subs if 0 in t])))
res["D06-math-h-v09"] = letters("D06-math-h-v09", cp)

print()
for k, v in res.items():
    print(k, v)
    assert len(v) == 1, k
