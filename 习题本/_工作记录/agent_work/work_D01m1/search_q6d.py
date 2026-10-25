from fractions import Fraction as F
res=[]
for e100 in range(20,51):
    if e100 in (35,40,25): continue
    e=F(e100,100)
    for p100 in range(3,21):
        p=F(p100,100)
        for sgn in (1,-1):
            Y=e+sgn*p; Z=1-e-Y
            Ym=e*(1+sgn*p); Zm=1-e-Ym
            if min(Y,Z)<=F(10,100): continue
            for pair in [('Y','Z'),('X','Z'),('Z','X'),('Z','Y')]:
                vals={'X':e,'Y':Y,'Z':Z}; valm={'X':e,'Y':Ym,'Z':Zm}
                d=vals[pair[0]]-vals[pair[1]]; dm=valm[pair[0]]-valm[pair[1]]
                if d<=F(5,100) or dm<=F(2,100): continue
                r=d/dm
                if not (F(1,4)<=r<=F(4)) : continue
                for T in range(500,5001,100):
                    if T in (600,800,1000,1200): continue
                    D=d*T
                    if D.denominator!=1 or D%10!=0: continue
                    Tm=D/dm
                    if Tm.denominator!=1 or Tm%10!=0: continue
                    res.append((e100,sgn*p100,pair,T,int(D),int(Tm),float(Y),float(Z),float(d),float(dm)))
                    break
for r in res: print(r)
print(len(res))
