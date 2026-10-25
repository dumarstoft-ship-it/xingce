from fractions import Fraction as F
def nice(x):
    return (x*2).denominator==1
for v1 in [100,108,120,126,140,144,150,160,200]:
    for v2 in [250,270,288,300,310,324,350]:
        for L in range(200,441,10):
            for L1 in [200,210,220,240,250,280,300,400,420]:
                if L1==L: continue
                d=F(v2-v1)/F(36,10); s=F(v1+v2)/F(36,10)
                t=F(L)/d
                if not nice(t): continue
                errs={'full':F(L+L1)/d,'sum':F(L)/s,'onlyv2':F(L)/(F(v2)/F(36,10)),'onlyv1':F(L)/(F(v1)/F(36,10))}
                vals=[t]+list(errs.values())
                if len(set(vals))<len(vals): continue
                k=sum(nice(v) for v in errs.values())
                if not nice(errs['full']) or k<3: continue
                print(v1,v2,L,L1,'t',float(t),{a:round(float(b),3) for a,b in errs.items()},k)
