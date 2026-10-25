from fractions import Fraction as F
import itertools
print("== 29-6-1 search: total N, men:women a:b, pass p:q, fail r:s ; want pass != fail, integers")
for (a,b) in [(4,5),(5,4),(3,4),(4,3),(5,7),(7,5)]:
  for N in [630,720,810,900,960,990,1080]:
    if N%(a+b): continue
    M=N*a//(a+b); W=N-M
    for (p,q) in [(1,2),(2,3),(1,3),(3,4),(2,1)]:
      for (r,s) in [(5,4),(4,3),(3,2),(6,5),(7,5),(2,1)]:
        for x in range(1,M):
          if (M-x)*s==(W-q*x/p)*r if False else None: pass
        # pass men = p*t, pass women = q*t
        for t in range(1,N):
          pm,pw=p*t,q*t
          if pm>M or pw>W: break
          fm,fw=M-pm,W-pw
          if fm*s==fw*r and fm>0:
            P=pm+pw
            if P!=N-P: print((a,b),N,(p,q),(r,s),'pass',P,'fail',N-P,'passW',pw,'passM',pm)
