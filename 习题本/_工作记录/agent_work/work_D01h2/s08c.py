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
      dx=A0-A1
      sc=u//gcd(A1,u)
      # true: in scaled parts
      A1s=A1*sc; B1s=B1*sc; B2s=A1s*v//u; dys=B2s-B1s
      for k1 in range(1,20):        # value of one step-1 part
        x=dx*k1
        if k1%sc: continue          # need integer people in scaled parts
        k2=F(k1,sc)
        y=dys*k2
        T0=L1*k1
        if not (60<=T0<=300 and 4<=x<=30 and 4<=y<=40): continue
        # E1: step2 total const with step-1 parts
        B2w=F(v*L1,u+v); yw=(B2w-B1)*k1
        # no-rescale error: use k1 as value of scaled part
        yns=dys*k1 if sc>1 else None
        out.append(dict(r=(p,q,r,s,u,v),L1=L1,sc=sc,k1=k1,T0=T0,A0=A0*k1,B0=B0*k1,A1=A1*k1,B1=B1*k1,B2=int(B2s*k2),x=x,y=int(y),yw=yw,yns=yns,xy=int(x+y)))
good=[o for o in out if o['sc']>1 and o['yw'].denominator==1 and o['yw']>0 and len({o['y'],int(o['yw']),o['yns'],o['xy']})==4]
print(len(out),len(good))
for o in good[:60]: print(o)
