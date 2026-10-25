"""Scratch verification for D04 hardening decisions (skeleton numbers only)."""
from fractions import Fraction as F
import math

def hdr(s):
    print("\n==", s)

# ---------------- kept variants (sanity) ----------------
hdr("keep v07 phone subsidy cliff")
def pay(p):
    if p <= 6000:
        return p - min(0.15 * p, 500)
    return p
best = max(p for p in range(1, 8001) if pay(p) <= 5600)
print("max price", best, "pay", pay(best), "| pay(6100)=", pay(6100))

hdr("keep v13 income/expense growth")
# 1.2(E+P)=1.12E+1.5P
print("E/P =", F(3, 10) / F(8, 100))

hdr("keep v04-2 cap")
print(max(((20 + x) * (180 - 3 * x), x) for x in range(0, 11)))
hdr("keep v05-2 minsu")
print(max(((160 + 20 * x) * (40 - 2 * x), 200 + 20 * x) for x in range(0, 21)))
hdr("keep v06-2 step 2")
print(sorted((((40 - 2 * n) * (80 + 15 * n)), 100 - 2 * n) for n in range(0, 21))[-3:])
hdr("keep v08-2 tiered electricity two months")
def elec(u):
    t = 0.6 * min(u, 200)
    if u > 200:
        t += 0.65 * (min(u, 400) - 200)
    if u > 400:
        t += 0.9 * (u - 400)
    return t
print([u for u in range(0, 600) if abs(elec(u) + elec(u + 120) - 453) < 1e-6])

# ---------------- added reals (independent re-solve) ----------------
hdr("2021GK-75 coupons")
x, y = 8.8, 6.8
assert abs(x + y - 15.6) < 1e-9 and abs(10 * x + 30 * y - 219 / 0.75) < 1e-9
print("min pay (wan)", x * 40 + y * 70)

hdr("2024SC-47 tiered discount, max saving")
def rate(o):
    return 0.6 if o >= 988 else 0.7 if o >= 688 else 0.8 if o >= 488 else 1.0
def origs(paid):
    return [o for o in (paid, paid / 0.8, paid / 0.7, paid / 0.6) if abs(o * rate(o) - paid) < 1e-6]
sav = [(400 + 630 - (a + b) * rate(a + b), a, b) for a in origs(400) for b in origs(630)]
print(sorted(sav))

hdr("2022SD-40 bulk vs single")
def disc(t):
    return 0.10 if t > 1000 else 0.05 if t > 500 else 0.02 if t > 100 else 0
sol = [p for p in [x / 10 for x in range(10, 5000)] if abs(10 * (p * (1 - disc(p)) + 6) - (10 * p * (1 - disc(10 * p)) + 6) - 174) < 1e-6]
print("unit price", sol, "single cost", [p * (1 - disc(p)) + 6 for p in sol])

hdr("2020SC0725-50 packs")
def mincost(x):
    best = 1e9
    for t in range(0, x // 10 + 3):
        for h in range(0, x // 3 + 3):
            rest = max(0, x - 10 * t - 3 * h)
            best = min(best, 15 * t + 5 * h + 1.7 * rest)
    return round(best, 2)
print([x for x in range(1, 40) if abs(mincost(x) - (1.7 * x - 2.3)) < 1e-6])

hdr("2021JSA-62 buy-gift")
for b in (24, 25, 26, 27):
    a = 56 - b
    print(b, 18 * (a - a // 3) + 12 * (b - b // 4))

hdr("2021ZJA-70")
# 1.5R-1.35C = 2(R-C) -> R = 1.3C
C = F(10); R = F(13)
print("new profit share", (2 * (R - C)) / (F(3, 2) * R))

hdr("2021SD-43")
price = [1, .9, .8, .7, .6, .5]; vol = [1, 2, 4, 8, 16, 4]
rev = sum(p * v for p, v in zip(price, vol)); cost = 0.6 * sum(vol)
print("profit/cost", (rev - cost) / cost)

hdr("2023SD-44")
# unit labour 3k, non 1k; after 1.5k,0.9k; output 2Q; 2Q(1.5k-0.9k)=3.6 -> kQ=3
kQ = 3.6 / 1.2
print("days", 3456 / (2 * kQ * (4 - 2.4)))

hdr("2022GK-72")
print("energy/other", F(4, 14), float(F(4, 14)))

hdr("2025SD-58")
print((90000 / 30 + 106800 / 40) / (800 + 16800 / 56))

hdr("2023GK-61")
# price 10 shares: 2(8-c)=10-c -> c=6 ; 3*(10-c-d)=4 -> d=8/3 share =120
print("price", 10 * 120 / F(8, 3))

hdr("2024JSA-53")
N = 7410 / 0.19
print("total", N / 100, "discount part", (30 * N / 100 - 7410) / 39)

hdr("2022GK-75")
c = 500; P = 750
print(5 * ((P - 30) * 0.8 - c) - (P - c), 15000 / P, 15000 / 24, [(P - 50) * .8, P * .9 - 50, P - 150, P * .85])

hdr("2025GK-76")
units = sum(40 + 10 * d for d in range(1, 16))
print(units, "cost/price", F(8 * units - 800 * 10, units - 800) / 10)

hdr("2024SZ-57")
for a in range(1, 20):
    for m in range(0, 30):
        if abs(30 * a + 1.5 * (30 - m) - 247.5) < 1e-9:
            for h in range(30, 40):
                if abs(40 * a + 1.5 * (h - m) - (40 - h) - 315) < 1e-9:
                    print("a", a, "base", m, "health", h, "->", a - 1)

hdr("2021HB-72")
for name, v, f, t, pk in [("jia", 60, 6, 4, 1500), ("yi", 50, 8, 2, 1000), ("bing", 100, 10, 3, 700), ("ding", 75, 7, 5, 1200)]:
    print(name, "slope", f + 300 / v, "const", pk + 300 * t)

# ---------------- NEW VARIANT SKELETONS ----------------
hdr("NV-B three bases (commission on deal price, discount on list, margin on cost)")
C = 200 + 200 * 0.10 + 35
need = 1.2 * C
print("cost", C, "correct P", need / (0.9 * 0.85), "| fee on list", need / (0.9 - 0.15),
      "| no fee", need / 0.9, "| fee as markup", C * 1.2 * 1.15 / 0.9, "| margin on price", C / (0.765 - 0.18))

hdr("NV01 loss-making segment, growth mix with negative weight")
# a=manufacturing profit, b=e-commerce loss: 1.1a-0.6b = 1.5(a-b)
r = F(4, 10) / F(9, 10)
print("b/a", r, float(r), "| 2025 ratio", float(F(6, 10) * r / F(11, 10)), "| sign error b/a", F(4, 10) / F(1, 10))

hdr("NV02 national + local subsidy, caps, reverse")
def pay2(P):
    g = min(0.15 * P, 2000)
    l = min(0.10 * (P - g), 800)
    return P - g - l
sol = [P for P in range(1000, 30001) if abs(pay2(P) - 12200) < 1e-6]
print("P", sol, "| naive", 12200 / 0.765, "| only national capped", 12200 / 0.9 + 2000, "| drop local", 12200 + 2000)

hdr("NV03 price +10%, volume -20%, profit +20% -> original margin")
# unit profit ratio new/old = 1.2/0.8 = 3/2 ; delta = 0.1*price
old, new = 2, 3
price = (new - old) / 0.1
cost = price - old
print("price", price, "cost", cost, "orig margin", old / cost, "new margin", new / cost, "margin on price", old / price)

hdr("NV04 weekday/weekend weighted, weekend revenue invariant")
# weekday x3 at 0.5 ; weekend x1.25 at 0.8 ; total +20% ; find weekend/weekday visitors k
k = F(15, 10) / F(4, 10)
print("k", k, float(k), "| per-day (no day weights):", F(3, 10) / F(2, 10))
assert 5 * 3 * F(1, 2) + 2 * k * F(5, 4) * F(4, 5) == F(6, 5) * (5 + 2 * k)

hdr("NV-pp cost +20%, price +10%, margin -10 points")
for r0 in (0.10, 0.20, 0.25, 0.30):
    P = 100 * (1 + r0)
    print(r0, "new margin", round(1.1 * P / 120 - 1, 4), "drop pts", round((r0 - (1.1 * P / 120 - 1)) * 100, 2))

hdr("NV05 fixed-cost dilution two steps")
# unit = f+v ; 1.25Q -> 0.8f+v = 0.9(f+v) -> f=v
f = v = F(1, 2)
print("share f", f, "| at 2Q unit cost", f / 2 + v, "drop", 1 - (f / 2 + v), "| linear extrap 40%, naive 10/25=40%")

hdr("NV07 EOQ")
D, S, H = 3600, 200, 4
tot = lambda q: S * D / q + H * q / 2
print(min((tot(q), q) for q in range(50, 3601, 50)), [(q, tot(q)) for q in (300, 600, 900, 1200)])

hdr("NV09 parking, infer tier price and boundary by difference")
b = (34 - 19) / (8 - 5)
a = (5 * b - 19) / (b - 3)
fee = lambda t: 3 * min(math.ceil(t), a) + b * max(0, math.ceil(t) - a)
print("b", b, "a", a, "max hours for 24:", max(t / 60 for t in range(1, 12 * 60) if fee(t / 60) <= 24 and fee(t / 60) == 24))

hdr("NV10 tax difference straddles a bracket")
def tax(x):
    t = 0.03 * min(x, 3000)
    if x > 3000: t += 0.10 * (min(x, 12000) - 3000)
    if x > 12000: t += 0.20 * (min(x, 25000) - 12000)
    return t
print([x for x in range(6000, 25001, 100) if abs(tax(x) - tax(x - 6000) - 840) < 1e-6])

hdr("NV11 metro cumulative tiers, avg <= 5")
def metro(n):
    s = 6 * n
    return min(s, 100) + 0.8 * max(0, min(s, 150) - 100) + 0.5 * max(0, s - 150)
print("first n avg<=5:", min(n for n in range(1, 100) if metro(n) / n <= 5), [(n, round(metro(n) / n, 3)) for n in (25, 26, 32, 33)])

hdr("NV13 three phone plans")
A = lambda t: 0.2 * t
B = lambda t: 30 + 0.15 * max(0, t - 200)
Cc = lambda t: 60 + 0.1 * max(0, t - 500)
best_B = [t for t in range(0, 801) if B(t) < A(t) and B(t) < Cc(t)]
print("B cheapest for", best_B[0], "...", best_B[-1])

hdr("NV14 piecewise variable cost, target profit")
def profit(q):
    return 50 * q - 200000 - 30 * min(q, 5000) - 26 * max(0, q - 5000)
print("min q", min(q for q in range(0, 30000) if profit(q) >= 140000), "| all-30", 340000 / 20, "| all-26", 340000 / 24)

hdr("NV15 target cost-profit-rate break-even")
F0, vc, p = 70000, 30, 50
print("q", min(q for q in range(1, 20000) if (p - vc) * q - F0 >= 0.2 * (F0 + vc * q)),
      "| margin on revenue", min(q for q in range(1, 20000) if (p - vc) * q - F0 >= 0.2 * p * q),
      "| base=variable only", min(q for q in range(1, 20000) if (p - vc) * q - F0 >= 0.2 * vc * q), "| breakeven", F0 / (p - vc))

hdr("NV16 make-or-buy with capacity")
print("max saving", 12 * 6000 - 90000, "naive crossover", 90000 / 12)

hdr("NV17 two-day loss + clearance -> list price")
c0 = 7.29
print("correct", 1.2 * c0 / (0.81 * 0.9), "| loss 20%", 1.2 * c0 / (0.8 * 0.9), "| ignore clearance discount", 1.2 * c0 / 0.81,
      "| ignore loss", 1.2 * c0 / 0.9, "| clearance revenue dropped", 1.2 * c0 / (0.81 * 0.8))

hdr("NV18 buyout vs consignment")
s = F(30, 36)
print("threshold", s, float(s), "| buyout break-even", 30 / 50, "| unit-margin ratio", 14 / 20)

hdr("NV19 newsvendor")
dem = {100: 4, 120: 8, 140: 6, 160: 2}
def tot19(q):
    return sum(n * (10 * min(q, d) + 2 * max(0, q - d) - 4 * q) for d, n in dem.items())
print({q: tot19(q) for q in dem}, "mean demand", sum(d * n for d, n in dem.items()) / 20)

hdr("NV20 cold chain vs normal")
print("threshold price", (1.5 - 0.3) / (0.98 - 0.90), "| loss valued at cost:", (0.98 - 0.90) * 8, "< 1.2")
