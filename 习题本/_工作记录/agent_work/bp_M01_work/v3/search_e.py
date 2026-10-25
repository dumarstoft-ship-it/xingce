from fractions import Fraction as F
import itertools
print("== 15-14-1 capital x months, retained r, given C's share g -> total profit P")
res=[]
for c1,c2,c3 in itertools.permutations([20,30,40,50,60,80],3):
    for m2,m3 in [(9,6),(8,6),(10,6),(9,4),(8,4),(6,3)]:
        w=[c1*12,c2*m2,c3*m3]; W=sum(w)
        for r in [F(1,5),F(1,4),F(3,10),F(2,5)]:
            for P in range(20,200,5):
                dist=P*(1-r)
                shares=[dist*x/W for x in w]
                cap=[dist*c/(c1+c2+c3) for c in (c1,c2,c3)]
                if all(s.denominator==1 for s in shares) and all(c.denominator==1 for c in cap) and len(set(shares))==3:
                    # ask: given P, the share of person with the largest capital
                    res.append(((c1,c2,c3),(12,m2,m3),r,P,[int(s) for s in shares],[int(c) for c in cap], [P*x/W for x in w]))
for x in res[:40]: print(x)
print(len(res))
