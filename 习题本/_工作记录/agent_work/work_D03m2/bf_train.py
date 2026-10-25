from fractions import Fraction as F
def nice(x):
    return (x*2).denominator==1
res=[]
for v1 in range(80,221,4):
    if v1==180: continue
    for v2 in range(240,351,6):
        if v2<=v1+40: continue
        for L in range(200,441,10):
            for L1 in range(150,421,10):
                if L1==L: continue
                d=F(v2-v1)/F(36,10); s=F(v1+v2)/F(36,10)
                t=F(L)/d
                if t.denominator!=1: continue
                errs={'full':F(L+L1)/d,'sum':F(L)/s,'onlyv2':F(L)/(F(v2)/F(36,10)),'onlyv1':F(L)/(F(v1)/F(36,10))}
                vals=[t]+list(errs.values())
                if len(set(vals))<len(vals): continue
                k=sum(nice(v) for v in errs.values())
                if not nice(errs['full']) or k<3: continue
                res.append((v1,v2,L,L1,t,errs,k))
for r in res[:60]:
    v1,v2,L,L1,t,errs,k=r
    print(v1,v2,L,L1,'t',t,{a:float(b) for a,b in errs.items()},k)
print(len(res))
