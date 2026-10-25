from fractions import Fraction as F
rs=[F(6,5),F(5,4),F(3,2),F(2),F(5,2),F(4,3),F(7,4),F(8,5),F(9,5),F(3)]
ps=[F(1,5),F(1,4),F(3,10),F(1,2),F(7,10),F(3,4),F(4,5),F(1,3),F(2,3)]
qs=[F(1,5),F(1,4),F(3,10),F(1,2),F(1,3),F(2,3),F(3,4),F(7,10)]
ms=[20,24,25,30,36,40,45,48,50,60,70,75,80,90,120]
ks=[F(3,2),F(2),F(5,2),F(3),F(4)]
bad={1450,1500,1550,1600,1260,100,1000,1200,600,800}
out=[]
for r in rs:
  for p in ps:
    for q in qs:
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
          if B1-m<20 or L1-m<20: continue
          tot=R+b
          if tot in bad or tot>3000: continue
          den2=k*(1-q)-r*p
          mis=None
          if den2>0 and p!=F(1,2):
            b2=m*(k-1)/den2
            if b2.denominator==1 and (r*b2).denominator==1 and (b2*(1-q)).denominator==1 and b2*(1-q)-m>0 and r*b2*p-m>0:
              mis=(1+r)*b2
          if mis is None: continue
          if mis in (tot,R,b): continue
          out.append((float(r),float(p),float(q),m,float(k),int(b),int(R),int(tot),int(mis),int(L1),int(B1),int(L1-m),int(B1-m)))
for o in out: print(o)
print(len(out))
