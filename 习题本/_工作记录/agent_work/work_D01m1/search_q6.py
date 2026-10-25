# search numbers for 百分点 trap question
from fractions import Fraction as F
res=[]
for e100 in range(20,46):
    if e100 in (35,40): continue
    for p100 in range(4,16):
        e=F(e100,100); p=F(p100,100)
        med=e+p; old=1-2*e-p
        if old<=F(5,100): continue
        diff=med-old
        if diff<=F(5,100): continue
        med2=e*(1+p); old2=1-e-med2
        diff2=med2-old2
        if diff2<=0: continue
        for T in range(500,5001,100):
            if T in (600,800,1000,1200): continue
            D=diff*T
            if D.denominator!=1 or D%10!=0: continue
            Tm=D/diff2
            if Tm.denominator!=1: continue
            d_old=D/old  # D taken as 养老 share
            d_p=D/p      # D taken as the p points
            cands={'ans':T,'mis':int(Tm)}
            if d_old.denominator==1: cands['old']=int(d_old)
            if d_p.denominator==1: cands['p']=int(d_p)
            if len(cands)<4: continue
            vals=list(cands.values())
            if len(set(vals))<4: continue
            res.append((e100,p100,T,int(D),cands, float(old)))
for r in res: print(r)
print(len(res))
