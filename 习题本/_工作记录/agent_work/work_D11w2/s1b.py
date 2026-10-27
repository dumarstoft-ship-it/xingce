from fractions import Fraction as F
import itertools
def isint(x): return x is not None and x.denominator==1 and x>0
pairs=[(F(1,5),F(1,3)),(F(1,6),F(2,5)),(F(1,5),F(2,5)),(F(1,4),F(2,5)),(F(1,3),F(2,5)),(F(1,6),F(1,3)),(F(1,5),F(1,2)),(F(1,4),F(1,2)),(F(1,6),F(1,4)),(F(1,8),F(1,4)),(F(1,5),F(3,8)),(F(1,4),F(3,7)),(F(2,7),F(1,2)),(F(1,7),F(1,3)),(F(1,9),F(1,3))]
for r1,r2 in pairs:
    for Y in range(18,91):
        M = F(Y)/(1-r2)
        if not isint(M): continue
        Bo = r2*M
        if not isint(Bo): continue
        for X in range(4,41):
            A = (Bo+X)/(1-r1)
            if not isint(A) or not isint(r1*A): continue
            N = A+M
            if not (80<=N<=180): continue
            e={}
            coefA = (1-r2)*(1-r1)/r2 - 1
            if coefA != 0:
                A1 = (Y + (1-r2)*X/r2)/coefA
                N1 = ((1-r1)*A1 - X)/r2
                if isint(N1) and isint(A1) and isint(r1*A1) and isint(r2*N1) and N1>A1: e['E1']=int(N1)
            Bo2=r2*Y; A2=(Bo2+X)/(1-r1)
            if isint(Bo2) and isint(A2) and isint(r1*A2): 
                e['E2']=int(A2+Y)
                e['E4']=int(A2+Y+Bo2)
            e['E3']=int(Bo+X+M)
            vals=list(e.values())
            if len(set(vals))==len(vals) and N not in vals and len(vals)>=4:
                print(r1,r2,'Y',Y,'X',X,'A',A,'M',M,'Bo',Bo,'AB',r1*A,'N',N,e)
