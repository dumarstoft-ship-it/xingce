from fractions import Fraction as F
import itertools
fr = [F(1,3),F(1,4),F(1,5),F(1,6),F(2,5),F(3,8),F(2,7),F(3,10),F(1,2),F(2,3),F(3,4),F(3,5),F(1,8),F(1,10),F(1,7)]
def isint(x): return x is not None and x.denominator==1 and x>0
res=[]
for r1,r2 in itertools.product(fr,fr):
    if r1==r2: continue
    if r2 <= r1: continue   # non-reserved more likely to need supplements
    for Y in range(20,91):
        M = F(Y)/(1-r2)
        if not isint(M): continue
        Bo = r2*M
        if not isint(Bo): continue
        for X in range(4,41):
            A = (Bo+X)/(1-r1)
            if not isint(A): continue
            if not isint(r1*A): continue
            N = A+M
            if not (80<=N<=200): continue
            # error paths
            errs={}
            # E1: r2 of total
            # (1-r2)N - A = Y ; r2 N = (1-r1)A - X
            # N = ((1-r1)A - X)/r2 ; (1-r2)((1-r1)A-X)/r2 - A = Y
            coefA = (1-r2)*(1-r1)/r2 - 1
            if coefA != 0:
                A1 = (Y + (1-r2)*X/r2)/coefA
                N1 = ((1-r1)*A1 - X)/r2
                if isint(N1) and isint(A1) and isint(r1*A1) and isint(r2*N1): errs['E1']=N1
            # E2: neither treated as non-A count
            Bo2 = r2*Y
            A2 = (Bo2+X)/(1-r1)
            N2 = A2+Y
            if isint(Bo2) and isint(A2) and isint(N2): errs['E2']=N2
            # E3: B only non-A row
            A3 = Bo+X; N3=A3+M
            errs['E3']=N3
            # E5: base reversed in A row: AB = r1*B ; B = AB + Bo -> B = Bo/(1-r1)
            B5 = Bo/(1-r1)
            if isint(B5) and isint(r1*B5):
                A5 = B5+X; N5=A5+M
                errs['E5']=N5
            # E6: total = A + neither (forget B-only)
            errs['E6']=A+Y
            vals=[v for k,v in errs.items()]
            distinct=set(vals)-{N}
            if len(distinct)>=3:
                res.append((r1,r2,Y,X,int(A),int(M),int(N),{k:int(v) for k,v in errs.items()}))
print(len(res))
import random
random.seed(1)
for r in res:
    if 'E2' in r[7] and 'E5' in r[7] and len(set(r[7].values())|{r[6]})==len(r[7])+1:
        print(r)
