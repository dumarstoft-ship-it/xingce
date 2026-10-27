from fractions import Fraction as F
from math import gcd
def isint(x): return x.denominator==1 and x>0
pairs=[(F(1,4),F(2,5)),(F(1,6),F(2,5)),(F(1,5),F(1,3)),(F(1,5),F(3,8)),(F(1,6),F(3,8)),(F(1,3),F(2,5)),(F(1,8),F(1,3)),(F(1,8),F(2,5)),(F(1,5),F(3,7)),(F(1,6),F(3,7)),(F(1,4),F(3,7)),(F(1,9),F(2,5)),(F(1,7),F(2,5)),(F(1,6),F(2,7)),(F(2,9),F(2,5))]
for r1,r2 in pairs:
    if gcd(r1.denominator, r2.denominator)!=1: continue
    for Y in range(20,91):
        M=F(Y)/(1-r2)
        if not isint(M) or not isint(r2*M): continue
        Bo=r2*M
        for X in range(4,31):
            A=(Bo+X)/(1-r1)
            if not isint(A) or not isint(r1*A): continue
            N=A+M
            if not (90<=N<=150): continue
            Bo2=r2*Y; A2=(Bo2+X)/(1-r1)
            if not (isint(Bo2) and isint(A2) and isint(r1*A2)): continue
            e2=A2+Y; e4=A2+Y+Bo2; e3=Bo+X+M
            v=[int(N),int(e2),int(e4),int(e3)]
            if len(set(v))<4: continue
            if min(abs(a-b) for i,a in enumerate(v) for b in v[i+1:])<6: continue
            print(r1,r2,'Y',Y,'X',X,'A',A,'AB',r1*A,'M',M,'Bo',Bo,'N',N,'E2',e2,'E4',e4,'E3',e3)
