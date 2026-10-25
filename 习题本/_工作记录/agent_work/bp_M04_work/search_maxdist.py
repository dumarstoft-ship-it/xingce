import sys
sys.path.insert(0, '.')
from m04lib import *
def shuttle(L, v, trips, delay=0, stayB=0, stayA=0):
    tr = Traj(0, 0)
    if delay: tr.wait(delay)
    for k in range(trips):
        tr.move_to(L, v)
        if stayB: tr.wait(stayB)
        tr.move_to(0, v)
        if stayA and k < trips - 1: tr.wait(stayA)
    return tr
def maxdist(A, B):
    T = max(A.end(), B.end())
    pts = sorted(A.breakpoints() | B.breakpoints() | {T})
    best = max((abs(A.pos(t) - B.pos(t)), t) for t in pts)
    return best
res = []
for L in [20, 24, 30, 36, 40, 45, 48, 60]:
    for v1, v2 in [(100, 80), (90, 60), (80, 60), (60, 40), (90, 75), (120, 80), (100, 60), (60, 45), (72, 48), (75, 50)]:
        for trips in [1, 2]:
            for delay in [F(0), F(1, 10), F(1, 6), F(1, 5), F(1, 4), F(1, 3), F(1, 2)]:
                for stay in [F(0), F(1, 10), F(1, 6), F(1, 5), F(1, 4)]:
                    A = shuttle(L, v1, trips, stayB=stay)
                    B = shuttle(L, v2, trips, delay=delay)
                    m, t = maxdist(A, B)
                    if m.denominator == 1 and 0 < m < L and t not in (A.end(), B.end()) :
                        res.append((L, v1, v2, trips, delay, stay, m, t, A.end(), B.end()))
print(len(res))
# 优先：无停留+乙晚出发；有停留+同时出发
for r in res:
    L, v1, v2, trips, delay, stay, m, t, ea, eb = r
    if (delay == 0) != (stay == 0) and trips == 2:
        print('L=%s v=%s/%s trips=%s 乙晚%s h 甲在B停%s h -> 最远 %s 于 t=%s (甲完%s 乙完%s)' % (L, v1, v2, trips, delay, stay, m, t, ea, eb))
