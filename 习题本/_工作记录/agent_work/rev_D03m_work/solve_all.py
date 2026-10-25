# Independent blind solver for D03 math (行程) - written BEFORE opening the key.
# Every question is solved from the stem data; where useful an event simulation is used.
import json, math
from fractions import Fraction as F

Q = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/review/D03_math_questions.json'))
opts = {q['vid']: q['options'] for q in Q}
res = {}

def match(vid, value, fmt=None, tol=1e-9):
    """return list of option letters whose numeric value equals `value`"""
    hits = []
    for k, s in opts[vid].items():
        if fmt is not None:
            if fmt(s) == value:
                hits.append(k)
            continue
        try:
            x = float(s.replace('%', ''))
        except ValueError:
            continue
        if abs(x - float(value)) < tol:
            hits.append(k)
    return hits

# ---------------- generic bouncing simulator on segment [0,L] ----------------
def bounce_meetings(L, x0, d0, v0, x1, d1, v1, tmax, maxn=50):
    """two walkers on [0,L], start pos x, direction d (+1 toward L), speed v (Fractions).
    Turn instantly at ends. Return list of (t, pos, kind) meetings, kind 'head'/'catch'/'both-end'."""
    t = F(0)
    s = [[F(x0), d0, F(v0)], [F(x1), d1, F(v1)]]
    out = []
    while t < tmax and len(out) < maxn:
        # time to next wall event for each
        def wall(p):
            x, d, v = p
            return (F(L) - x) / v if d > 0 else x / v
        tw = min(wall(s[0]), wall(s[1]))
        # time to meeting with current directions
        (xa, da, va), (xb, db, vb) = s
        rel = da * va - db * vb
        tm = None
        if rel != 0:
            cand = (xb - xa) / rel
            if cand > 0:
                tm = cand
        if tm is not None and tm <= tw:
            t += tm
            for p in s:
                p[0] += p[1] * p[2] * tm
            kind = 'head' if da != db else 'catch'
            # record, then advance an epsilon by stepping to next wall without re-detecting same meeting
            out.append((t, s[0][0], kind, da, db))
            # move to the wall event (no more meeting before it except this one)
            tw2 = min(wall(s[0]), wall(s[1]))
            if tw2 == 0:
                for p in s:
                    if (p[1] > 0 and p[0] == L) or (p[1] < 0 and p[0] == 0):
                        p[1] = -p[1]
                continue
            # step to just the next wall
            t += tw2
            for p in s:
                p[0] += p[1] * p[2] * tw2
            for p in s:
                if (p[1] > 0 and p[0] == L) or (p[1] < 0 and p[0] == 0):
                    p[1] = -p[1]
            # check meeting exactly at the wall moment
            if s[0][0] == s[1][0]:
                out.append((t, s[0][0], 'at-wall', s[0][1], s[1][1]))
            continue
        t += tw
        for p in s:
            p[0] += p[1] * p[2] * tw
        for p in s:
            if (p[1] > 0 and p[0] == L) or (p[1] < 0 and p[0] == 0):
                p[1] = -p[1]
        if s[0][0] == s[1][0]:
            out.append((t, s[0][0], 'at-wall', s[0][1], s[1][1]))
    return out

# ======================= batch 1 =======================
# 1-v01: 1500 m, same start; fast returns, meets slow 300 from end
L = F(1500); fast_total = L + 300; slow_total = L - 300
ratio = fast_total / slow_total
slow_when_fast_at_end = L / ratio
ans = L - slow_when_fast_at_end
# simulation check with speeds 3,2 scaled from ratio
vf, vs = ratio, F(1)
m = bounce_meetings(1500, 0, 1, vf, 0, 1, vs, F(10**6), maxn=1)
assert m[0][1] == 1200, m
res['D03-math-1-v01'] = (ans, match('D03-math-1-v01', ans))

# 1-v02: sum = L/3 -> 甲 walked 800; sum = 5L/6 -> 乙 walked 3000
# unknowns r = va/(va+vb), L:  r*L/3 = 800 ; (1-r)*5L/6 = 3000
# => rL = 2400 ; (1-r)L = 3600 ; L = 6000
rL = F(800) * 3
oneminus_rL = F(3000) * F(6, 5)
Ltot = rL + oneminus_rL
res['D03-math-1-v02'] = (rL, match('D03-math-1-v02', rL))
v02_note = f"L={Ltot}, meeting from A={rL}; note: meeting from A follows from cond.1 alone (800*3)"

# 1-v03: after meeting 甲 16 min to B, 乙 25 min to A, v甲=200 m/min
# t^2 = 16*25 -> t=20 ; verify by solving: v甲*16 = v乙*t, v乙*25 = v甲*t
t = math.isqrt(16 * 25)
vb = F(200 * 16, t)
assert vb * 25 == 200 * t
AB = 200 * (t + 16)
res['D03-math-1-v03'] = (AB, match('D03-math-1-v03', AB))

# 1-v04: 300 km, 甲 const; 乙 0.5h at v, then v+24 for 2.5h; same arrival
T = F(1, 2) + F(5, 2)
va = F(300) / T
v = (F(300) - F(5, 2) * 24) / T
pct = (va / v - 1) * 100
res['D03-math-1-v04'] = (pct, match('D03-math-1-v04', pct))

# 1-v05: speed -1/6 whole -> +12 min ; first 20 km normal then -1/6 -> +8 min
# brute force over integer distance and speed to be safe
sols = []
for S in range(21, 301):
    # extra = (S/(5v/6) - S/v) = S/(5v) hours = 12/60 -> v = S
    v_ = F(S) / 5 / F(12, 60)
    extra2 = (F(S - 20) / (v_ * F(5, 6)) - F(S - 20) / v_) * 60
    if extra2 == 8:
        sols.append((S, v_))
assert len(sols) == 1, sols
res['D03-math-1-v05'] = (sols[0][0], match('D03-math-1-v05', sols[0][0]))

# 1-v06: detour = 3 d, speed v; channel d at 4v/3; save 1 h; find channel minutes
# let d/v = x hours: 3x - 3x/4 = 1 -> x = 4/9 ; channel time = 3x/4 h
x = F(1) / (3 - F(3, 4))
chan_min = F(3, 4) * x * 60
res['D03-math-1-v06'] = (chan_min, match('D03-math-1-v06', chan_min))

# 1-v07: avg = 1.2 v1, harmonic mean of v1, v2
v1 = F(1); avg = F(6, 5)
# 2 v1 v2 / (v1 + v2) = avg -> v2 (2 v1 - avg) = avg v1
v2 = avg * v1 / (2 * v1 - avg)
pct = (v2 / v1 - 1) * 100
res['D03-math-1-v07'] = (pct, match('D03-math-1-v07', pct))

# 1-v08: 甲 half time 10 / 6 ; 乙 half distance 10 / 6 ; 甲 earlier 6 min
# time甲 = S/8 ; time乙 = S/20 + S/12
coef = (F(1, 20) + F(1, 12)) - F(1, 8)
S = F(6, 60) / coef
res['D03-math-1-v08'] = (S, match('D03-math-1-v08', S))

# 1-v09: up base->station 75 min, rest 15, down summit->station 30, station->base 45
ratio_up_down = F(75, 45)
up_station_summit = 30 * ratio_up_down
arr = 8 * 60 + 75 + 15 + up_station_summit
hhmm = f"{int(arr)//60}:{int(arr)%60:02d}"
res['D03-math-1-v09'] = (hhmm, [k for k, s in opts['D03-math-1-v09'].items() if s == hhmm])

# 1-v10: flat 20, up 10, down 30 ; go flat then up 36 min ; back down then flat 24 min
# f/20 + s/10 = 36/60 ; s/30 + f/20 = 24/60
s = (F(36, 60) - F(24, 60)) / (F(1, 10) - F(1, 30))
f = (F(36, 60) - s / 10) * 20
res['D03-math-1-v10'] = (f + s, match('D03-math-1-v10', f + s))

# 1-v11: 9 km apart, 甲 5 km/h; drone from t=0.25h at 40 km/h until meeting, flew 30 km
fly_t = F(30, 40)
t_meet = F(1, 4) + fly_t
vb = F(9) / t_meet - 5
# numeric zigzag simulation check for each option
def drone_dist(vb):
    va = 5.0; t = 0.25; xa = va * t; xb = 9 - vb * t; xd = xa; dirn = 1; dist = 0.0
    for _ in range(200000):
        if xb - xa < 1e-12:
            break
        if dirn == 1:
            dt = (xb - xd) / (40 + vb)
        else:
            dt = (xd - xa) / (40 + va)
        # cap at meeting time
        tm = (xb - xa) / (va + vb)
        if dt > tm:
            dt = tm
        xa += va * dt; xb -= vb * dt; xd += dirn * 40 * dt; dist += 40 * dt; t += dt
        dirn = -dirn
    return dist
sim = {k: round(drone_dist(float(s)), 6) for k, s in opts['D03-math-1-v11'].items()}
res['D03-math-1-v11'] = (vb, match('D03-math-1-v11', vb), sim)

# 1-v12: 140 km, 乙 later by d, catches 甲 at 60 km, arrives 24 min earlier
# for several v甲, solve v乙 and d; d must be invariant
ds = set()
for vA in [30, 40, 45, 50, 60, 72, 80]:
    pa = F(60, 1) / vA  # hours per km * 60 -> minutes per km
    pa = F(60, vA)      # min per km
    # 80*(pa - pb) = 24  -> pb = pa - 24/80
    pb = pa - F(24, 80)
    if pb <= 0:
        continue
    vB = F(60) / pb
    d = 60 * pa - 60 * pb
    # recheck both conditions
    assert 60 * pa == d + 60 * pb
    assert 140 * pa - (d + 140 * pb) == 24
    assert vB > vA
    ds.add(d)
assert len(ds) == 1
d = ds.pop()
res['D03-math-1-v12'] = (d, match('D03-math-1-v12', d))

# 1-v13: 甲 = 乙 + 4 ; after 2.5 h 甲 rests 40 min ; min 乙 speed to catch en route
def catches(vb, horizon=100.0):
    va = vb + 4
    # 甲 position piecewise; check if gap <= 0 at any time
    # during rest gap = 10 - vb*(t-2.5) ; after rest gap grows
    gap_end_rest = 4 * 2.5 - vb * (40 / 60)
    return gap_end_rest <= 1e-12
lo, hi = 0.0, 100.0
for _ in range(200):
    mid = (lo + hi) / 2
    if catches(mid):
        hi = mid
    else:
        lo = mid
vmin = F(4 * 5, 2) / F(40, 60)
assert abs(hi - float(vmin)) < 1e-9
res['D03-math-1-v13'] = (vmin, match('D03-math-1-v13', vmin))

# 1-v14: arrives 7:25, walks 27 min, meets shuttle; shuttle normally at exit 8:00
# simulate with arbitrary shuttle speed c and walking speed w with 27 w = 8 c?  NO - derive:
# choose D (company->exit) and c; shuttle departs 8:00 - D/c ; walker from 7:25 at speed w.
# meeting time = 7:25 + 27 (given) -> solve w from meeting, then compute arrival diff
diffs = set()
for D, c in [(F(10), F(1, 2)), (F(12), F(2, 5)), (F(30), F(1))]:
    dep = 8 * 60 - D / c
    tmeet = 7 * 60 + 25 + 27
    # shuttle pos from exit at tmeet: D - c*(tmeet - dep)
    pos_from_exit = D - c * (tmeet - dep)
    w = pos_from_exit / 27
    assert w > 0 and tmeet > dep
    arrive = tmeet + (D - pos_from_exit) / c
    normal = 8 * 60 + D / c
    diffs.add(normal - arrive)
assert len(diffs) == 1
dd = diffs.pop()
res['D03-math-1-v14'] = (dd, match('D03-math-1-v14', dd))

# ======================= batch 2 =======================
# 2-v01: AB 900, both from A, 70 & 50 m/min, 2nd head-on meeting
ms = bounce_meetings(900, 0, 1, 70, 0, 1, 50, F(1000))
heads = [mm for mm in ms if mm[2] == 'head' or (mm[2] == 'at-wall' and mm[3] != mm[4])]
res['D03-math-2-v01'] = (heads[1][1], match('D03-math-2-v01', heads[1][1]), [(str(a), str(b), c) for a, b, c, *_ in ms[:5]])

# 2-v02: A,B opposite start, 1st head-on 40 from A, 2nd head-on 60 from A ; find L
def check_L(L):
    L = F(L)
    if L <= 40:
        return False
    va, vb = F(40), L - 40
    ms = bounce_meetings(L, 0, 1, va, L, -1, vb, F(10**4), maxn=10)
    heads = [mm for mm in ms if mm[2] == 'head']
    return len(heads) >= 2 and heads[0][1] == 40 and heads[1][1] == 60
cand = [L for L in range(41, 1001) if check_L(L)]
# also half-integers
cand_half = [F(k, 2) for k in range(83, 1001) if check_L(F(k, 2))]
res['D03-math-2-v02'] = (cand, [k for k, s in opts['D03-math-2-v02'].items() if check_L(int(s))], cand_half)

# 2-v03: ring, start half lap apart, opposite directions, 甲 16 min/lap, 乙 24 min/lap; 3rd meeting
va, vb = F(1, 16), F(1, 24)
# meetings when combined = 1/2 + k
t3 = (F(1, 2) + 2) / (va + vb)
laps_b = vb * t3
# simulate numerically: positions on circle, count meetings
def ring_meet_count(tend, steps=200000):
    cnt = 0; prev = None
    for i in range(1, steps + 1):
        tt = tend * i / steps
        pa = (0 + float(va) * tt) % 1
        pb = (0.5 - float(vb) * tt) % 1
        gap = (pb - pa) % 1
        if prev is not None and gap > prev + 0.5:  # wrapped
            cnt += 1
        prev = gap
    return cnt
assert ring_meet_count(float(t3) + 1e-6) == 3
res['D03-math-2-v03'] = (laps_b, match('D03-math-2-v03', laps_b))

# 2-v04: 500 m ring, 乙 100 m ahead, v乙 = 1.25 v甲 ; 乙 catches 甲 second time
vA, vB = F(4), F(5)
gain_needed = (500 - 100) + 500
tt = gain_needed / (vB - vA)
dist_b = vB * tt
res['D03-math-2-v04'] = (dist_b, match('D03-math-2-v04', dist_b))

# 2-v05: 36 s and 84 s per lap ; same direction ; count catch-ups in (0, first common return]
Tc = 36 * 84 // math.gcd(36, 84)
cnt = 0
for tsec in range(1, Tc + 1):
    # 甲 laps minus 乙 laps crosses integer
    diff_now = F(tsec, 36) - F(tsec, 84)
    diff_prev = F(tsec - 1, 36) - F(tsec - 1, 84)
    if math.floor(diff_now) > math.floor(diff_prev):
        cnt += 1
res['D03-math-2-v05'] = (cnt, match('D03-math-2-v05', cnt))

# 2-v06: 甲 catches 乙 every 24, 乙 catches 丙 every 40
per = 1 / (F(1, 24) + F(1, 40))
res['D03-math-2-v06'] = (per, match('D03-math-2-v06', per))

# 2-v07: 72 km, down 3 h, up 4 h, new still-water 30
down, up = F(72, 3), F(72, 4)
cur = (down - up) / 2
tnew = F(72) / (30 - cur)
hm = f"{int(tnew)}小时{int((tnew - int(tnew)) * 60)}分"
res['D03-math-2-v07'] = (hm, [k for k, s in opts['D03-math-2-v07'].items() if s == hm])

# 2-v08: upstream boat 16 still, current 4; buoy drops, noticed 15 min later, turn & chase
# ground frame computation
t1 = F(15, 60)
boat_up = 16 - 4
gap = boat_up * t1 + 4 * t1  # separation after t1 (boat moved up, buoy moved down)
t2 = gap / ((16 + 4) - 4)
drift = 4 * (t1 + t2)
res['D03-math-2-v08'] = (drift, match('D03-math-2-v08', drift))

# 2-v09: escalator up; 王 walks 24 steps; 李 rate 2x walks 40 steps ; N ?
# N = 24 + e*24/w ; N = 40 + e*40/(2w)  -> x = e/w
x = F(40 - 24) / (24 - 20)
N = 24 + 24 * x
assert N == 40 + 20 * x
res['D03-math-2-v09'] = (N, match('D03-math-2-v09', N))

# 2-v10: overtaken train 120 km/h ; HSR 350 m at 300 km/h overtakes; time head-to-tail past window
rel = F(300 - 120) * 1000 / 3600
tt = F(350) / rel
res['D03-math-2-v10'] = (tt, match('D03-math-2-v10', tt))

# 2-v11: overtaken every 18, oncoming every 9 ; departure interval
T = 2 * F(18 * 9) / (18 + 9)
# simulation check: bus speed V=3, bike v=1, interval T, buses on infinite line both directions
V, vbk = F(3), F(1)
spacing = V * T
# overtaking frequency: spacing / (V - v) ; oncoming: spacing / (V + v)
assert spacing / (V - vbk) == 18 and spacing / (V + vbk) == 9
res['D03-math-2-v11'] = (T, match('D03-math-2-v11', T))

# 2-v12: accelerate 10 s, cruise 30 s, decelerate 10 s, total 240 m
vmax = F(240) / (F(10, 2) + 30 + F(10, 2))
res['D03-math-2-v12'] = (vmax, match('D03-math-2-v12', vmax))

# 2-v13: A west of B ; 甲 east, 乙 west, v甲 = 4/3 v乙 ; after meeting 乙 north ; when 甲 at B, distance 75
# AB = 7k ; meeting 4k from A; 甲 needs 3k at speed 4 -> time 3k/4; 乙 north 9k/4
k = F(75) / F(15, 4)
AB = 7 * k
# geometric re-check
dx, dy = 3 * k, F(9, 4) * k
assert dx * dx + dy * dy == 75 * 75
res['D03-math-2-v13'] = (AB, match('D03-math-2-v13', AB))

for vid in [q['vid'] for q in Q]:
    r = res[vid]
    print(vid, '->', r)
print(v02_note)
