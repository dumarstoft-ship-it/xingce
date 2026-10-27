from fractions import Fraction as F
from itertools import permutations, product
import math

res = {}

# 2026GD-39: server profit5 credit-4; terminal profit2 credit+1; x+y<=2000; y-4x>=0; max 5x+2y (integers)
best = max((5*x+2*y, x, y) for x in range(0, 2001) for y in range(0, 2001 - x) if y - 4*x >= 0)
res['2026GD-39'] = best  # expect 5200 -> C

# 2025HB-76: fuel x profit2 credit-2; ev y profit1 credit+3; x+y<=3000; 3y-2x>=0
best = max((2*x+y, x, y) for x in range(0, 3001) for y in range(0, 3001 - x) if 3*y - 2*x >= 0)
res['2025HB-76'] = best  # expect 4800 -> C

# 2019JSA-55
best = max((1000*x+1700*y, x, y) for x in range(0, 101) for y in range(0, 41) if 2*x+5*y <= 200 and 3*x+4*y <= 240)
res['2019JSA-55'] = best  # expect 85900

# 2024HB-67 integer tons and continuous
best = min((F(3,10)*a + F(4,10)*b, a, b) for a in range(0, 10) for b in range(0, 10) if F(5,10)*a+F(7,10)*b >= F(19,10) and F(4,10)*a+F(3,10)*b <= 1)
res['2024HB-67_int'] = (float(best[0]), best[1], best[2])
# continuous LP by vertices
from itertools import combinations
cons = [ (F(-5,10), F(-7,10), F(-19,10)), (F(4,10), F(3,10), F(1)), (F(-1),F(0),F(0)), (F(0),F(-1),F(0)) ]  # a*x+b*y<=c
pts=[]
for (a1,b1,c1),(a2,b2,c2) in combinations(cons,2):
    det=a1*b2-a2*b1
    if det==0: continue
    x=(c1*b2-c2*b1)/det; y=(a1*c2-a2*c1)/det
    if all(a*x+b*y<=c for a,b,c in cons): pts.append((F(3,10)*x+F(4,10)*y,x,y))
res['2024HB-67_cont'] = [(float(p[0]), float(p[1]), float(p[2])) for p in sorted(pts)[:2]]

# 2026CQ-59 / 2026HB-69
ok = [x for x in range(0, 9) if 12*x + 10*(8-x) <= 90 and 240*x + 160*(8-x) >= 1600]
res['2026CQ-59'] = max(ok)

# 2026CQ-68: x m by 甲 (1.5d, 5万), y by 乙 (2d, 4万); sequential; 1.5x+2y<=365; x+y>=200; min 5x+4y (x,y real >=0, check integer too)
best = min((5*x+4*y, x, y) for x in range(0, 244) for y in range(0, 183) if F(3,2)*x+2*y <= 365 and x+y >= 200)
res['2026CQ-68'] = best  # expect 870
# continuous check: on x+y=200 -> 1.5x+2(200-x)<=365 -> x>=70 -> cost 5x+4(200-x)=800+x min at 70 -> 870
# 2023GK-63
best = max(x for x in range(0, 50) for y in range(0, 50) if 16*x + 13*y <= 200 and 9*y > 100)
res['2023GK-63'] = best  # expect 2

# 2026CQ-67: >=160t; 8 A (24t, 350), 4 B (20t, 450), 10 drivers
best = min((350*a+450*b, a, b) for a in range(0, 9) for b in range(0, 5) if a + b <= 10 and 24*a+20*b >= 160)
res['2026CQ-67'] = best
# 2026HB-74 with B=350t typo
best = min((350*a+450*b, a, b) for a in range(0, 9) for b in range(0, 5) if a + b <= 10 and 24*a+350*b >= 160)
res['2026HB-74_typo'] = best

# 2015ZJA-72: 1480t, 1100km; plane 550km/h 20t; train 100km/h 600t
def arrival_times(speed, cap, dist, trips):
    one = dist / speed
    return [ (2*k - 1) * one for k in range(1, trips+1) ]  # k-th trip arrival
bestT = None
for train_trips in range(0, 4):
    rem = max(0, 1480 - 600*train_trips)
    plane_trips = math.ceil(rem / 20)
    t_train = (2*train_trips - 1) * 11 if train_trips else 0
    t_plane = (2*plane_trips - 1) * 2 if plane_trips else 0
    T = max(t_train, t_plane)
    if bestT is None or T < bestT[0]: bestT = (T, train_trips, plane_trips)
res['2015ZJA-72'] = bestT  # expect 54

# 2021JSA-60: apprentice times; master 1.5x efficiency
tasks = [2, 6, 10, 12, 15, 25]
best = None
for mask in range(1 << 6):
    app = sum(t for i, t in enumerate(tasks) if not mask >> i & 1)
    mas = F(sum(t for i, t in enumerate(tasks) if mask >> i & 1)) / F(3, 2)
    T = max(F(app), mas)
    if best is None or T < best: best = T
res['2021JSA-60'] = best

# 2021ZJA-67: emails 2(n-1)
res['2021ZJA-67'] = 2 * (8 - 1)

# 2015ZJA-63
best = max(8*x - 15 for x in range(5, 200) if 20*x + 30*(x-5) <= 3000)
res['2015ZJA-63'] = best

# 2025GK-73: modules; LP over fractions of time: 甲 produces A at 6/day or B 3/day; 乙 A 1/day or B 2/day; need 120 A, 80 B
# minimize T: 甲 spends a days on A, T-a on B; 乙 spends b on A, T-b on B: 6a+b>=120, 3(T-a)+2(T-b)>=80
best = None
for T10 in range(1, 1000):
    T = F(T10, 10)
    # maximize B given A requirement: choose a,b to minimize "B-time loss" -> comparative advantage: 甲 does A first
    # brute force a on grid
    feasible = False
    for a10 in range(0, T10 + 1):
        a = F(a10, 10)
        b = max(F(0), F(120) - 6*a)
        if b > T: continue
        if 3*(T - a) + 2*(T - b) >= 80:
            feasible = True; break
    if feasible:
        best = T; break
res['2025GK-73'] = best  # expect 28

# 2026GK-77: two teams; projects A,B,C; times 甲 (10,15,10), 乙 (12,9,18); fractional split LP
# minimize T s.t. sum_i t甲_i * p_i <= T, sum_i t乙_i*(1-p_i) <= T, 0<=p_i<=1
t1 = [10, 15, 10]; t2 = [12, 9, 18]
best = None
N = 60
for pa in range(N + 1):
    for pb in range(N + 1):
        for pc in range(N + 1):
            p = [F(pa, N), F(pb, N), F(pc, N)]
            T1 = sum(t1[i] * p[i] for i in range(3))
            T2 = sum(t2[i] * (1 - p[i]) for i in range(3))
            T = max(T1, T2)
            if best is None or T < best[0]: best = (T, p)
res['2026GK-77'] = (best[0], [str(x) for x in best[1]])
# naive: both teams together on each project in sequence
naive = sum(F(1) / (F(1, t1[i]) + F(1, t2[i])) for i in range(3))
res['2026GK-77_naive_together'] = (naive, float(naive))
# whole-project assignment (no split)
whole = min(max(sum(t1[i] for i in range(3) if m >> i & 1), sum(t2[i] for i in range(3) if not m >> i & 1)) for m in range(8))
res['2026GK-77_whole'] = whole

# 2026GD-44: storage cost; batches 4,6,7,8; fee 100/h while in warehouse
best = min((sum(sum(o[:k]) for k in range(len(o))) * 100, o) for o in permutations([4, 6, 7, 8]))
res['2026GD-44'] = best
worst = max((sum(sum(o[:k]) for k in range(len(o))) * 100, o) for o in permutations([4, 6, 7, 8]))
res['2026GD-44_worst'] = worst
allvals = sorted(set(sum(sum(o[:k]) for k in range(len(o))) * 100 for o in permutations([4, 6, 7, 8])))
res['2026GD-44_all'] = allvals

# 2021JSA-55: assignment
tab = {'甲': [3, 16, 14, 5], '乙': [7, 3, 13, 14], '丙': [5, 10, 12, 9], '丁': [7, 8, 11, 9]}
people = list(tab)
best = min((sum(tab[people[i]][p[i]] for i in range(4)), p) for p in permutations(range(4)))
res['2021JSA-55'] = best

# 2024SZ-53: squirrel - simulate by DP on depots? use formula check
# camel-banana: n=90, cap=45, dist=25, eat 1 per meter
def camel(n, cap, dist):
    pos = 0.0; load = n
    while pos < dist:
        trips = math.ceil(load / cap)
        cost_per_m = 2 * trips - 1
        if trips == 1:
            return max(0, load - (dist - pos))
        # move until load drops to (trips-1)*cap
        target = (trips - 1) * cap
        d = (load - target) / cost_per_m
        if pos + d >= dist:
            return load - cost_per_m * (dist - pos)
        pos += d; load = target
    return load
res['2024SZ-53'] = camel(90, 45, 25)

# 2023GK-66
def lab(Tlim):
    a = 200 * Tlim; b = 10000 - a
    assert b / 500 <= Tlim
    return a * 100 + b * 200
res['2023GK-66'] = (lab(15) - lab(18)) / 10000

# 2025JSA-70 MST
edges = [('E','B',7),('E','D',9),('A','B',4),('A','D',7),('A','C',5),('B','C',6),('D','C',11),('D','F',9),('F','C',6)]
def mst(nodes, edges):
    par = {n: n for n in nodes}
    def f(x):
        while par[x] != x: x = par[x]
        return x
    tot = 0; used = []
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        ru, rv = f(u), f(v)
        if ru != rv:
            par[ru] = rv; tot += w; used.append((u, v, w))
    return tot, used
res['2025JSA-70'] = mst('ABCDEF', edges)
# 2018JSA-59 MST (edges read from figure)
edges2 = [('F','A',3),('A','B',10),('A','C',4),('F','C',6.5),('F','E',7.5),('C','B',8),('C','D',2.5),('B','D',6),('C','E',3),('E','D',5)]
res['2018JSA-59'] = mst('ABCDEF', edges2)

# 2022SC2-45 courses: lower bound check via flow-ish feasibility
hours = [28, 36, 40]
def courses_feasible(D):
    need = [h // 2 for h in hours]  # days each course needs (2h/day)
    if max(need) > D: return False
    if sum(need) > 2 * D: return False
    return True
res['2022SC2-45'] = min(D for D in range(1, 100) if courses_feasible(D))

# 2022SC1-50 pillars: stacks types; 2 stacks per truck
best = None
for a in range(0, 16):      # (2T)
    for b in range(0, 10):  # (1T+2S)
        for c in range(0, 7):   # (3S)
            for d in range(0, 3):  # (1T+1S) partial etc
                pass
# general: enumerate stack patterns (t tall, s short) with 0.8t+0.6s<=2
pats = [(t, s) for t in range(0, 3) for s in range(0, 4) if 0.8*t + 0.6*s <= 2.0 + 1e-9 and (t + s) > 0]
from functools import lru_cache
@lru_cache(None)
def minstacks(T, S):
    if T <= 0 and S <= 0: return 0
    bestv = 10**9
    for t, s in pats:
        if (t > 0 and T <= 0 and s == 0): continue
        nt, ns = max(0, T - t), max(0, S - s)
        if (nt, ns) == (T, S): continue
        bestv = min(bestv, 1 + minstacks(nt, ns))
    return bestv
st = minstacks(30, 18)
res['2022SC1-50'] = (st, math.ceil(st / 2))

# 2020HB-72 goods concentration
w = {'A': 10, 'B': 20, 'C': 15, 'D': 25}; pos = {'A': 0, 'B': 5, 'C': 10, 'D': 15}
res['2020HB-72'] = min((sum(w[k] * abs(pos[k] - pos[t]) for k in w) * 3, t) for t in w)

# 2015ZJA-68 ropes (lengths in 0.1m units)
best = min((10*l + 6*m + 3*s, l, m, s) for l in range(0, 5) for m in range(0, 6) for s in range(0, 9) if 7*l + 5*m + 3*s >= 23)
res['2015ZJA-68'] = best

# 2021GK-69
people_n = 12*20 + 17*30 + 6
vmin = min(b + m for b in range(0, 40) for m in range(0, 40) if 30*b + 20*m >= people_n)
bmin = min(b for b in range(0, 40) for m in range(0, 40) if 30*b + 20*m >= people_n and b + m == vmin)
res['2021GK-69'] = (people_n, vmin, bmin)

# 2021ZJA-59
cnt = 0
for ac in range(0, 11):
    ad = 10 - ac; bc = 9 - ac; bd = 6 - bc
    if min(ad, bc, bd) < 0 or ad + bd != 7: continue
    cost = 400*ac + 600*ad + 300*bc + 700*bd
    if cost <= 7800: cnt += 1
res['2021ZJA-59'] = cnt

# 2021JSA-63
best = min((150*x + 130*(500-x) + 160*(600-x) + 145*(100+x), x) for x in range(0, 501))
res['2021JSA-63'] = best

# 2015ZJA-69
best = max((20*d + 30*t, d, t) for d in range(0, 5) for t in range(0, 5) if 2*d + 3*t <= 7 and d + t <= 4)
res['2015ZJA-69'] = best

# 2022SD-38
best = max((8*b + 3*s, b, s) for b in range(0, 13) for s in range(0, 26) if 1200*b + 600*s <= 15000)
res['2022SD-38'] = best

# 2024ZJA-57: rates
# eff: 甲+乙=3,甲+丙=4,乙+丙=5 -> 1,2,3 ; pay/h: 60,90,110 -> 20,40,70; all 3 participate; finish within 13h
best = None
for t3 in [F(k, 10) for k in range(1, 131)]:
    # 丙 works t3 hours; 甲,乙 work at most 13h each; minimize cost: cost per unit work 甲20,乙20,丙70/3
    rem = 60 - 3 * t3
    if rem < 0: continue
    # 甲乙 can do up to 3*13=39 in 13h (need both participate)
    if rem > 39: continue
    cost = 20 * rem + 70 * t3   # 甲 and 乙 both 20/unit
    if best is None or cost < best[0]: best = (cost, t3)
res['2024ZJA-57'] = (float(best[0]), float(best[1]))

# 2025SC-52
vals = [7*x + 4*(100-x) + 6*(80-x) + 5*(x-20) for x in range(20, 81)]
res['2025SC-52'] = (min(vals), max(vals), (max(vals) - min(vals)) / min(vals))

# 2015ZJA-75: triangle side 6: up=21, down=15 -> 31
res['2015ZJA-75'] = 2 * 15 + 1

for k, v in res.items():
    print(k, v)
