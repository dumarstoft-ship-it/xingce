import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_M04_work/v2')
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
res=[]
for L in [24, 30, 36, 40, 45, 48, 60]:
    for v1, v2 in [(90,60),(80,60),(100,80),(120,80),(60,40),(75,50),(90,72),(120,90)]:
        for trips in [1,2]:
            for delay in [F(0),F(1,12),F(1,6),F(1,5),F(1,4),F(1,3)]:
                for stay in [F(0),F(1,12),F(1,6),F(1,4)]:
                    if (delay==0)==(stay==0): continue
                    A = shuttle(L, v1, trips, stayB=stay)
                    B = shuttle(L, v2, trips, delay=delay)
                    m, t = maxdist(A, B)
                    # 常见错解：甲回到A时的距离
                    tA = A.end(); naive = abs(A.pos(tA)-B.pos(tA))
                    if m.denominator==1 and 0<m<L and naive!=m and t not in (A.end(),B.end()):
                        res.append((L,v1,v2,trips,delay,stay,m,t,naive))
print(len(res))
for r in res[:60]:
    print(r)
