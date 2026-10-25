from math import gcd
from fractions import Fraction as F
def lcm(a,b): return a*b//gcd(a,b)
out=[]
for p in range(2,10):
 for q in range(1,10):
  if gcd(p,q)!=1: continue
  for r in range(1,10):
   for s in range(1,10):
    if gcd(r,s)!=1: continue
    if not F(p,p+q)>F(r,r+s): continue
    L1=lcm(p+q,r+s)
    if L1 in (p+q,r+s): continue
    for u in range(1,10):
     for v in range(1,10):
      if gcd(u,v)!=1: continue
      if not F(v,u)>F(s,r): continue
      A1=r*L1//(r+s)
      sc=u//gcd(A1,u)
      L=L1*sc
      A0=p*L//(p+q); B0=q*L//(p+q); A1=r*L//(r+s); B1=s*L//(r+s); B2=A1*v//u
      dy=B2-B1; dx=A0-A1
      # wrong: step2 keeps total L
      if L%(u+v)!=0: continue
      B2w=v*L//(u+v); dyw=B2w-B1
      if dyw<=0 or dyw==dy: continue
      for k in range(1,40):
        y=dy*k; T0=L*k
        if not(60<=T0<=360 and 4<=y<=40): continue
        kw=F(y,dyw); T0w=L*kw
        if T0w.denominator!=1: continue
        out.append(dict(r1=(p,q),r2=(r,s),r3=(u,v),L=L,k=k,T0=T0,A0=A0*k,B0=B0*k,A1=A1*k,B1=B1*k,B2=B2*k,x=dx*k,y=y,T2=T0+y,T0w=int(T0w)))
print(len(out))
for o in out[:80]: print(o)
