from fractions import Fraction as F
from math import gcd
res=[]
def intin(v,lo,hi):
    return v is not None and v.denominator==1 and lo<=v<=hi
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
      if not p>q or p>9: continue
      W=t1*(a1*p+b1*q)
      Xi=a1-a2; Yi=b2-b1
      ign=None
      if Xi>0 and Yi>0 and Xi!=Yi:
          gi=gcd(Xi,Yi); ign=(Yi//gi,Xi//gi)
      for N in range(5,13):
        for t3 in range(2,8):
          if t3 in (t1,t2): continue
          R=F(W,t3)
          x=(R-N*q)/(p-q)
          if not intin(x,1,N-1): continue
          x=int(x)
          W1=t1*(a1*q+b1*p); x1=(N*p-F(W1,t3))/(p-q)          # reversed ratio
          e1=int(x1) if intin(x1,0,N) else None
          e2=None
          if ign:
              pi,qi=ign
              vs=set()
              for (aa,bb,tt) in ((a1,b1,t1),(a2,b2,t2)):
                  vs.add((F(tt*(aa*pi+bb*qi),t3)-N*qi)/(pi-qi))
              if len(vs)==1:
                  v=vs.pop()
                  if intin(v,0,N): e2=int(v)
          e3=N-x                                               # answered small count
          x4=(R-N*q)/p                                         # wrong divisor in 鸡兔同笼
          e4=int(x4) if intin(x4,0,N) else None
          ds=set(v for v in (e1,e2,e3,e4) if v is not None and v!=x)
          if len(ds)<3: continue
          res.append(((a1,b1,t1),(a2,b2,t2),(p,q),W,N,t3,x,{'rev':e1,'ign':e2,'small':e3,'div':e4}))
print(len(res))
for r in res:
    (p,q)=r[2]
    if (p,q)!=(2,1):
        print(r)
