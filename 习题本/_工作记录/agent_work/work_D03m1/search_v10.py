from fractions import Fraction as F
res=[]
for u in range(4,25):
  for d in range(u+2,40):
    if (u+d)%2: continue
    f=(u+d)//2
    if f in (9,12) and (u,d) in ((6,18),): continue
    H=F(2*u*d,u+d)
    for a2 in range(1,41):      # a in 0.5 km
      a=F(a2,2)
      for b2 in range(1,21):
        b=F(b2,2)
        T1=(a/f+b/u)*60; T2=(a/f+b/d)*60
        if T1.denominator!=1 or T2.denominator!=1: continue
        D=a+b
        Derr=F(f)*(T1+T2)/60/2      # arithmetic-mean shortcut error
        Dh=H*(T1+T2)/60/2            # harmonic shortcut misapplied
        if D.denominator!=1: continue
        if Derr.denominator>2: continue
        if Derr==D: continue
        res.append((u,d,f,float(a),float(b),int(T1),int(T2),float(D),float(Derr),float(Dh)))
for r in res:
    u,d,f,a,b,T1,T2,D,Derr,Dh=r
    if T1<=60 and T2>=15 and (u,d,f)!=(6,18,12) and a>=2 and b>=1.5:
        print(r)
