from fractions import Fraction as F
import itertools
print("== 39-4-1 workshops: people a:b, per-capita c:d; A per-capita +p ; B people +q ; need B per-capita +r to equal")
nice=[F(1,10),F(1,5),F(1,4),F(3,10),F(2,5),F(1,2),F(3,5),F(4,5),F(3,4),F(1,1)]
res=[]
for a,b in [(3,2),(4,3),(5,4),(5,3),(3,4),(2,3)]:
    for c,d in [(4,5),(5,6),(3,4),(5,4),(6,5),(2,3),(3,2)]:
        for p in [F(1,10),F(1,5),F(1,4),F(3,10),F(1,2)]:
            for q in [F(1,10),F(1,5),F(1,4),F(1,2)]:
                A=a*c*(1+p); B=b*(1+q)*d
                r=A/B-1
                if r>0 and r in nice and r!=p and r!=q:
                    res.append((a,b,c,d,p,q,r, 'base ratio',F(a*c,b*d)))
for x in res: print(x)
