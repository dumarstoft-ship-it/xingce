# Blind solve of w2_r1 questions (written BEFORE opening the key).
# Every answer is computed from the stem data by brute force / enumeration.
from fractions import Fraction as F
from itertools import permutations, product
import heapq

def pick(options, value):
    hits = [k for k, v in options.items() if abs(float(v) - float(value)) < 1e-9]
    return hits

print("=" * 70)
# ---------------------------------------------------------------- Q1 D09
# stock: 甲30 乙16 丙9 丁6 戊2 ; need >=2 varieties with >=5 bags.
stock = [30, 16, 9, 6, 2]
best_bad = 0
for c in product(*[range(s + 1) for s in stock]):
    if sum(1 for x in c if x >= 5) < 2:
        best_bad = max(best_bad, sum(c))
ans1 = best_bad + 1
print("Q1 D09-v01: worst 'bad' draw =", best_bad, "-> answer", ans1,
      pick({"A": 20, "B": 44, "C": 45, "D": 47}, ans1))
# error paths
print("   err: cap everyone at 4 then +1 +1          =", sum(min(s, 4) for s in stock) + 2)
print("   err: forgot +1                             =", best_bad)
print("   err: 戊 treated as 4 (30+4*4) +1            =", 30 + 4 * 4 + 1)
print("   err: cap at 5 (misread) +1                 =", 30 + sum(min(s, 5) for s in stock[1:]) + 1)

print("=" * 70)
# ---------------------------------------------------------------- Q2 D10-v01
# x 甲 acres, y 乙 acres. land x+y<=60, water 300x+100y<=15000, labor 10x+20y<=1000
cons = [(1, 1, 60), (300, 100, 15000), (10, 20, 1000), (-1, 0, 0), (0, -1, 0)]
def feasible(x, y):
    return all(a * x + b * y <= c for a, b, c in cons)
verts = []
for (a1, b1, c1), (a2, b2, c2) in [(p, q) for i, p in enumerate(cons) for q in cons[i + 1:]]:
    det = a1 * b2 - a2 * b1
    if det == 0:
        continue
    x = F(c1 * b2 - c2 * b1, det)
    y = F(a1 * c2 - a2 * c1, det)
    verts.append(((x, y), feasible(x, y)))
best = max((2000 * x + 3000 * y, (x, y)) for (x, y), ok in verts if ok)
print("Q2 D10-v01: optimum profit", float(best[0]) / 1e4, "万 at", best[1])
# integer-grid cross-check
gbest = max((2000 * x + 3000 * y, x, y) for x in range(0, 101) for y in range(0, 101) if feasible(x, y))
print("   integer grid best:", gbest[0] / 1e4, "万 at", gbest[1:])
print("   answer letter:", pick({"A": 13.5, "B": 15, "C": 16, "D": 17}, float(best[0]) / 1e4))
for (x, y), ok in verts:
    if x >= 0 and y >= 0:
        print(f"   vertex ({float(x):.2f},{float(y):.2f}) feasible={ok} profit={float(2000*x+3000*y)/1e4}万")

print("=" * 70)
# ---------------------------------------------------------------- Q3 D10-v02
# total work 24 units; 甲 2 units/day 5万/day; 乙 1 unit/day 2万/day; budget 52万.
W = 24
best3 = None
step = F(1, 200)
a = F(0)
while a <= W:
    tA, tB = a / 2, (W - a) / 1
    cost = 5 * tA + 2 * tB
    if cost <= 52:
        t = max(tA, tB)
        if best3 is None or t < best3[0]:
            best3 = (t, a, cost)
    a += step
print("Q3 D10-v02: min days", best3[0], "with 甲 doing", best3[1], "of 24 units, cost", best3[2])
print("   answer letter:", pick({"A": 8, "B": 16, "C": 20, "D": 24}, best3[0]))
print("   err: no budget, both together =", F(1) / (F(1, 12) + F(1, 24)))
print("   err: sequential (甲 4d then 乙 16d) =", F(8, 2) + 16)
print("   err: 乙 alone =", 24)

print("=" * 70)
# ---------------------------------------------------------------- Q4 D10-v03
p = {"甲": 5, "乙": 2, "丙": 6, "丁": 3}
w = {"甲": 2, "乙": 1, "丙": 4, "丁": 3}
def loss(order):
    t = tot = 0
    for m in order:
        t += p[m]
        tot += t * w[m]
    return tot
allv = sorted((loss(o), o) for o in permutations(p))
print("Q4 D10-v03: min loss", allv[0][0], "order", "".join(allv[0][1]),
      "| ties:", [("".join(o)) for v, o in allv if v == allv[0][0]])
print("   answer letter:", pick({"A": 43, "B": 88, "C": 95, "D": 101}, allv[0][0]))
print("   max over orders:", allv[-1][0], "".join(allv[-1][1]))
print("   SPT order:", loss(sorted(p, key=lambda m: p[m])))
print("   heaviest-loss-rate first:", loss(sorted(p, key=lambda m: -w[m])))
print("   waiting-only (forgot own repair time):", allv[0][0] - sum(p[m] * w[m] for m in p))
print("   sum p*w (constant part):", sum(p[m] * w[m] for m in p))
print("   all distinct totals:", sorted(set(v for v, o in allv)))

print("=" * 70)
# ---------------------------------------------------------------- Q5 D10-v04
edges = [("A", "B", 2), ("B", "C", 4), ("C", "D", 5), ("C", "E", 5), ("E", "F", 3)]
tons = {"A": 6, "B": 4, "C": 3, "D": 7, "E": 8, "F": 14}
g = {v: [] for v in tons}
for u, v, d in edges:
    g[u].append((v, d)); g[v].append((u, d))
def dij(s):
    dist = {s: 0}; pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, wgt in g[u]:
            if d + wgt < dist.get(v, 10 ** 9):
                dist[v] = d + wgt; heapq.heappush(pq, (d + wgt, v))
    return dist
cost = {s: 2 * sum(tons[v] * dij(s)[v] for v in tons) for s in tons}
print("Q5 D10-v04: cost at each site (元):", cost)
m5 = min(cost.values())
print("   min:", m5, "at", [s for s in cost if cost[s] == m5])
print("   answer letter:", pick({"A": 458, "B": 478, "C": 542, "D": 654}, m5))
# continuous check: any point on an edge (should not beat the vertex optimum on a tree)
bestpt = m5
for u, v, d in edges:
    du, dv = dij(u), dij(v)
    for k in range(0, 101):
        x = F(d * k, 100)  # distance from u along edge
        c = 2 * sum(tons[t] * min(du[t] + x, dv[t] + (d - x)) for t in tons)
        bestpt = min(bestpt, c)
print("   best over all points on roads:", bestpt)
# side weights at C and E
print("   total tons", sum(tons.values()), "half", sum(tons.values()) / 2)

print("=" * 70)
# ---------------------------------------------------------------- Q6 D12-v01
# n甲=400 @40; 乙@49 丙@46; total 2000 @48; 丁 has the most orders (strictly).
ranks = {}
ranks_nocond = {}
xs = []
for nB in range(1, 1600):
    for nC in range(1, 1600 - nB):
        nD = 1600 - nB - nC
        if nD <= 0:
            continue
        x = F(2000 * 48 - 400 * 40 - 49 * nB - 46 * nC, nD)
        if x <= 0:
            continue
        others = [40, 49, 46]
        rank = 1 + sum(1 for o in others if o > x)
        tie = any(o == x for o in others)
        key = (rank, tie)
        ranks_nocond[key] = ranks_nocond.get(key, 0) + 1
        if nD > max(400, nB, nC):
            ranks[key] = ranks.get(key, 0) + 1
            xs.append(x)
print("Q6 D12-v01: possible (rank, tie) with condition:", ranks)
print("   without 'most orders' condition:", ranks_nocond)
print("   丁 avg range under condition: [%.4f, %.4f]" % (float(min(xs)), float(max(xs))))
print("   avg of 乙丙丁 combined:", F(2000 * 48 - 400 * 40, 1600))
