from fractions import Fraction as F
import math, itertools
P=print
P('=== 15-4-2 elder care: x self(1:10) y semi(1:5) z dis(1:2); x+y+z=N; x/10+y/5+z/2=C; y-z=d (unique z)')
res=[]
for N in (180,200,240,250,300):
  for d in range(5,80,5):
    sols=[]
    for z in range(2,N,2):
      y=z+d
      if y%5: continue
      x=N-y-z
      if x<=0 or x%10: continue
      C=x//10+y//5+z//2
      sols.append((x,y,z,C))
    # for each C, unique?
    from collections import Counter
    cnt=Counter(s[3] for s in sols)
    for s in sols:
      if cnt[s[3]]==1 and 30<=s[3]<=60 and s[0]>=50 and s[2]>=20:
        res.append((N,d)+s)
for r in res[:25]: P(r)
P('=== 29-3-1 survey: paper p of total, valid fractions vp, vn ; valid count V')
for p in [F(1,4),F(1,3),F(2,5),F(3,8),F(2,7),F(1,5),F(3,7)]:
  for vp in [F(2,3),F(3,4),F(4,5),F(5,6),F(5,8),F(7,8)]:
    for vn in [F(2,3),F(3,4),F(4,5),F(5,6),F(7,8),F(9,10)]:
      if vp==vn: continue
      share=p*vp+(1-p)*vn
      for N in range(200,3001,10):
        if (N*p).denominator==1 and (N*p*vp).denominator==1 and (N*(1-p)*vn).denominator==1:
          V=N*share
          if V.denominator==1 and N in (840,960,1200,1440,1680,2400):
            P('p',p,'vp',vp,'vn',vn,'N',N,'V',V,'paper',N*p,'paper valid',N*p*vp,'net valid',N*(1-p)*vn)
            break
