# Independent blind solvers for revh_A (written before opening the key).
from fractions import Fraction as Fr
from itertools import combinations, permutations, product
import math

res = {}

# ---------- Q1 D02-math-h-v01 : sorting lines ----------
# day1: 8:00 start, each 280. At 12:00 (4h) A left 160, B left 80; C done at 11:30 (3.5h)
vA = Fr(280 - 160, 4); vB = Fr(280 - 80, 4); vC = Fr(280, Fr(7, 2))
# day2: total 560; A,B start 8:00, C starts 9:00; all finish together at T hours after 8:00
# brute force: scan T in small fractional steps
sol = []
for num in range(1, 2000):
    T = Fr(num, 60)  # minute resolution
    if T <= 1: continue
    if vA * T + vB * T + vC * (T - 1) == 560:
        sol.append((T, vC * (T - 1)))
res['Q1'] = (vA, vB, vC, sol)

# ---------- Q2 D02-math-h-v02 : expedition supplies ----------
s2 = []
for N in range(7, 500):
    total = 25 * N          # person-days
    left = total - 5 * N    # after 5 days
    left -= 6 * 5           # 6 people take 5 days of return supplies
    if left == 23 * (N - 6):
        s2.append(N)
res['Q2'] = s2

# ---------- Q3 D02-math-h-v03 : pumping (cow-grass) ----------
# pump rate 1/h each; inflow r; initial W
# W + 18 r = 10*18 ; W + 9 r = 14*9
r = Fr(10 * 18 - 14 * 9, 18 - 9); W = 10 * 18 - 18 * r
s3 = []
for n in range(4, 100):
    # simulate in fine steps (exact)
    water = W + r * 6 - (4 * n + 2 * (n - 3))
    # also make sure not dried before the end: water level at t=4 must stay > 0 and at t=6 ==0
    lvl4 = W + 4 * r - 4 * n
    if water == 0 and lvl4 > 0:
        s3.append(n)
res['Q3'] = (r, W, s3)

# ---------- Q4 D02-math-h-v04 : dredging ships added every 5 days ----------
done = 0; day = 0
while done < 300:
    day += 1
    ships = (day - 1) // 5 + 1
    done += ships
res['Q4'] = (day, done)

# ---------- Q5 D02-math-h-v05 : +40% then -40% ----------
s5 = []
for T in range(1, 500):
    Wk = Fr(T)  # planned efficiency 1 per day, work = T
    actual = (Wk / 2) / Fr(14, 10) + (Wk / 2) / Fr(6, 10)
    if actual - T == 4:
        s5.append(T)
res['Q5'] = s5

# ---------- Q6 D03-math-h-v01 : three walkers ----------
s6 = []
for D in range(100, 20000):
    t_yi = Fr(D, 75 + 65); t_jia = Fr(D, 60 + 65)
    if t_jia - t_yi == 6:
        s6.append(D)
res['Q6'] = s6

# ---------- Q7 D03-math-h-v02 : bus shuttling two teams ----------
# brute force on drop-off point d (in km, fine grid of fractions)
s7 = []
L = 18; v = 36; u = 4
for k in range(1, 18 * 60):
    d = Fr(k, 60)            # drop-off distance of team Jia
    t_drop = d / v
    jia_arrive = t_drop + (L - d) / u
    # bus returns to meet Yi
    yi_pos = u * t_drop
    t_meet = t_drop + (d - yi_pos) / (v + u)
    meet_pos = u * t_meet
    yi_arrive = t_meet + (L - meet_pos) / v
    if jia_arrive == yi_arrive:
        s7.append((d, jia_arrive * 60))
res['Q7'] = s7

# ---------- Q8 D03-math-h-v03 : bus schedule ----------
# minutes after 6:30. buses from both terminals at 0,8,16,...; trip 48.
my_dep = 16; my_arr = my_dep + 48
cnt = 0; met = []
for s in range(0, 24 * 60, 8):  # departures from Yi that day
    # meet time solves (t - my_dep) = 48 - (t - s)  -> positions as fraction of route from Jia
    t = Fr(my_dep + 48 + s, 2)
    if my_dep < t < my_arr and s < t < s + 48:   # strictly on the road for both
        cnt += 1; met.append(s)
res['Q8'] = (cnt, met)

# ---------- Q9 D03-math-h-v04 : nearest distance ----------
best = None
for k in range(0, 100001):
    t = Fr(k, 10000) * Fr(100, 32)   # until cargo ship reaches O
    x = -100 + 32 * t; y = 24 * t
    dd = x * x + y * y
    if best is None or dd < best[0]:
        best = (dd, t)
res['Q9'] = (math.sqrt(best[0]), best[1])

# ---------- Q10 D05-math-h-v01 : triangles in 3x4 grid ----------
pts = [(r_, c) for r_ in range(3) for c in range(4)]
tri = 0
for a, b, c in combinations(pts, 3):
    area2 = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if area2 != 0:
        tri += 1
res['Q10'] = tri

# ---------- Q11 D05-math-h-v02 : grouping ----------
people = list(range(9))   # 0,1,2 new; 3..8 experienced
new = {0, 1, 2}
arr = set()
for perm in permutations(people):
    g1 = frozenset(perm[0:3]); g2 = frozenset(perm[3:6]); g3 = frozenset(perm[6:9])
    if all(len(g - new) >= 1 for g in (g1, g2, g3)):
        # g1,g2 = two identical home-visit groups (unordered); g3 = fire-check group
        arr.add((frozenset([g1, g2]), g3))
res['Q11'] = len(arr)

# ---------- Q12 D05-math-h-v03 : identical books with leftovers ----------
c12 = 0
for x in product(range(12), repeat=3):
    if all(xi >= 2 for xi in x) and sum(x) <= 11:
        c12 += 1
res['Q12'] = c12

# ---------- Q13 D07-math-h-v01 : fence cost ----------
best13 = None
for k in range(1, 50001):
    x = Fr(k, 1000)            # side parallel to wall (<= 50)
    y = Fr(600) / x            # depth (<= 15)
    if x <= 50 and y <= 15:
        cost = 200 * x + 150 * 2 * y
        if best13 is None or cost < best13[0]:
            best13 = (cost, x, y)
res['Q13'] = best13

# ---------- Q14 D07-math-h-v02 : extended triangle ----------
A = (Fr(0), Fr(0)); B = (Fr(7), Fr(0)); C = (Fr(2), Fr(5))
def area(P, Q, R):
    return abs((Q[0] - P[0]) * (R[1] - P[1]) - (Q[1] - P[1]) * (R[0] - P[0])) / 2
def ext(P, Q, k):   # point beyond Q on ray PQ with QX = k*PQ
    return (Q[0] + k * (Q[0] - P[0]), Q[1] + k * (Q[1] - P[1]))
D = ext(A, B, 2); E = ext(B, C, 1); F = ext(C, A, 4)
ratio = area(D, E, F) / area(A, B, C)
res['Q14'] = (ratio, ratio * 5)

for k, v_ in res.items():
    print(k, v_)
