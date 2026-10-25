# Extra discrete simulations (blind, before the key)
from fractions import Fraction as F

# ---- 2-v11: real bus fleet on a 0..Lr line, both terminals dispatch every T min, cyclist rides at speed u
def bus_sim(T, V, u, Lr=F(600), tmax=F(2000)):
    # cyclist starts at x=100 at t=0 going +; buses from x=0 going + depart at k*T, from x=Lr going - depart at k*T + phase
    over, oncoming = [], []
    # overtaking bus k (from 0): position V*(t - kT) ; cyclist 100 + u t ; meet when V(t-kT) = 100+ut
    for k in range(-400, 400):
        t = (100 + V * k * T) / (V - u)
        if 0 < t < tmax and 0 <= 100 + u * t <= Lr:
            over.append(t)
        # oncoming bus from Lr: Lr - V(t - kT - phase)
        phase = F(7, 3)
        t2 = (Lr - 100 + V * (k * T + phase)) / (V + u)
        if 0 < t2 < tmax and 0 <= 100 + u * t2 <= Lr and t2 >= k * T + phase:
            oncoming.append(t2)
    over.sort(); oncoming.sort()
    d1 = {over[i + 1] - over[i] for i in range(len(over) - 1)}
    d2 = {oncoming[i + 1] - oncoming[i] for i in range(len(oncoming) - 1)}
    return d1, d2

# unknown bus speed V relative to cyclist u=1 ; try T=12 with V solved from 18 & 9 -> V=3 ; check others fail
for T in [6, 9, 12, F(27, 2)]:
    found = []
    for V in [F(n, 4) for n in range(5, 81)]:
        d1, d2 = bus_sim(F(T), V, F(1))
        if d1 == {18} and d2 == {9}:
            found.append(V)
    print('2-v11 T=', T, 'bus speeds giving (18,9):', found)

# ---- 2-v04: ring 500, 乙 100 ahead, speeds 4 and 5 (any scale) ; time-step count of 乙 catching 甲
def ring_catch(n_target, va=4, vb=5, Lr=500, start_gap=100):
    # positions measured along running direction ; 甲 at 0, 乙 at 100
    # 乙 catches 甲 when (pos乙 - pos甲) increases through a multiple of 500 (beyond the initial 100)
    t = F(0); cnt = 0
    # gap(t) = 100 + (vb - va) t ; catch when gap = 500 m * j for j>=1
    j = 1
    while True:
        tj = F(Lr * j - start_gap, vb - va)
        cnt += 1
        if cnt == n_target:
            return tj, vb * tj
        j += 1
print('2-v04 second catch (t, 乙 distance):', ring_catch(2))
# scale-invariance check
print('2-v04 scaled speeds 8,10:', ring_catch(2, 8, 10))

# ---- 1-v13 time-stepping check: catch iff min gap <= 0 over a long horizon
def min_gap(vb, dt=F(1, 600), horizon=F(12)):
    va = vb + 4
    t = F(0); g = None; best = None
    while t <= horizon:
        if t <= F(5, 2):
            pa = va * t
        elif t <= F(5, 2) + F(2, 3):
            pa = va * F(5, 2)
        else:
            pa = va * F(5, 2) + va * (t - F(5, 2) - F(2, 3))
        pb = vb * t
        gap = pa - pb
        if t > 0:
            best = gap if best is None else min(best, gap)
        t += dt
    return best
for vb in [14, F(299, 20), 15, 16, 19]:
    print('1-v13 v乙=', vb, 'min gap after start =', float(min_gap(F(vb))))

# ---- 2-v02: dense real-valued scan of L to confirm uniqueness of L=90
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/rev_D03m_work')
