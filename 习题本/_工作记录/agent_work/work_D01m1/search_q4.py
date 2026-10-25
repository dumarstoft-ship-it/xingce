from fractions import Fraction as F
rs=[F(6,5),F(5,4),F(3,2),F(2),F(5,2),F(4,3)]
ps=[F(1,5),F(1,4),F(3,10),F(2,5),F(1,2),F(3,5),F(3,4)]
qs=[F(1,5),F(1,4),F(3,10),F(2,5),F(1,2),F(3,5)]
ms=[20,30,40,50,60,80,100,120]
ks=[F(3,2),F(2),F(3)]
bad={1450,1500,1550,1600,1260,100}
out=[]
for r in rs:
  for p in ps:
    for q in qs:
      if p==q: continue
      for m in ms:
        for k in ks:
          den=k*(1-q)-r*(1-p)
          if den<=0: continue
          b=m*(k-1)/den
          if b.denominator!=1: continue
          R=r*b
          if R.denominator!=1: continue
          L1=R*(1-p); B1=b*(1-q)
          if L1.denominator!=1 or B1.denominator!=1: continue
          if B1-m<=0 or L1-m<=0: continue
          tot=R+b
          if tot in bad: continue
          # misread p as remaining
          den2=k*(1-q)-r*p
          mis=None
          if den2>0:
            b2=m*(k-1)/den2
            if b2.denominator==1 and (r*b2).denominator==1 and b2*(1-q)-m>0 and r*b2*p-m>0:
              mis=(1+r)*b2
          if mis is None: continue
          if mis in (tot,R,b): continue
          out.append((float(r),float(p),float(q),m,float(k),int(b),int(R),int(tot),int(mis),int(B1-m),int(L1-m)))
for o in out: print(o)
print(len(out))
