from fractions import Fraction as F
from math import gcd
res=[]
seednums={5,9,7,6,3}
for z in range(2,10):
  for l in range(1,z):
    if gcd(z,l)!=1 or (z,l)==(3,2): continue
    for a in range(2,14):
      for b in range(2,16):
        W=z*a+l*b
        for c in range(1,a):
          rem=W-(z+l)*c
          if rem<=0 or rem%l: continue
          d=rem//l
          if d<=0 or d>16: continue
          if {a,b,c,d} & seednums: continue
          Tz=F(W,z); Tl=F(W,l)
          if Tz.denominator!=1: continue
          if d-b<=0 or c+d-b<=0: continue
          z1,l1=d-b,a-c; g=gcd(z1,l1); z1//=g; l1//=g; T1=F(z1*a+l1*b,z1)
          z2,l2=c+d-b,a; g=gcd(z2,l2); z2//=g; l2//=g; T2=F(z2*a+l2*b,z2)
          vals=[Tz,Tl,T1,T2]
          if len(set(vals))<4: continue
          if not (T1.denominator==1 and T2.denominator==1): continue
          if Tl.denominator not in (1,2,5): continue
          if not Tz<min(Tl,T1,T2): continue
          if max(vals)>2.5*Tz: continue
          res.append((z,l,a,b,c,d,W,[str(v) for v in vals]))
for r in res: print(r)
