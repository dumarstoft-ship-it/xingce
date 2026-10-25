# need 14: A,B sales equal -> counts inverse to price; pack; find C count
from math import gcd
from fractions import Fraction as F
out=[]
prices=range(20,125,5)
for pA in prices:
  for pB in prices:
    if pB>=pA: continue
    g=gcd(pA,pB); u,v=pB//g,pA//g      # nA:nB = u:v
    if u+v>8: continue
    for pC in prices:
      if pC in (pA,pB): continue
      for N in range(100,301,10):
        for R in range(1000,30001,100):
          # correct
          # nA=u t, nB=v t, nC=N-(u+v)t ; revenue 2 pA u t + pC (N-(u+v)t) = R
          den=2*pA*u-pC*(u+v)
          if den==0: continue
          num=R-pC*N
          if num%den: continue
          t=num//den
          if t<=0: continue
          nA,nB,nC=u*t,v*t,N-(u+v)*t
          if nC<=0: continue
          # E1: direct ratio nA:nB = v:u (A count bigger share for higher price)
          den1=pA*v+pB*u-pC*(u+v)
          if den1==0: continue
          if num%den1: continue
          s=num//den1
          if s<=0: continue
          nC1=N-(u+v)*s
          if nC1<=0: continue
          opts={nC,nC1,nC//(u+v) if nC%(u+v)==0 else None,nA,nB}
          if None in opts: continue
          if len(opts)<5: continue
          out.append((pA,pB,pC,N,R,u,v,t,nA,nB,nC,s,nC1,nC//(u+v)))
print(len(out))
import random
random.seed(1)
for o in out:
    pA,pB,pC,N,R,u,v,t,nA,nB,nC,s,nC1,pk=o
    if pA%10==0 and pB%10==0 and pC%5==0 and N%50==0 and R%100==0 and pA<=100:
        print(f"pA={pA} pB={pB} pC={pC} N={N} R={R} u:v={u}:{v} nA={nA} nB={nB} nC={nC} | E1 nC={nC1} (s={s}) | pkg={pk}")
