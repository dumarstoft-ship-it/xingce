from fractions import Fraction as F
from math import gcd
out=[]
for a in range(3,13):
  for b in range(a+1,16):
    for c in range(1,a):
      for m in range(1,7):
        for n in range(1,7):
          if gcd(m,n)!=1 or m==n: continue
          avg=F(m*b+n*c,m+n)
          if avg<=a: continue
          for S in range(10,121):
            N=S/(avg-a)
            if N.denominator!=1: continue
            N=int(N)
            if N%(m+n): continue
            if not 30<=N<=240: continue
            sa=F(b+c,2)
            Ns=S/(sa-a) if sa>a else None
            avr=F(n*b+m*c,m+n)
            Nr=S/(avr-a) if avr>a else None
            tot=a*N+S
            c_={'N':N}
            if Ns is not None and Ns.denominator==1: c_['Ns']=int(Ns)
            if Nr is not None and Nr.denominator==1: c_['Nr']=int(Nr)
            if len(c_)<3: continue
            if len(set(c_.values()))<3: continue
            out.append((a,b,c,m,n,S,N,m*N//(m+n),n*N//(m+n),tot,c_, str(avg)))
print(len(out))
import random
random.seed(5)
for o in random.sample(out,min(70,len(out))): print(o)
