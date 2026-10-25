# Search parameters for 2-9-1: 甲乙合作原计划N天; 合作a天后甲抽调; 乙单独b天时恰好完成p;
# 丙加入(效率给成 丙=k*乙 或 丙单独T丙天); 丙加入x天后甲返回; 最终提前d天. 求x.
from fractions import Fraction as F
res=[]
for N in range(12,41):
    for a in range(1,10):
        for b in range(1,20):
            for p in [F(1,2),F(2,5),F(3,5),F(1,3),F(2,3),F(3,10)]:
                # a(1+r)+b r = p N (1+r)  -> r (a+b - pN) = pN - a
                den = a+b-p*N
                if den==0: continue
                r = (p*N-a)/den
                if r<=0: continue
                if r.denominator>3 or r.numerator>4: continue
                W = N*(1+r)
                for d in range(1,4):
                    rem_days = N-d-a-b
                    if rem_days<2: continue
                    for c in [F(1,2),F(1),F(3,2),F(2),F(5,2),F(3),F(4),F(2,3),F(4,3),F(5,3)]:
                        # (1-p)W = x(r+c)+(rem_days-x)(1+r+c) -> x = (rem_days*(1+r+c) - (1-p)W)/1
                        x = rem_days*(1+r+c) - (1-p)*W
                        if x.denominator!=1 or x<1 or x>=rem_days: continue
                        res.append((N,a,b,str(p),str(r),str(c),d,int(x),rem_days))
print(len(res))
import random
for t in res:
    N,a,b,p,r,c,d,x,rem=t
    if (r,c) in (('2','3'),): continue
    if x==3: continue
    print(t)
