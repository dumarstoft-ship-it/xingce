from itertools import combinations, permutations, product
from math import comb
# v01: 3x4 lattice
pts=[(x,y) for y in range(3) for x in range(4)]
def col(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])==0
tri=sum(1 for t in combinations(pts,3) if not col(*t))
colin=[t for t in combinations(pts,3) if col(*t)]
print('v01 triangles',tri,'collinear',len(colin))
# classify collinear by direction
from collections import Counter
def d(t):
    a,b,c=sorted(t); dx,dy=c[0]-a[0],c[1]-a[1]
    return 'h' if dy==0 else 'v' if dx==0 else ('+' if dx*dy>0 else '-')
print(Counter(d(t) for t in colin))
# 2-point diagonals count
lines=set()
for a,b in combinations(pts,2):
    dx,dy=b[0]-a[0],b[1]-a[1]
    if abs(dx)==abs(dy)!=0:
        # line through a with slope sign
        s=dy//dx if dx else None
        on=frozenset(p for p in pts if (p[0]-a[0])*dy==(p[1]-a[1])*dx)
        lines.add(on)
print('diag lines by size',Counter(len(l) for l in lines))
# v02: 9 people, B labeled + two identical A groups, each group >=1 experienced (3 new)
people=list(range(9)); new={0,1,2}
plans=set()
for p in permutations(people):
    B=frozenset(p[0:3]); A1=frozenset(p[3:6]); A2=frozenset(p[6:9])
    plans.add((B,frozenset([A1,A2])))
ok=[pl for pl in plans if all(len(g-new)>=1 for g in [pl[0],*pl[1]])]
print('v02 total',len(plans),'ok',len(ok))
lab=set(); 
for p in permutations(people):
    lab.add((frozenset(p[0:3]),frozenset(p[3:6]),frozenset(p[6:9])))
okl=[x for x in lab if all(len(g-new)>=1 for g in x)]
unl=set(frozenset(x) for x in lab)
oku=[x for x in unl if all(len(g-new)>=1 for g in x)]
print('labeled',len(lab),len(okl),'unlabeled',len(unl),len(oku))
# v03
N=11
cnt=sum(1 for a,b,c in product(range(N+1),repeat=3) if min(a,b,c)>=2 and a+b+c<=N)
ex=sum(1 for a,b,c in product(range(N+1),repeat=3) if min(a,b,c)>=2 and a+b+c==N)
ge1=sum(1 for a,b,c in product(range(N+1),repeat=3) if min(a,b,c)>=1 and a+b+c<=N)
print('v03',cnt,'exact',ex,'must leave',cnt-ex,'>=1 version',ge1)
