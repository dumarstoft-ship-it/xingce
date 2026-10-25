from fractions import Fraction as F
def nice(x):
    m = x*60
    return m.denominator==1 and (m % 6 == 0 or m % 5 == 0 or m%4==0)
res=[]
for D in range(20,241,1):
    for t1 in [F(x,4) for x in range(4,40)]:
        for t2 in [F(x,4) for x in range(5,60)]:
            if t2<=t1: continue
            d=F(D)/t1; u=F(D)/t2
            b=(d+u)/2; w=(d-u)/2
            if b.denominator!=1 or w.denominator!=1 or d.denominator!=1 or u.denominator!=1: continue
            if w<=0 or w>5 or b<4*w or b>40: continue
            # boat speed multiplicative
            for p in [F(1,5),F(1,4),F(1,2),F(1,10),F(3,10),F(2,5)]:
                b2=b*(1+p); u2=b2-w
                if b2.denominator!=1: continue
                T=F(D)/u2
                if not nice(T): continue
                errs={'up*(1+p)':F(D)/(u*(1+p)), 'D/b2':F(D)/b2, 't2*(1-p)':t2*(1-p)}
                vals=[T]+list(errs.values())
                if len(set(vals))<len(vals): continue
                if not all(nice(v) for v in errs.values()): continue
                res.append(('boat',D,t1,t2,b,w,p,T,errs))
            # water multiplicative
            for k in [F(2),F(3,2),F(1,2),F(3)]:
                w2=w*k; u2=b-w2
                if u2<=0 or w2.denominator!=1: continue
                T=F(D)/u2
                if not nice(T): continue
                errs={'t2*k':t2*k, 'D/(b-w)':t2, 'wrong w=d-u':(F(D)/(u+ (d-u) - (d-u)*k) if (u+(d-u)-(d-u)*k)>0 else None)}
                if errs['wrong w=d-u'] is None: del errs['wrong w=d-u']
                vals=[T]+list(errs.values())
                if len(set(vals))<len(vals): continue
                if not all(nice(v) for v in errs.values()): continue
                res.append(('water',D,t1,t2,b,w,k,T,errs))
seen=set()
for r in res:
    kind,D,t1,t2,b,w,p,T,errs=r
    key=(kind,t1,t2,p,b/w)
    if key in seen: continue
    seen.add(key)
    print(kind,D,float(t1),float(t2),'b',b,'w',w,'p/k',p,'T',float(T*60),'min |',{k:float(v*60) for k,v in errs.items()})
print(len(res))
