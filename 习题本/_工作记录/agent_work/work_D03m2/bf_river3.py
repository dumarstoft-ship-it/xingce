from fractions import Fraction as F
def intmin(x):
    m = x*60
    return m.denominator==1
def nice(x):
    m = x*60
    return m.denominator==1 and (m % 6 == 0 or m % 5 == 0 or m%4==0)
res=[]
for D in range(12,241,1):
    for t1 in [F(x,4) for x in range(2,40)]:
        for t2 in [F(x,4) for x in range(3,60)]:
            if t2<=t1: continue
            d=F(D)/t1; u=F(D)/t2
            b=(d+u)/2; w=(d-u)/2
            if b.denominator!=1 or w.denominator!=1 or d.denominator!=1 or u.denominator!=1: continue
            if w<=0 or w>6 or b<3*w or b>40: continue
            for p in [F(1,5),F(1,4),F(1,2),F(1,10),F(3,10),F(2,5),F(1,3)]:
                b2=b*(1+p); u2=b2-w
                if b2.denominator!=1: continue
                T=F(D)/u2
                if not nice(T): continue
                errs={'up*(1+p)':F(D)/(u*(1+p)), 'D/b2':F(D)/b2, 't2*(1-p)':t2*(1-p), 't2/(1+p) same as up*(1+p)':None}
                del errs['t2/(1+p) same as up*(1+p)']
                vals=[T]+list(errs.values())
                if len(set(vals))<len(vals): continue
                if not all(intmin(v) for v in errs.values()): continue
                res.append(('boat',D,t1,t2,b,w,p,T,errs))
seen=set()
for r in res:
    kind,D,t1,t2,b,w,p,T,errs=r
    key=(kind,t1,t2,p,b/w)
    if key in seen: continue
    seen.add(key)
    print(kind,D,float(t1),float(t2),'d',D/t1,'u',D/t2,'b',b,'w',w,'p',p,'T',float(T*60),'min |',{k:float(v*60) for k,v in errs.items()})
print(len(res))
