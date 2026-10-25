from fractions import Fraction as F
res=[]
for e100 in range(20,46):
    if e100 in (35,40): continue
    for p100 in range(4,21):
        e=F(e100,100); p=F(p100,100)
        med=e+p; old=1-2*e-p
        if old<=F(8,100): continue
        diff=med-old
        if diff<=F(8,100): continue
        med2=e*(1+p); old2=1-e-med2
        diff2=med2-old2
        if diff2<=F(2,100): continue
        for T in range(500,6001,100):
            if T in (600,800,1000,1200): continue
            D=diff*T
            if D.denominator!=1 or D%10!=0: continue
            Tm=D/diff2
            if Tm.denominator!=1 or Tm%10!=0: continue
            res.append((e100,p100,T,int(D),int(Tm), float(old), float(diff), float(diff2), D/old, D/p))
for r in res: print(r[:8], [str(x) for x in r[8:]])
print(len(res))
