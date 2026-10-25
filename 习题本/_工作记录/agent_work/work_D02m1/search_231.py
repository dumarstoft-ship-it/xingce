# 2-3-1: jia alone A days, together T days; jia first a days, then together x, then yi alone y; total D days (date span)
from fractions import Fraction as F
from math import lcm
res=[]
for A in range(12,41):
  for T in range(6,A):
    yb=F(1,T)-F(1,A)
    if yb<=0 or (1/yb).denominator!=1: continue
    B=int(1/yb)
    if B>80: continue
    W=lcm(A,B); p=W//A; q=W//B
    if (p,q)==(3,2): continue
    for D in range(20,36):
      for a in range(2,10):
        sols=[]
        for x in range(1,D-a):
          y=D-a-x
          if y<=0: continue
          if p*a+(p+q)*x+q*y==W: sols.append(x)
        if len(sols)!=1: continue
        x=sols[0]
        # errors
        def solve(days, work):
            s=[]
            for xx in range(0,days+1):
                yy=days-xx
                if (p+q)*xx+q*yy==work: s.append(xx)
            return s
        ea=solve(D, W-p*a)      # forgot a days are within D
        eb=solve(D-a, W)        # forgot jia's work
        ec=solve(D, W)          # both
        em=solve(D-1-a, W-p*a); ep=solve(D+1-a, W-p*a)  # miscount days
        if len(ea)==1 and len(eb)==1 and len(ec)==1 and not em and not ep:
            vals=[x,ea[0],eb[0],ec[0]]
            if len(set(vals))==4 and min(vals)>0:
                res.append((A,T,B,W,p,q,D,a,vals))
for r in res: print(r)
print(len(res))
