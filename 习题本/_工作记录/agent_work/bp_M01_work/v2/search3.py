from fractions import Fraction as F
import math, itertools
from collections import Counter
P=print
P('=== 29-9-1: T=a n + r1 ; (1+u) T = b n + r2 ; then shops + m, everyone >= c bottles -> min extra % (integer %)')
c=0
for a in (5,6):
  for r1 in range(10,61,2):
    for u in (F(1,5),F(1,4),F(3,10),F(2,5)):
      for b in (6,7,8):
        if b<=a: continue
        for r2 in range(0,40,2):
          # (1+u)(a n + r1) = b n + r2 -> n((1+u)a - b) = r2 - (1+u) r1
          den=(1+u)*a-b
          if den==0: continue
          n=(r2-(1+u)*r1)/den
          if n<=10 or n.denominator!=1 or n>80: continue
          T=a*n+r1
          if ((1+u)*T).denominator!=1: continue
          if c<20: P('a',a,'r1',r1,'u',u,'b',b,'r2',r2,'n',n,'T',T,'T2',(1+u)*T); c+=1
P('=== 29-12-1 servers: x+y+z=N ; P=pa x+pb y+pc z ; next: drop A, B*(1+fb), C*(1+fc), same P ; unique z given N,P')
res=[]
for pa,pb,pc in [(1,2,4),(1,2,5),(1,3,5),(2,3,5),(1,3,4),(2,3,6),(1,2,3)]:
  for fb,fc in [(F(1,2),F(1,2)),(F(1,2),F(1,4)),(F(1,4),F(1,2)),(F(1,3),F(1,2)),(F(1,2),F(1,5)),(F(1,5),F(1,2)),(F(1,4),F(1,4))]:
    for N in range(100,301,20):
      sols=[]
      for z in range(1,N):
        for y in range(1,N-z):
          x=N-y-z
          if x<1: continue
          P1=x*pa+y*pb+z*pc
          P2=(1+fb)*y*pb+(1+fc)*z*pc
          if P1==P2 and ((1+fb)*y).denominator==1 and ((1+fc)*z).denominator==1:
            sols.append((x,y,z,P1))
      cnt=Counter(s[3] for s in sols)
      for s in sols:
        if cnt[s[3]]==1 and min(s[:3])>=20:
          res.append((pa,pb,pc,str(fb),str(fc),N)+s)
for r in res[:30]: P(r)
