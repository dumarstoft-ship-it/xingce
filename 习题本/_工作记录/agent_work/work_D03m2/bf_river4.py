from fractions import Fraction as F
def nice(x):
    m = x*60
    return m.denominator==1 and (m % 6 == 0 or m % 5 == 0)
res=[]
for D in range(12,241,1):
    for t1 in [F(x,4) for x in range(2,40)]:
        for t2 in [F(x,4) for x in range(3,60)]:
            if t2<=t1: continue
            d=F(D)/t1; u=F(D)/t2
            b=(d+u)/2; w=(d-u)/2
            if b.denominator!=1 or w.denominator!=1 or d.denominator!=1 or u.denominator!=1: continue
            if w<=0 or w>6 or b<3*w or b>40: continue
            for b2 in range(int(b)+1, int(b)+16):
                T=F(D)/(b2-w)
                if not nice(T): continue
                errs={'D/b2':F(D)/b2, 'w=d-u':(F(D)/(b2-2*w) if b2>2*w else None), 't2*b/b2':t2*b/b2}
                if errs['w=d-u'] is None: continue
                vals=[T]+list(errs.values())
                if len(set(vals))<len(vals): continue
                if not all(nice(v) for v in errs.values()): continue
                res.append((D,t1,t2,b,w,b2,T,errs))
seen=set()
for r in res:
    D,t1,t2,b,w,b2,T,errs=r
    key=(t1,t2,b/w,b2/b)
    if key in seen: continue
    seen.add(key)
    print(D,float(t1),float(t2),'d',D/t1,'u',D/t2,'b',b,'w',w,'b2',b2,'T',float(T*60),'min |',{k:float(v*60) for k,v in errs.items()})
print(len(res))
