# Independent blind solver for D04 math (M05 economic/profit) adapted questions.
# Every answer is computed from the stem data only (no answer key used).
import json, math, re, sys
from fractions import Fraction as F
import sympy as sp

QFILE = sys.argv[1]
qs = {q["vid"]: q for q in json.load(open(QFILE, encoding="utf-8"))}

def num(s):
    """Parse the first number in an option string ('约11.1%' -> 11.1, '$1.5m$' -> 1.5)."""
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    return F(m.group()) if m else None

def match_numeric(vid, value, tol=F(1, 100)):
    opts = qs[vid]["options"]
    hits = [k for k, v in opts.items() if num(v) is not None and abs(num(v) - F(value)) <= tol]
    return hits

results = {}

def record(vid, hits, detail):
    ok = len(hits) == 1
    results[vid] = (hits[0] if ok else hits, detail)
    print(f"{vid}: {'OK ' if ok else '!! '} answer={hits}  | {detail}")

# ---------------- 1-v01: same selling price, +20% / -20%, total loss 25
P = sp.symbols("P", positive=True)
sol = sp.solve(sp.Eq(P / sp.Rational(6, 5) + P / sp.Rational(4, 5) - 2 * P, 25), P)[0]
record("D04-math-1-v01", match_numeric("D04-math-1-v01", F(str(sol))), f"P={sol}")

# ---------------- 1-v02: A buys a, sells +20% to B; B sells -10% to C for 540
a = F(540) / (F(6, 5) * F(9, 10))
profitA = F(6, 5) * a - a
profitB = F(540) - F(6, 5) * a
total = profitA + profitB
opts = qs["D04-math-1-v02"]["options"]
hits = [k for k, v in opts.items() if ("盈利" in v if total > 0 else "亏损" in v) and num(v) == abs(total)]
record("D04-math-1-v02", hits, f"a={a}, A={profitA}, B={profitB}, total={total}")

# ---------------- 1-v03: markup 25% on cost vs profit = 25% of price
pa = F(120) * F(5, 4)
pb = F(120) / (1 - F(1, 4))
d = pb - pa
opts = qs["D04-math-1-v03"]["options"]
def parse3(v):
    if "相同" in v: return F(0)
    n = num(v)
    return n if v.startswith("乙") else -n   # positive => 乙 higher
hits = [k for k, v in opts.items() if parse3(v) == d]
record("D04-math-1-v03", hits, f"甲={pa}, 乙={pb}, 乙-甲={d}")

# ---------------- 1-v04: market M, member 0.8M, first order 0.9 of that, paid 3600
M = F(3600) / (F(8, 10) * F(9, 10))
record("D04-math-1-v04", match_numeric("D04-math-1-v04", M - 3600), f"M={M}, saved={M-3600}")

# ---------------- 1-v05: trade-in subsidy with caps
def pay(label, disc, rate, cap):
    final = F(label) * disc
    return final - min(final * rate, cap)
payA = pay(12500, F(88, 100), F(20, 100), 2000)
payB = pay(13000, F(80, 100), F(15, 100), 1500)
cheaper = "甲" if payA < payB else "乙"
diff = abs(payA - payB)
opts = qs["D04-math-1-v05"]["options"]
hits = [k for k, v in opts.items() if v.startswith(cheaper) and num(v) == diff]
record("D04-math-1-v05", hits, f"甲 pays {payA}, 乙 pays {payB}")

# ---------------- 1-v06: 甲 0.8x-30, 乙 0.9(x-50), promo only if x>=100; threshold where 甲 cheaper
def pA(x): return x * F(8, 10) - 30 if x >= 100 else x
def pB(x): return (x - 50) * F(9, 10) if x >= 100 else x
# scan in 0.01 steps from 0 to 1000 to find sup of set where NOT cheaper, inf where cheaper
cheaper_set = [F(i, 100) for i in range(0, 100001) if pA(F(i, 100)) < pB(F(i, 100))]
lo = min(cheaper_set)
# check set is an up-ray (contiguous to the end)
contig = all(pA(F(i, 100)) < pB(F(i, 100)) for i in range(int(lo * 100), 100001))
thresh = lo - F(1, 100)   # last point not cheaper
record("D04-math-1-v06", match_numeric("D04-math-1-v06", thresh), f"甲 cheaper for x>{thresh} (contiguous={contig})")

# ---------------- 1-v07: subsidy 15% capped 500 if price<=6000, else none; pay <= 5600; max price
def pay7(p):
    return p - min(p * F(15, 100), 500) if p <= 6000 else p
feasible = [F(i) for i in range(0, 20001) if pay7(F(i)) <= 5600]
mx = max(feasible)
# also check finer grid just above 6000 to be safe
assert all(pay7(F(6000) + F(k, 100)) > 5600 for k in range(1, 100000))
record("D04-math-1-v07", match_numeric("D04-math-1-v07", mx), f"max price={mx}, pay={pay7(mx)}")

# ---------------- 1-v08: A = B + 4, B = 0.8A; budget/B - budget/A = 15; equal counts
A_ = sp.symbols("A_", positive=True)
Aval = sp.solve(sp.Eq(A_ - sp.Rational(4, 5) * A_, 4), A_)[0]
Bval = sp.Rational(4, 5) * Aval
Fb = sp.symbols("Fb", positive=True)
budget = sp.solve(sp.Eq(Fb / Bval - Fb / Aval, 15), Fb)[0]
n = int(budget // (Aval + Bval))
record("D04-math-1-v08", match_numeric("D04-math-1-v08", n), f"A={Aval}, B={Bval}, budget={budget}, n={n}")

# ---------------- 1-v09: profit rate (on cost) 26% -> 40%, price fixed; cost decrease %
S = F(1)
c1, c2 = S / F(126, 100), S / F(140, 100)
dec = (c1 - c2) / c1 * 100
record("D04-math-1-v09", match_numeric("D04-math-1-v09", dec, tol=F(1, 10)), f"cost decrease={float(dec):.4f}%")

# ---------------- 1-v10: price 1.5c, m units; cost +20%; profit >= 90% of last month
c = F(1); price = F(3, 2)
need = F(9, 10) * (price - c) / (price - c * F(6, 5))   # multiples of m
record("D04-math-1-v10", match_numeric("D04-math-1-v10", need, tol=F(1, 100)), f"n >= {need} m")

# ---------------- 1-v11: cost -8%, price fixed, profit rate +10 points; original rate
r = sp.symbols("r")
rs = sp.solve(sp.Eq((1 + r) / sp.Rational(92, 100) - 1, r + sp.Rational(1, 10)), r)[0]
record("D04-math-1-v11", match_numeric("D04-math-1-v11", F(str(rs)) * 100), f"r={rs}")

# ---------------- 1-v12: selenium rice
C = F(1); rev_n = C * F(3, 2)           # normal revenue: profit = 0.5 C
prof_n = rev_n - C
rev_s = rev_n * F(9, 10) * F(3, 2)
prof_s = rev_s - C * F(6, 5)
inc = (prof_s / prof_n - 1) * 100
record("D04-math-1-v12", match_numeric("D04-math-1-v12", inc), f"normal profit={prof_n}, Se profit={prof_s}, inc={inc}%")

# ---------------- 1-v13: revenue +20%, expense +12%, profit +50%, last profit 800
R, E = sp.symbols("R E")
s13 = sp.solve([sp.Eq(R - E, 800), sp.Eq(sp.Rational(6, 5) * R - sp.Rational(28, 25) * E, 1200)], [R, E])
rev_this = sp.Rational(6, 5) * s13[R]
record("D04-math-1-v13", match_numeric("D04-math-1-v13", F(str(rev_this))), f"last R={s13[R]}, E={s13[E]}, this R={rev_this}")

# ---------------- 1-v14: material 60% (+20%), processing 40% (-25%), price fixed, profit -10%
Pp = sp.symbols("Pp")
cost0 = 100; cost1 = 60 * sp.Rational(6, 5) + 40 * sp.Rational(3, 4)
Pv = sp.solve(sp.Eq(Pp - cost1, sp.Rational(9, 10) * (Pp - cost0)), Pp)[0]
rate = (Pv - cost0) / cost0 * 100
record("D04-math-1-v14", match_numeric("D04-math-1-v14", F(str(rate))), f"new cost={cost1}, price={Pv}, rate={rate}%")

# ---------------- 2-v01: group-buy price
before = 600 * (50 - 30)
retail = 600 - 600 * F(1, 3)
group = 2 * retail
g = 30 + (before - retail * 20) / group
record("D04-math-2-v01", match_numeric("D04-math-2-v01", g), f"retail={retail}, group={group}, g>={g}")

# ---------------- 2-v02: kumquats, 3600 for 150, +50% price, rest at 80%, profit = 88% of full
unit = F(3600, 150); pr = unit * F(3, 2); dpr = pr * F(8, 10)
full = 150 * (pr - unit)
xs = [x for x in range(0, 151) if x * (pr - unit) + (150 - x) * (dpr - unit) == full * F(88, 100)]
record("D04-math-2-v02", match_numeric("D04-math-2-v02", F(xs[0] * 100, 150)) if len(xs) == 1 else [], f"x={xs} pots at full price")

# ---------------- 2-v03: oranges cost 6, price 10, 60% full, rest discounted, profit rate >= 30%
# discount factor d (in 'zhe' units /10); scan 0.1-zhe steps
ok_d = [F(z, 10) for z in range(0, 101) if (F(6, 10) * 10 + F(4, 10) * 10 * F(z, 100)) >= 6 * F(13, 10)]
dmin = min(ok_d)   # in zhe
record("D04-math-2-v03", match_numeric("D04-math-2-v03", dmin), f"min discount = {dmin} zhe")

# ---------------- 2-v04: price 50+x (x>0), qty 300-10x, cost 40; max profit
best = max(((50 + F(x, 100) - 40) * (300 - 10 * F(x, 100)), F(x, 100)) for x in range(1, 3001))
record("D04-math-2-v04", match_numeric("D04-math-2-v04", best[0]), f"max profit={best[0]} at +{best[1]}")

# ---------------- 2-v05: homestay 40 rooms, 200 full, +20 -> 2 more empty, cost 40 per occupied
best5 = max(((200 + 20 * k - 40) * (40 - 2 * k), 200 + 20 * k) for k in range(0, 21))
# also continuous check
bestc = max(((200 + 20 * F(k, 100) - 40) * (40 - 2 * F(k, 100)), 200 + 20 * F(k, 100)) for k in range(0, 2001))
record("D04-math-2-v05", match_numeric("D04-math-2-v05", best5[1]), f"best price={best5[1]} profit={best5[0]}; continuous best={bestc[1]}")

# ---------------- 2-v06: rice cooker, cost 60, price 100 sells 80, each -2 -> +15, steps of 2
tab = [((100 - 2 * k - 60) * (80 + 15 * k), 100 - 2 * k) for k in range(0, 21)]
best6 = max(tab)
second = sorted(tab, reverse=True)[1]
record("D04-math-2-v06", match_numeric("D04-math-2-v06", best6[1]), f"best price={best6[1]} profit={best6[0]}; runner-up={second}")

# ---------------- 2-v07: parking fee
def fee(minutes):
    if minutes <= 15: return 0
    if minutes <= 60: return 6
    return 6 + 3 * math.ceil((minutes - 60) / 30)
zhang = fee(160)
li_minutes = [m for m in range(0, 24 * 60 + 1) if fee(m) == zhang + 6]
mxm = max(li_minutes)
opts = qs["D04-math-2-v07"]["options"]
def to_min(v):
    h = re.search(r"(\d+)小时", v); mm = re.search(r"(\d+)分钟", v)
    return (int(h.group(1)) * 60 if h else 0) + (int(mm.group(1)) if mm else 0)
hits = [k for k, v in opts.items() if to_min(v) == mxm]
record("D04-math-2-v07", hits, f"张 fee={zhang}, 李 fee range minutes={min(li_minutes)}..{mxm}")

# ---------------- 2-v08: tiered electricity, total 453, Aug = Jul + 120
def elec(u):
    u = F(u)
    t1 = min(u, 200) * F(6, 10)
    t2 = max(min(u, 400) - 200, 0) * F(65, 100)
    t3 = max(u - 400, 0) * F(9, 10)
    return t1 + t2 + t3
sols8 = [F(x, 10) for x in range(0, 10001) if elec(F(x, 10)) + elec(F(x, 10) + 120) == 453]
record("D04-math-2-v08", match_numeric("D04-math-2-v08", sols8[0]) if len(sols8) == 1 else [], f"July={sols8}")

# ---------------- 2-v09: ride-hailing two routes
def ride(km, speed, toll):
    dist = 10 + max(km - 3, 0) * 2
    minutes = F(km, speed) * 60
    return dist + minutes * F(1, 2) + toll
hw = ride(30, 60, 10); city = ride(24, 24, 0)
opts = qs["D04-math-2-v09"]["options"]
cheaper = "市区" if city < hw else "高速"
hits = [k for k, v in opts.items() if cheaper in v.split("更省")[0] and num(v) == abs(hw - city)]
record("D04-math-2-v09", hits, f"highway={hw}, city={city}")

# ---------------- 2-v10: membership 190 + 0.95x vs x
x = sp.symbols("x")
be = sp.solve(sp.Eq(190 + sp.Rational(95, 100) * x, x), x)[0]
record("D04-math-2-v10", match_numeric("D04-math-2-v10", F(str(be))), f"break-even={be}")

# ---------------- 2-v11: fixed 60000, var 30, price 50 profit 40000; price 46
Q0 = F(60000 + 40000, 50 - 30)
Q1 = F(60000 + 40000, 46 - 30)
incp = (Q1 / Q0 - 1) * 100
record("D04-math-2-v11", match_numeric("D04-math-2-v11", incp), f"Q0={Q0}, Q1={Q1}, +{incp}%")

# ---------------- 2-v12: lychee 200 jin at 12, 10% loss, profit rate 35%
p12 = F(200 * 12) * F(135, 100) / (200 * F(9, 10))
record("D04-math-2-v12", match_numeric("D04-math-2-v12", p12), f"price={p12}")

# ---------------- 2-v13: veg 100 jin/day, 6 days sold out, 4 days equal leftover r, total 4520
rs13 = [rr for rr in range(0, 101) if 6 * (100 * 10 - 500) + 4 * ((100 - rr) * 10 + rr * 2 - 500) == 4520]
record("D04-math-2-v13", match_numeric("D04-math-2-v13", rs13[0]) if len(rs13) == 1 else [], f"leftover={rs13}")

print()
print("SUMMARY:", json.dumps({k: v[0] for k, v in results.items()}, ensure_ascii=False))
bad = [k for k, v in results.items() if not isinstance(v[0], str)]
print("questions without exactly one matching option:", bad)
