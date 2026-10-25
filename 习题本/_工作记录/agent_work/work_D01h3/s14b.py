from math import gcd
from fractions import Fraction as F
pairs=[(60,40),(75,50),(90,60),(45,30),(80,40),(60,30),(90,45),(100,25),(80,60),(100,60),(120,80),(50,30),(100,40),(70,30),(120,40),(150,100)]
res=[]
for pA,pB in pairs:
    g=gcd(pA,pB); u,v=pB//g,pA//g
    hm=F(2*pA*u,u+v); e1=F(pA*v+pB*u,u+v); e4=F(pA+pB,2)
    for pC in range(20,160,5):
        if pC in (pA,pB): continue
        for N in range(100,401,10):
            for R in range(2000,40001,100):
                avg=F(R,N)
                # correct
                if not (min(hm,pC)<avg<max(hm,pC)): continue
                nAB=F(N)*(avg-pC)/(hm-pC)   # tickets of A+B
                if nAB.denominator!=1 or nAB%(u+v): continue
                nAB=int(nAB); t=nAB//(u+v); nA,nB=u*t,v*t; nC=N-nAB
                # E1
                if not (min(e1,pC)<avg<max(e1,pC)): continue
                n1=F(N)*(avg-pC)/(e1-pC)
                if n1.denominator!=1 or n1%(u+v): continue
                nC1=N-int(n1)
                # E4 equal counts
                n4=F(N)*(avg-pC)/(e4-pC) if e4!=pC else None
                nC4=None
                if n4 is not None and min(e4,pC)<avg<max(e4,pC) and n4.denominator==1 and n4%2==0: nC4=N-int(n4)
                pk=F(nC,u+v)
                res.append((pA,pB,pC,N,R,u,v,hm,nA,nB,nC,nC1,nC4,pk))
print(len(res))
for r in res:
    pA,pB,pC,N,R,u,v,hm,nA,nB,nC,nC1,nC4,pk=r
    if hm.denominator==1 and pk.denominator==1 and N%50==0 and R%200==0:
        print(f"pA={pA} pB={pB} pC={pC} N={N} R={R} u:v={u}:{v} hm={hm} nA={nA} nB={nB} nC={nC} | E1={nC1} E4={nC4} pkg={pk}")
