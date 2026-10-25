import sys
sys.path.insert(0, '.')
from m04lib import *
def shuttle(L, v, trips, delay=0, stayB=0):
    tr = Traj(0, 0)
    if delay: tr.wait(delay)
    for k in range(trips):
        tr.move_to(L, v)
        if stayB: tr.wait(stayB)
        tr.move_to(0, v)
    return tr
def maxdist(A, B):
    T = max(A.end(), B.end())
    pts = sorted(A.breakpoints() | B.breakpoints() | {T})
    return max((abs(A.pos(t) - B.pos(t)), t) for t in pts)
out = []
for L in [20, 24, 30, 36, 40, 45, 48, 60]:
    for v1, v2 in [(100, 80), (90, 60), (80, 60), (60, 40), (90, 75), (120, 80), (100, 60), (60, 45), (72, 48), (75, 50)]:
        for trips in [1, 2]:
            for dl in [F(1, 10), F(1, 6), F(1, 5), F(1, 4), F(1, 3), F(1, 2)]:
                for who in ['快车晚', '慢车晚']:
                    if who == '快车晚':
                        A = shuttle(L, v1, trips, delay=dl); B = shuttle(L, v2, trips)
                    else:
                        A = shuttle(L, v1, trips); B = shuttle(L, v2, trips, delay=dl)
                    m, t = maxdist(A, B)
                    if m.denominator == 1 and 0 < m < L and t not in (A.end(), B.end(), dl):
                        out.append((L, v1, v2, trips, who, dl, m, t * 60, A.end() * 60, B.end() * 60))
for o in out[:60]:
    print('L=%s v=%s/%s trips=%s %s %s h -> 最远 %s 于 t=%s min (快完%s 慢完%s)' % o)
print(len(out))
