# 2-6-1: N machines D days; after h hours, k machines stop; remaining supplies N-k machines for E days. find h.
from fractions import Fraction as F
res=[]
for N in range(8,31):
  for D in range(3,11):
    for k in range(2,N//2+1):
      for E in range(2,16):
        diff=N*D-(N-k)*E
        if diff<=0: continue
        h=F(24*diff,N)
        if h.denominator!=1 or not (3<=h<=20): continue
        if h==12: continue
        e1=F(diff)            # tai-days taken as hours
        e2=F(24*diff,N-k)     # divided by remaining machines
        e3=F(24*diff,k)       # divided by stopped machines
        vals=[h,e1,e2,e3]
        if len(set(vals))<4: continue
        if not all(v.denominator==1 for v in vals): continue
        if 5 in (D,E) and 20 in (N,): continue
        if D==5 or E==5: continue
        if max(vals)>48: continue
        res.append((N,D,k,E,diff,h,e1,e2,e3))
for r in res: print(r)
