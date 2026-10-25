from fractions import Fraction as F

def tri(u, L):
    # position on [0,L] after travelling u from 0 with reflection
    r = u % (2*L)
    return r if r <= L else 2*L - r

# T056: pool 100, jia 100/72 m/s from 0, yi 100/60 m/s from 100, 720 s
L = F(100)
va, vb = F(100,72), F(100,60)
def pa(t): return tri(va*t, L)
def pb(t): return L - tri(vb*t, L)
# find meeting times exactly: candidate events where pa==pb; scan fine grid + exact candidates
# head-on: (va+vb)t = (2n-1)L ; catch-up: |va-vb| t = 2kL + offset... just brute-force with fine step and sign changes
import math
meet = []
N = 720*2000
prev = None
for i in range(N+1):
    t = F(i, 2000)
    d = pa(t) - pb(t)
    if d == 0:
        meet.append(float(t))
    elif prev is not None and (prev > 0) != (d > 0) and prev != 0:
        meet.append(float(t))
    prev = d
# dedupe near-duplicates
m2 = []
for t in meet:
    if not m2 or t - m2[-1] > 0.01:
        m2.append(t)
print('T056 meetings within 720s:', len(m2), [round(x,2) for x in m2])

# 2022SC1-47: A-B 30km, jia 100, yi 80, two round trips (120 km for each), max distance
L2 = 30.0
def pos(v, t, total=120.0):
    u = min(v*t, total)
    r = u % 60.0
    if u >= total: return 0.0
    return r if r <= 30 else 60 - r
best = (0, 0)
for i in range(0, 150001):
    t = i/100000*1.5
    d = abs(pos(100,t) - pos(80,t))
    if d > best[0]: best = (d, t)
print('2022SC1-47 max gap', best)

# 2026GK-79: speeds 4k,5k,6k; jia-bing meet L/(10k), yi-bing L/(11k); diff 5s => L/k = 550 ; yi catches jia: L/k
print('2026GK-79 L/k =', 5/(F(1,10)-F(1,11)), 'sec ->', float(5/(F(1,10)-F(1,11)))/60, 'min')

# 2025JSA-60: son up u, down d; father 1.2u, 0.8d; dist 1 and 2; equal times
# 1/u + 2/d = 1/(1.2u) + 2/(0.8d)  -> solve d/u
r = None
for num in range(1,200):
    for den in range(1,50):
        ratio = F(num,den)  # d = ratio*u, take u=1
        lhs = 1 + 2/ratio
        rhs = F(1)/F(6,5) + 2/(F(4,5)*ratio)
        if lhs == rhs:
            r = ratio; break
    if r: break
print('2025JSA-60 d/u =', r, ' father up:down =', F(6,5), ':', F(4,5)*r)

# 2023SZ-56 brute force: 7 soldiers from 0 at t=0..6, 8 from 9 at t=0.5..7.5, speed 1, turn on meeting, stop at ends
# simulate on time step 1/8 (all events are on multiples of 1/4)
dt = F(1,8)
sold = []  # [pos, dir, active, started]
spawn = [(F(i),0,1) for i in range(7)] + [(F(1,2)+i,9,-1) for i in range(8)]
t = F(0); active=[]; done=0; last=None
events = sorted(spawn)
while True:
    # spawn
    for s in [e for e in events if e[0]==t]:
        active.append([F(s[1]), s[2]])
    events = [e for e in events if e[0]!=t]
    # move
    if not active and not events: break
    for s in active: s[0] += s[1]*dt
    # stop at ends
    still=[]
    for s in active:
        if (s[0] <= 0 and s[1]==-1) or (s[0] >= 9 and s[1]==1):
            done += 1; last = t+dt
        else: still.append(s)
    active = still
    # turn on meeting (same position, opposite dirs) or crossing
    pos_map = {}
    for s in active: pos_map.setdefault(s[0], []).append(s)
    for p, group in pos_map.items():
        dirs = set(g[1] for g in group)
        if len(dirs) == 2:
            for g in group: g[1] = -g[1]
    t += dt
    if t > 40: break
print('2023SZ-56 all stopped at', last, 'count', done)
