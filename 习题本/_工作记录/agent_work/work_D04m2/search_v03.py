from fractions import Fraction as F
def nice(x):  # multiple of 0.05 within (0,1)
    return 0 < x < 1 and (x*20).denominator == 1
res=[]
for c in range(4,13):
    for p in range(c+2, 2*c+3):
        for a in [F(1,2),F(3,5),F(7,10),F(3,4),F(4,5)]:
            for r in [F(1,5),F(1,4),F(3,10)]:
                d=((1+r)*c-a*p)/((1-a)*p)
                d1=(1+r)*c/p            # only remainder reaches r
                d2=F(c,p)               # remainder breakeven
                d3=(F(c)/(1-r)-a*p)/((1-a)*p)  # sales margin
                d4=((1+r)*c-(1-a)*p)/(a*p)     # weights reversed
                d5=(c+r*p-a*p)/((1-a)*p)       # base = list price
                if not nice(d): continue
                errs={'d1':d1,'d2':d2,'d3':d3,'d4':d4,'d5':d5}
                ok={k:v for k,v in errs.items() if nice(v) and v!=d}
                if len(set(ok.values()))>=3 and d<d2:
                    res.append((c,p,float(a),float(r),float(d),{k:float(v) for k,v in ok.items()}))
for x in res: print(x)
