from fractions import Fraction as F
res=[]
for e1000 in range(200,460,5):
    if e1000 in (350,400): continue
    for p100 in range(3,21):
        e=F(e1000,1000); p=F(p100,100)
        med=e+p; old=1-2*e-p
        if old<=F(8,100): continue
        diff=med-old
        if diff<=F(8,100): continue
        med2=e*(1+p); old2=1-e-med2
        diff2=med2-old2
        if diff2<=0: continue
        ratio=diff/diff2
        if not (1.3<=ratio<=4): continue
        for T in range(500,6001,50):
            if T in (600,800,1000,1200): continue
            D=diff*T
            if D.denominator!=1 or D%10!=0: continue
            Tm=D/diff2
            if Tm.denominator!=1 or Tm%10!=0: continue
            res.append((float(e),p100,T,int(D),int(Tm), float(med), float(old), float(diff), float(diff2), str(D/old), str(D/p)))
for r in res: print(r)
print(len(res))
