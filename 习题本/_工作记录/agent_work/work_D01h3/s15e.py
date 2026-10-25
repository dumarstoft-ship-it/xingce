# Option (b): uneven load ratio; c big + d small trucks; quotient just above an integer -> ceiling trap.
from fractions import Fraction as F
from math import gcd, ceil, floor
res=[]
for a1 in range(1,9):
 for b1 in range(1,9):
  for t1 in range(2,8):
   for a2 in range(1,9):
    for b2 in range(1,9):
     for t2 in range(2,8):
      if t1==t2 or (a1,b1)==(a2,b2): continue
      X=a1*t1-a2*t2; Y=b2*t2-b1*t1
      if X<=0 or Y<=0: continue
      g=gcd(X,Y); p,q=Y//g,X//g
      if not p>q: continue
      if (p,q) in ((2,1),(3,1),(4,1)) or p>9: continue      # avoid too-tidy ratios
      W=t1*(a1*p+b1*q)
      Xi=a1-a2; Yi=b2-b1
      ign=None
      if Xi>0 and Yi>0:
          gi=gcd(Xi,Yi); ign=(Yi//gi,Xi//gi)
      for c in range(1,10):
        for d in range(0,10):
          if (c,d) in ((a1,b1),(a2,b2)) or c+d==0: continue
          cap=c*p+d*q
          Q=F(W,cap)
          if Q.denominator==1: continue
          fr=Q-floor(Q)
          if fr>F(1,5): continue                 # just over an integer: rounding trap
          ans=ceil(Q)
          if not 3<=ans<=9: continue
          fl=floor(Q)
          # reversed ratio
          W1=t1*(a1*q+b1*p); Q1=F(W1,c*q+d*p); e1=ceil(Q1)
          # ignore trips (both plans must agree)
          e2=None
          if ign and ign[0]!=ign[1]:
              pi,qi=ign
              vs={ceil(F(tt*(aa*pi+bb*qi),c*pi+d*qi)) for (aa,bb,tt) in ((a1,b1,t1),(a2,b2,t2))}
              if len(vs)==1: e2=vs.pop()
          ds={fl,e1,e2}
          if None in ds or len(ds)<3 or ans in ds: continue
          if max(ds)>ans+4 or min(ds)<1: continue
          pos=sorted(list(ds)+[ans]).index(ans)
          res.append((pos,(a1,b1,t1),(a2,b2,t2),(p,q),W,(c,d),str(Q),round(float(Q),3),ans,fl,e1,e2))
print(len(res))
res.sort(key=lambda r:(r[0]!=3, r[0]!=0))
for r in res[:60]: print(r)
