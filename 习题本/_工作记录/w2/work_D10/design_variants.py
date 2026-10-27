from fractions import Fraction as F
from itertools import permutations, combinations

print("== v1: 3-constraint LP (example skeleton)")
# land x+y<=100 ; water 3x+y<=240 ; labor x+3y<=240 ; profit 4x+5y
cons = [((1,1),100,'land'), ((3,1),240,'water'), ((1,3),240,'labor')]
def feas(x,y): return x>=0 and y>=0 and all(a*x+b*y<=c for (a,b),c,_ in cons)
pts = []
lines = cons + [((1,0),0,'x=0'), ((0,1),0,'y=0')]
for (p,c1,n1),(q,c2,n2) in combinations(lines,2):
    a1,b1=p; a2,b2=q
    det=a1*b2-a2*b1
    if det==0: continue
    x=F(c1*b2-c2*b1,det); y=F(a1*c2-a2*c1,det)
    pts.append((n1,n2,x,y,feas(x,y),4*x+5*y))
for r in pts: print(r[0],r[1],'->',r[2],r[3],'feasible' if r[4] else 'INFEASIBLE','profit',r[5])
best=max(4*x+5*y for x in range(0,101) for y in range(0,101) if feas(x,y))
print('integer optimum', best)

print("\n== v2: weighted storage ordering search")
import random
random.seed(7)
cands=[]
for ts in combinations([2,3,4,5,6,8],4):
    for ws in permutations([100,200,300,400,500,600],4):
        items=list(zip(ts,ws))
        ratios=[t/w for t,w in items]
        if len(set(ratios))<4: continue
        def cost(order):
            tot=0; elapsed=0
            for t,w in order:
                tot+=w*elapsed   # waiting only
                elapsed+=t
            return tot
        allc={o:cost(o) for o in permutations(items)}
        opt=min(allc.values())
        spt=cost(tuple(sorted(items,key=lambda z:z[0])))
        feehi=cost(tuple(sorted(items,key=lambda z:-z[1])))
        ratio=cost(tuple(sorted(items,key=lambda z:z[0]/z[1])))
        assert ratio==opt
        nopt=sum(1 for v in allc.values() if v==opt)
        if nopt==1 and spt!=opt and feehi!=opt and spt!=feehi and opt%100==0:
            # want SPT order and fee order to both be wrong by a decent margin
            cands.append((min(spt,feehi)-opt, items, opt, spt, feehi))
cands.sort(key=lambda z:-z[0])
for c in cands[:6]: print(c)

print("\n== v3: budget -> min time (example)")
# 甲 alone 20 days at 5/day (100 per project), 乙 alone 30 days at 3/day (90 per project), budget 94
best=None
for T10 in range(10,400):
    T=F(T10,10)
    # 乙 works T days (cheaper per unit work); 甲 does the rest if it fits in T
    share_y=min(F(1),T/30); share_x=1-share_y
    if share_x/F(1,20) > T: continue
    cost=share_x*100+share_y*90
    if cost<=94: best=T; break
print('min T',best)
T_ideal=F(1)/(F(1,20)+F(1,30)); print('ideal T (ignore budget)',T_ideal,'cost',T_ideal*8)

print("\n== v4: goods concentration on a branched road (example)")
# tree: A-B 4, B-C 3, C-D 5, C-E 6, B-F 2 ; weights
edges={('A','B'):4,('B','C'):3,('C','D'):5,('C','E'):6,('B','F'):2}
w={'A':8,'B':5,'C':6,'D':9,'E':12,'F':4}
adj={}
for (u,v),d in edges.items():
    adj.setdefault(u,[]).append((v,d)); adj.setdefault(v,[]).append((u,d))
def dists(s):
    D={s:0}; st=[s]
    while st:
        u=st.pop()
        for v,d in adj[u]:
            if v not in D: D[v]=D[u]+d; st.append(v)
    return D
costs={s:sum(w[k]*dists(s)[k] for k in w) for s in w}
print(sorted(costs.items(), key=lambda z:z[1]))
