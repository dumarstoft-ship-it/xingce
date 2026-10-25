# brute-force numbers for 3-10-1: given D, down time t1, up time t2; still-water speed raised by p (multiplicative)
from fractions import Fraction as F
def nice(x):
    m = x*60
    return m.denominator==1 and (m % 6 == 0 or m % 5 == 0)
res=[]
for D in range(20,241,2):
    for t1 in [F(x,2) for x in range(2,13)]:
        for t2 in [F(x,2) for x in range(3,19)]:
            if t2<=t1: continue
            d=F(D)/t1; u=F(D)/t2
            b=(d+u)/2; w=(d-u)/2
            if b.denominator!=1 or w.denominator!=1 or d.denominator!=1 or u.denominator!=1: continue
            if w<=0 or w>8 or b>40: continue
            for p in [F(1,5),F(1,4),F(1,2)]:
                b2=b*(1+p); u2=b2-w
                if u2<=0 or b2.denominator!=1: continue
                T=F(D)/u2
                if not nice(T): continue
                errs={'up*(1+p)':F(D)/(u*(1+p)), 'D/b2':F(D)/b2, 't2*(1-p)':t2*(1-p)}
                vals=[T]+list(errs.values())
                if len(set(vals))<len(vals): continue
                if not all(nice(v) for v in errs.values()): continue
                res.append((D,t1,t2,b,w,p,T,errs))
for r in res[:80]:
    D,t1,t2,b,w,p,T,errs=r
    print(D,float(t1),float(t2),'b',b,'w',w,'p',p,'T',float(T*60),'min |',{k:float(v*60) for k,v in errs.items()})
print(len(res))
