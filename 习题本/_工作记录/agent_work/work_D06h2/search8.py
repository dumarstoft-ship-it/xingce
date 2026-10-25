from fractions import Fraction as F
from math import comb
res=[]
for a in range(1,7):
  for b in range(1,7):
    if a+b>7 or a+b<4: continue
    for c in range(1,6):
      for d in range(1,6):
        if c+d>6 or c+d<4: continue
        k=2
        n1=a+b; n2=c+d
        # correct
        P=sum(F(comb(a,j)*comb(b,k-j),comb(n1,k))*F(c+j,n2+k) for j in range(0,k+1))
        ign=F(c,n2)
        probs={j:F(comb(a,j)*comb(b,k-j),comb(n1,k)) for j in range(k+1)}
        mx=max(probs.values()); js=[j for j in probs if probs[j]==mx]
        if len(js)!=1: continue
        ml=F(c+js[0],n2+k)
        avg=(F(a,n1)+F(c,n2))/2
        wd=(c+F(k*a,n1))/n2
        opts={'P':P,'ign':ign,'ml':ml,'avg':avg,'wd':wd}
        vals=list(opts.values())
        if len(set(vals))<5: continue
        if P.denominator>60: continue
        res.append((a,b,c,d,P,ign,ml,avg,wd))
for r in res:
    a,b,c,d,P,ign,ml,avg,wd=r
    four=sorted([P,ign,ml,wd])
    pos='ABCD'[four.index(P)]
    print(f'甲{a}+{b} 乙{c}+{d}: P={P}({float(P):.3f}) ign={ign} ml={ml} avg={avg} wd={wd} pos(ign,ml,wd)={pos}')
