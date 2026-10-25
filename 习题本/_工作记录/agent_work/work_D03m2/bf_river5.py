from fractions import Fraction as F
def nice(x):
    m = x*60
    return m.denominator==1 and (m % 6 == 0 or m % 5 == 0)
res=[]
for D in range(30,201,1):
    for t1 in [F(x,4) for x in range(4,40)]:
        for t2 in [F(x,4) for x in range(5,60)]:
            if t2<=t1: continue
            d=F(D)/t1; u=F(D)/t2
            b=(d+u)/2; w=(d-u)/2
            if b.denominator!=1 or w.denominator!=1 or d.denominator!=1 or u.denominator!=1: continue
            if not (2<=w<=6 and 15<=b<=35): continue
            for b2 in range(int(b)+1, int(b)+16):
                T=F(D)/(b2-w)
                if not nice(T): continue
                errs={'D/b2':F(D)/b2, 'w=d-u':F(D)/(b2-2*w), 't2*b/b2':t2*b/b2, 'D/(b2-w)+?':None}
                del errs['D/(b2-w)+?']
                vals=[T]+list(errs.values())
                if len(set(vals))<len(vals): continue
                ok=sum(nice(v) for v in errs.values())
                if ok<2: continue
                res.append((D,t1,t2,b,w,b2,T,errs,ok))
for r in res:
    D,t1,t2,b,w,b2,T,errs,ok=r
    print(D,float(t1),float(t2),'d',D/t1,'u',D/t2,'b',b,'w',w,'b2',b2,'T',float(T*60),'min |',{k:round(float(v*60),2) for k,v in errs.items()}, ok)
print(len(res))
