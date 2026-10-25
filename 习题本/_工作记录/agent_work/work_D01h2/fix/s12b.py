from fractions import Fraction as F
from itertools import combinations
def solve(p,q,S,dest,avg_override=None,sign=1):
    n=100
    c={1:n+p,2:n,3:n+q}
    m=F(sum(c.values()),3) if avg_override is None else avg_override(c)
    sols=[]
    for g1 in range(1,80):
      for g2 in range(1,80):
        g3=S-g1-g2
        if g3<1: continue
        g={1:g1,2:g2,3:g3}
        inc={1:0,2:0,3:0}
        for i in (1,2,3): inc[dest[i]]+=g[i]
        if all(sign*(inc[i]-g[i])==m-c[i] for i in (1,2,3)): sols.append((g1,g2,g3))
    return sols
R={1:3,3:2,2:1}     # 甲->丙, 丙->乙, 乙->甲
RV={1:2,2:3,3:1}
out=[]
for p in range(-12,13):
  for q in range(-12,13):
    if p==0 or q==0 or p==q or (p+q)%3: continue
    for S in range(24,61):
      s=solve(p,q,S,R)
      if len(s)!=1: continue
      g=s[0]
      if min(g)<4: continue
      paths={}
      rv=solve(p,q,S,RV); av=solve(p,q,S,R,avg_override=lambda c:c[2]); sg=solve(p,q,S,R,sign=-1)
      for ask in (1,2,3):
        d={}
        if len(rv)==1: d['rev']=rv[0][ask-1]
        if len(av)==1: d['avg']=av[0][ask-1]
        if len(sg)==1: d['sign']=sg[0][ask-1]
        if S%3==0: d['S3']=S//3
        for j in (1,2,3):
            if j!=ask: d['grp%d'%j]=g[j-1]
        ok=g[ask-1]
        for combo in combinations(sorted(d),3):
            vals=[d[k] for k in combo]
            if len(set(vals+[ok]))<4: continue
            # prefer strong paths: need at least two of rev/avg/sign/S3
            strong=sum(1 for k in combo if k in ('rev','avg','sign','S3'))
            if strong<2: continue
            pos=sorted(vals+[ok]).index(ok)
            if pos in (0,3):
                out.append((strong,p,q,S,ask,g,{k:d[k] for k in combo},ok,'pos',pos))
out.sort(key=lambda o:-o[0])
seen=set()
for o in out:
    key=o[1:5]
    if key in seen: continue
    seen.add(key); print(o)
    if len(seen)>70: break
print(len(out))
