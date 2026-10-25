# Option (a): after fixing the load ratio from two equal-total plans, a mixed fleet of N trucks
# finishes in exactly t3 trips -> how many big trucks.  Look for real-path integer distractors.
from fractions import Fraction as F
from math import gcd
res=[]
for a1 in range(1,9):
 for b1 in range(1,9):
  for t1 in range(2,8):
   for a2 in range(1,9):
    for b2 in range(1,9):
     for t2 in range(2,8):
      if t1==t2 or (a1,b1)==(a2,b2): continue
      X=a1*t1-a2*t2; Y=b2*t2-b1*t1      # X*B = Y*S
      if X<=0 or Y<=0: continue
      g=gcd(X,Y); p,q=Y//g,X//g          # B:S = p:q
      if not p>q or p>9: continue
      W=t1*(a1*p+b1*q)
      # ignore-trips ratio
      Xi=a1-a2; Yi=b2-b1
      ign=None
      if Xi>0 and Yi>0:
          gi=gcd(Xi,Yi); ign=(Yi//gi,Xi//gi)
      for N in range(4,13):
        for t3 in range(2,8):
          R=F(W,t3)
          x=(R-N*q)/(p-q)
          if x.denominator!=1 or not (1<=x<=N-1): continue
          x=int(x)
          # E1 reversed ratio
          W1=t1*(a1*q+b1*p); R1=F(W1,t3)
          x1=(N*p-R1)/(p-q)
          e1=int(x1) if x1.denominator==1 and 0<=x1<=N else None
          # E2 ignore trips (must agree for both plans)
          e2=None
          if ign:
              pi,qi=ign
              if pi!=qi:
                  vals=set()
                  for (aa,bb,tt) in ((a1,b1,t1),(a2,b2,t2)):
                      Wi=tt*(aa*pi+bb*qi); xi=(F(Wi,t3)-N*qi)/(pi-qi)
                      vals.add(xi)
                  if len(vals)==1:
                      xi=vals.pop()
                      if xi.denominator==1 and 0<=xi<=N: e2=int(xi)
          e3=N-x
          d=[v for v in (e1,e2,e3) if v is not None and v!=x]
          if len(set(d))<3: continue
          res.append(((a1,b1,t1),(a2,b2,t2),(p,q),W,N,t3,x,e1,e2,e3))
print(len(res))
for r in res[:80]: print(r)
