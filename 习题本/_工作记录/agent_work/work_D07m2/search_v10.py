# search clean data for the orchard question: a (opp c), b (opp x); x = a*c/b
from fractions import Fraction as F
from itertools import permutations, product
prices = [F(4,10),F(5,10),F(6,10),F(8,10),F(9,10),F(1),F(12,10),F(15,10)]
res=[]
for a in range(6,31):
  for b in range(6,31):
    for c in range(6,31):
      if len({a,b,c})<3: continue
      if (a*c)%b: continue
      x=a*c//b
      if x>40 or x in (a,b,c): continue
      m1=F(a*b,c); m2=F(b*c,a)
      if m1.denominator!=1 or m2.denominator!=1: continue
      if len({x,int(m1),int(m2)})<3: continue
      for pa,pb,pc,px in permutations(prices,4):
        T=a*pa+b*pb+c*pc+x*px
        T1=a*pa+b*pb+c*pc+m1*px
        T2=a*pa+b*pb+c*pc+m2*px
        avg=(pa+pb+pc+px)/4*(a+b+c+x)
        vals=[T,T1,T2,avg]
        if any((v*10).denominator!=1 for v in vals): continue
        if len(set(vals))<4: continue
        # want correct is max among options (b smallest => x largest) and avg < T
        if not (T>T1 and T>T2 and T>avg): continue
        # spacing: options differ by at least 8%
        s=sorted(vals)
        if any((s[i+1]-s[i])/s[i] < F(8,100) for i in range(3)): continue
        res.append((a,b,c,x,int(m1),int(m2),pa,pb,pc,px,T,T1,T2,avg))
print(len(res))
import random
random.seed(1)
# prefer small integers and totals integer
good=[r for r in res if r[10].denominator==1]
print('integer totals',len(good))
for r in sorted(good,key=lambda r:(r[0]+r[1]+r[2], r[10]))[:60]:
  a,b,c,x,m1,m2,pa,pb,pc,px,T,T1,T2,avg=r
  print(a,b,c,'x=',x,'mis',m1,m2,'p',float(pa),float(pb),float(pc),float(px),'T',float(T),'T1',float(T1),'T2',float(T2),'avg',float(avg))
