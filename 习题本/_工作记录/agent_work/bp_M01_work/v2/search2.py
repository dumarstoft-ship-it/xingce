from fractions import Fraction as F
import math, itertools
from collections import Counter
P=print
P('=== 29-7-1 two units: first round p1,p2 of totals (diff d: jia_out - yi_out = d), second q1,q2 of remaining, sum tr')
c=0
for p1,p2 in [(F(1,3),F(1,4)),(F(2,5),F(1,3)),(F(1,2),F(1,3)),(F(1,4),F(1,5)),(F(2,3),F(1,2)),(F(3,5),F(1,2)),(F(1,3),F(1,2))]:
  for q1,q2 in [(F(1,2),F(1,3)),(F(1,3),F(1,2)),(F(1,4),F(1,3)),(F(1,2),F(1,4)),(F(2,3),F(1,2)),(F(1,2),F(2,3)),(F(3,4),F(1,2))]:
    for x in range(30,160,6):
      for y in range(30,160,6):
        o1=p1*x; o2=p2*y; s1=q1*(x-o1); s2=q2*(y-o2)
        if all(v.denominator==1 for v in (o1,o2,s1,s2)) and o1-o2 in (2,3,4,5,6) and 20<=s1+s2<=60 and x!=y:
          # uniqueness: two linear eq in x,y
          A=[[p1,-p2],[q1*(1-p1),q2*(1-p2)]]
          det=A[0][0]*A[1][1]-A[0][1]*A[1][0]
          if det!=0 and c<14:
            P('p',p1,p2,'q',q1,q2,'x,y',x,y,'out',o1,o2,'d',o1-o2,'second',s1,s2,'tr',s1+s2,'x-y',x-y); c+=1
P('=== 29-8-1 three firms (2024->2025): A up dA (wan), B down pB and B25 = A25/2, C up qC and C24 = A24+B24 ; total up g')
res=[]
for g in [F(1,5),F(1,4),F(3,10),F(3,20)]:
  for dA in [100,200,300,400,600]:
    for pB in [F(1,10),F(1,5),F(1,4)]:
      for qC in [F(1,5),F(1,4),F(3,10),F(2,5),F(1,2)]:
        # unknown A24=a ; A25=a+dA ; B25=(a+dA)/2 ; B24 = B25/(1-pB) ; C24=a+B24 ; C25=C24*(1+qC)
        # total25 = (1+g) total24 -> linear in a
        a=F(1); # solve linear: f(a) = A25+B25+C25-(1+g)(A24+B24+C24)=0
        def f(a):
            A25=a+dA; B25=A25/2; B24=B25/(1-pB); C24=a+B24; C25=C24*(1+qC)
            return A25+B25+C25-(1+g)*(a+B24+C24)
        f0=f(F(0)); f1=f(F(1)); slope=f1-f0
        if slope==0: continue
        a=-f0/slope
        if a<=0 or a.denominator!=1: continue
        A25=a+dA; B25=A25/2; B24=B25/(1-pB); C24=a+B24; C25=C24*(1+qC)
        if all(v.denominator==1 and v>0 for v in (A25,B25,B24,C24,C25)) and a<5000:
            res.append((str(g),dA,str(pB),str(qC),'A24',a,'B24',B24,'C24',C24,'A25',A25,'B25',B25,'C25',C25,'C share25',C25/(A25+B25+C25)))
for r in res[:20]: P(r)
