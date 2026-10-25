# search params for 2-4-1: scenario1: z*a + l*b = W ; scenario2: (z+l)*c + l*d = W ; ask W/z
from fractions import Fraction as F
from math import gcd
res=[]
for z in range(2,8):
  for l in range(1,z):
    if gcd(z,l)!=1: continue
    if (z,l)==(3,2): continue
    for a in range(3,10):
      for b in range(3,12):
        W=z*a+l*b
        for c in range(1,a):
          # (z+l)c + l d = W -> d
          rem=W-(z+l)*c
          if rem<=0 or rem%l: continue
          d=rem//l
          if d<=0 or d>15: continue
          Tz=F(W,z); Tl=F(W,l)
          if Tz.denominator!=1: continue
          # error1: forgot l's part in c days: z*a + l*b = z*c + l*d  -> (a-c) z' = (d-b) l'
          if d-b<=0: continue
          z1,l1=d-b,a-c
          g=gcd(z1,l1); z1//=g; l1//=g
          W1=z1*a+l1*b; T1=F(W1,z1)
          # error2: forgot z's part in c days: z*a + l*b = l*c + l*d -> a z = (c+d-b) l
          if c+d-b<=0: continue
          z2,l2=c+d-b,a
          g=gcd(z2,l2); z2//=g; l2//=g
          W2=z2*a+l2*b; T2=F(W2,z2)
          vals={Tz,Tl,T1,T2}
          if len(vals)<4: continue
          if not all(v.denominator==1 for v in (T1,T2)): continue
          if not (Tz<min(Tl,T1,T2)): continue
          if max(Tl,T1,T2)>2*Tz: continue
          # avoid seed numbers 5,9,7,6,3 pattern
          if (a,b)==(5,9) or (a,b)==(7,6): continue
          res.append((z,l,a,b,c,d,W,Tz,Tl,T1,T2))
for r in res[:80]:
    print(r)
print(len(res))
