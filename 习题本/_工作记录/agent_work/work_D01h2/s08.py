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
      A0=p*L1//(p+q); B0=q*L1//(p+q); A1=r*L1//(r+s); B1=s*L1//(r+s)
      # scale so that A1 divisible by u
      sc=u//gcd(A1,u)
      A0s,B0s,A1s,B1s=A0*sc,B0*sc,A1*sc,B1*sc
      B2s=A1s*v//u
      xs=A0s-A1s; ys=B2s-B1s
      for k in range(1,30):
        T0=(A0s+B0s)*k; x=xs*k; y=ys*k
        if not (60<=T0<=300 and 3<=x<=40 and 3<=y<=40): continue
        out.append((p,q,r,s,u,v,L1,sc,k,T0,A0s*k,B0s*k,A1s*k,B1s*k,B2s*k,x,y))
print(len(out))
import random
random.seed(3)
for o in random.sample(out,60): print(o)
