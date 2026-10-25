# Independent blind solver for revh2_C (D04 v15-v19). Computes from stem data only.
from fractions import Fraction as F

def hdr(s):
    print("\n" + "=" * 70 + "\n" + s + "\n" + "=" * 70)

# ---------------------------------------------------------------- v15
hdr("v15  special order, capacity 10000, now 8000 @60, full cost 45 (var 30)")
CAP, Q0, P0, FULL, VAR = 10000, 8000, 60, 45, 30
FIXED = (FULL - VAR) * Q0                       # fixed cost total, unchanged
ORDER = 3000
displaced = max(0, Q0 + ORDER - CAP)            # regular sales that must be cut
def profit(p_order, take):
    if not take:
        return Q0 * P0 - Q0 * VAR - FIXED
    q_reg = Q0 - displaced
    return q_reg * P0 + ORDER * p_order - (q_reg + ORDER) * VAR - FIXED
base = profit(0, False)
# exact break-even by scanning in 0.01 steps (and a closed form)
pmin = None
for cents in range(0, 20001):
    p = F(cents, 100)
    if profit(p, True) >= base:
        pmin = p
        break
print("fixed total =", FIXED, " displaced =", displaced, " base profit =", base)
print("min order price =", pmin)
opts = {"A": 30, "B": 35, "C": 40, "D": 45}
print("options equal to min price:", [k for k, v in opts.items() if v == pmin])
# error paths
print("  err: ignore displaced sales  ->", VAR)
print("  err: displaced valued at full-cost margin (60-45) ->", VAR + F(displaced * (P0 - FULL), ORDER))
print("  err: use full cost 45 as floor ->", FULL)
print("  err: displaced = 3000 (whole order) ->", VAR + F(ORDER * (P0 - VAR), ORDER))
print("  err: full cost + displaced contribution ->", FULL + F(displaced * (P0 - VAR), ORDER))

# ---------------------------------------------------------------- v16
hdr("v16  bayberry: cost 10.53, 2-day compounding loss r, 80%@18, 20%@12.5, margin 30%")
c = F("10.53"); m = F(3, 10); p1 = 18; p2 = F("12.5"); a = F(4, 5)
avg = a * p1 + (1 - a) * p2
need = c * (1 + m) / avg                       # (1-r)^2
print("avg price =", avg, "= ", float(avg), "; (1-r)^2 =", need, "=", float(need))
opts = {"A": F("2.5"), "B": F("9.5"), "C": F(10), "D": F(19)}
for k, v in opts.items():
    r = v / 100
    rev = (1 - r) ** 2 * avg
    margin = rev / c - 1
    print(f"  {k} r={float(v)}%  margin={float(margin)*100:.4f}%  exact30={margin == m}")
# error paths
import math
print("  err: linear loss 1-2r=0.81 ->", (1 - need) / 2 * 100, "%")
print("  err: report total loss 1-(1-r)^2 ->", (1 - need) * 100, "%")
x = c * (1 + m) / (a * p1)
print("  err: drop clearance revenue (only 80%*18): (1-r)^2 =", x, " r =", (1 - math.sqrt(x)) * 100, "%")
x = c * (1 + m) / p1
print("  err: all sold at 18: r =", (1 - math.sqrt(x)) * 100, "%")
x = c * (1 + m) / ((p1 + p2) / 2)
print("  err: simple mean of prices: r =", (1 - math.sqrt(x)) * 100, "%")
x = c / avg
print("  err: forget margin: r =", (1 - math.sqrt(x)) * 100, "%")
x = c / (1 - m) / avg
print("  err: margin on revenue: r =", (1 - math.sqrt(x)) * 100, "%")
print("  shortcut check: 16.9/1.3 =", avg / (1 + m), "; 10.53/13 =", c / (avg / (1 + m)))

# ---------------------------------------------------------------- v17
hdr("v17  flowers: deliver 960 intact @30, buy 12; normal freight 1 loss 20%; cold loss 4%")
N, P, BUY = 960, 30, 12
fN, lN, lC = 1, F(1, 5), F(1, 25)
shipN = N / (1 - lN); shipC = N / (1 - lC)
profN = N * P - shipN * (BUY + fN)
# cold profit = N*P - shipC*(BUY+f) >= profN  ->  f <= ...
fmax = (N * P - profN) / shipC - BUY
print("ship normal =", shipN, " ship cold =", shipC, " profit normal =", profN, " max cold freight =", fmax, float(fmax))
opts = {"A": F("1.2"), "B": F("2.4"), "C": F(3), "D": F("3.6")}
print("options equal to max:", [k for k, v in opts.items() if v == fmax])
# error paths
sN = N * (1 + lN); sC = N * (1 + lC)
print("  err: ship = 960*(1+loss):", sN, sC, " fmax =", float(sN * (BUY + fN) / sC - BUY))
print("  err: only freight compared (ignore purchase saving):", float(shipN * fN / shipC))
print("  err: purchase saving only, forget normal freight:", float((shipN - shipC) * BUY / shipC))
print("  err: per-unit freight ratio 1*0.96/0.8 ... ->", float(fN * (1 - lC) / (1 - lN)))
print("  err: per delivered bundle, cold freight per delivered:", float((BUY + fN) / (1 - lN) - BUY / (1 - lC)))

# ---------------------------------------------------------------- v18
hdr("v18  mooncakes: 1500 boxes @60; buyout 24 (<=300 unsold returnable @12); consign 30 full return")
TOT, PR = 1500, 60
def buyout(x):
    u = TOT - x
    return PR * x - 24 * TOT + 12 * min(300, u)
def consign(x):
    return (PR - 30) * x
ok = [x for x in range(TOT + 1) if buyout(x) >= consign(x)]
xmin = min(ok)
print("min sold with buyout>=consign:", xmin, " holds for all x>=xmin:", all(buyout(x) >= consign(x) for x in range(xmin, TOT + 1)))
print("profits at xmin:", buyout(xmin), consign(xmin))
opts = {"A": 420, "B": 540, "C": 1000, "D": 1080}
print("options equal to xmin:", [k for k, v in opts.items() if v == xmin])
for k, v in opts.items():
    print(f"  {k} x={v}: buyout={buyout(v)} consign={consign(v)} ok={buyout(v) >= consign(v)}")
# error paths
print("  err: ignore 300 cap (all unsold back @12): x >=", F(24 * TOT - 12 * TOT, PR - 12 - 30))
print("  err: buyout break-even with 300 returned: x >=", F(24 * TOT - 12 * 300, PR))
print("  err: report unsold count at threshold:", TOT - xmin)
print("  err: no return at all: x >=", F(24 * TOT, PR - 30))

# ---------------------------------------------------------------- v19
hdr("v19  milk newsvendor: cost 8, price 12, salvage 2; demand 80x3,100x6,120x7,140x4")
cost, price, salv = 8, 12, 2
dem = {80: 3, 100: 6, 120: 7, 140: 4}
def tot(q):
    s = 0
    for d, n in dem.items():
        sold = min(d, q)
        s += n * (price * sold + salv * (q - sold) - cost * q)
    return s
res = {q: tot(q) for q in (80, 100, 120, 140)}
print("total profit by order qty:", res)
best = max(res, key=res.get)
print("best:", best, " unique:", list(res.values()).count(res[best]) == 1)
opts = {"A": 120, "B": 140, "C": 80, "D": 100}
print("option letter of best:", [k for k, v in opts.items() if v == best])
mean = F(sum(d * n for d, n in dem.items()), sum(dem.values()))
print("  mean demand =", mean, float(mean), "; mode =", max(dem, key=dem.get))
cu, co = price - cost, cost - salv
print("  critical ratio Cu/(Cu+Co) =", F(cu, cu + co))
cum = 0
for d in sorted(dem):
    cum += dem[d]
    print(f"   F({d}) = {cum}/20 = {cum/20}")
