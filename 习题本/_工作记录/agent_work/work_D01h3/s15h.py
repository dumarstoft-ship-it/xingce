from fractions import Fraction as F
from math import gcd
def intin(v,lo,hi): return v is not None and v.denominator==1 and lo<=v<=hi
out=[]
for a1 in range(1,11):
 for b1 in range(1,11):
  for t1 in range(2,8):
   for a2 in range(1,11):
    for b2 in range(1,11):
     for t2 in range(2,8):
      if t1==t2 or (a1,b1)==(a2,b2): continue
      X=a1*t1-a2*t2; Y=b2*t2-b1*t1
      if X<=0 or Y<=0: continue
      g=gcd(X,Y); p,q=Y//g,X//g
      if not p>q or p>9 or q==1: continue          # uneven ratios only (q>=2)
      W=t1*(a1*p+b1*q)
      if W>200: continue
      for N in range(5,16):
        for t3 in range(2,8):
          if t3 in (t1,t2): continue
          R=F(W,t3)
          x=(R-N*q)/(p-q)
          if not intin(x,1,N-1): continue
          x=int(x)
          W1=t1*(a1*q+b1*p); x1=(N*p-F(W1,t3))/(p-q)
          e1=int(x1) if intin(x1,0,N) else None
          e3=N-x
          x4=(R-N*q)/p; e4=int(x4) if intin(x4,0,N) else None
          ds=[e1,e3,e4]
          if None in ds or len(set(ds))<3 or x in ds: continue
          allv=sorted(ds+[x]); pos=allv.index(x)
          spread=allv[-1]-allv[0]
          out.append((pos,(p,q),s1:=(a1,b1,t1),(a2,b2,t2),W,N,t3,x,{'rev':e1,'small':e3,'div':e4},allv))
seen=set()
for o in sorted(out,key=lambda o:(o[0] not in (0,3),o[1],o[5])):
    key=(o[0],o[1],o[4],o[5],o[6],tuple(o[9]))
    if key in seen: continue
    seen.add(key)
    print(o)
print(len(out))
