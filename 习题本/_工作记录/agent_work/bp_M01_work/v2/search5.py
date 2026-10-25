from fractions import Fraction as F
import math, itertools
P=print
P('=== 39-8-2 five sessions: s2=s1(1+a); s2=s3(1-b); s4+s5 = k*(s1+s2+s3); s5 = s4*(1+c); s5 - s3 = D ; ask s4 - s1 (range opts)')
cnt=0
for a,b in [(F(1,4),F(1,5)),(F(1,5),F(1,6)),(F(1,2),F(1,4)),(F(1,4),F(1,6)),(F(1,3),F(1,5)),(F(2,5),F(1,8)),(F(1,5),F(1,5)),(F(3,5),F(1,5))]:
  for k in [2,F(3,2),3]:
    for c in [F(1,4),F(1,5),F(1,3),F(1,2),F(1,10),F(1,8)]:
      s3=F(1); s2=s3*(1-b); s1=s2/(1+a); front=s1+s2+s3; back=k*front; s4=back/(2+c); s5=s4*(1+c)
      D=s5-s3
      if D<=0: continue
      for Dv in [36,40,45,48,50,54,60,64,72,80,90,96,100,120]:
        t=F(Dv)/D
        vals=[x*t for x in [s1,s2,s3,s4,s5]]
        if all(v.denominator==1 for v in vals) and 20<=vals[0]<=200 and cnt<25:
          P('a',a,'b',b,'k',k,'c',c,'sessions',[int(v) for v in vals],'s5-s3',Dv,'ask s4-s1',vals[3]-vals[0]); cnt+=1
          break
P('=== 39-9-1 two goods: plan1 (m1 milk, e1 eggs per home): milk left - eggs left = rd ; plan2 (m2,e2): short sm milk, se eggs ; then ratio rm:re per home, no leftover -> min purchase')
for (m1,e1,rd) in [(6,4,18),(6,4,20),(5,3,16),(8,5,15),(6,3,24),(5,2,21),(4,3,10)]:
  for (m2,e2,sm,se) in [(8,5,6,3),(8,5,5,4),(7,5,10,8),(9,6,8,2),(10,6,7,9),(7,4,9,3),(6,4,4,6),(8,6,10,4)]:
    for n in range(8,60):
        M=m2*n-sm; E=e2*n-se
        if M-m1*n-(E-e1*n)==rd and M>0 and E>0:
            for (rm,re) in [(3,2),(2,1),(5,3),(4,3)]:
                best=None
                for kk in range(1,100):
                    if rm*kk*n>=M and re*kk*n>=E:
                        best=(rm*kk*n-M+re*kk*n-E,kk,rm*kk,re*kk); break
                P('plan1',m1,e1,rd,'plan2',m2,e2,sm,se,'n',n,'M,E',M,E,'ratio',rm,re,'best(buy,k,per milk,per egg)',best)
