from fractions import Fraction as F
import math, itertools
from collections import Counter
P=print
P('=== 39-3-1 three people pay: x-cost=f1(T-x); y-cost=f2(T-y); z-disc*cost=f3(T-z)')
c=0
for cost in [60,80,100,120,150]:
  for f1 in [F(1,4),F(1,3),F(2,7),F(1,5),F(2,9),F(3,7),F(1,2),F(2,5)]:
    for f2 in [F(1,4),F(1,3),F(2,7),F(1,5),F(3,8),F(2,5),F(1,2),F(3,5)]:
      for disc in [F(8,10),F(9,10)]:
        for f3 in [F(1,2),F(1,3),F(2,5),F(3,5),F(1,4),F(2,3)]:
          if f1==f2 or f2==f3 or f1==f3: continue
          A = f1/(1+f1) + f2/(1+f2) + f3/(1+f3)
          B = cost/(1+f1) + cost/(1+f2) + disc*cost/(1+f3)
          if A>=1: continue
          T=B/(1-A)
          if T.denominator==1 and 200<=T<=900:
            x=(cost+f1*T)/(1+f1); y=(cost+f2*T)/(1+f2); z=(disc*cost+f3*T)/(1+f3)
            if all(v.denominator==1 and v>cost for v in [x,y,z]) and c<25:
              P(cost,f1,f2,disc,f3,'T',T,'xyz',x,y,z); c+=1
P('=== 39-2-1 photos: singles s, group h = 2s+q?, s+h=T ; family r*h ; pair photos fm,fc,mc ; conds')
for T in range(30,80):
  for (p,q) in [(2,-1),(2,1),(2,-2),(2,2),(3,-1),(3,1)]:
    for s in range(1,T):
      h=p*s+q
      if h<=0 or s+h!=T: continue
      for r in [F(1,2),F(2,3),F(3,5),F(2,5),F(1,3),F(3,4)]:
        fam=r*h
        if fam.denominator!=1: continue
        pairs=h-fam
        sol=set()
        for fm in range(0,int(pairs)+1):
          for fc in range(0,int(pairs)-fm+1):
            mc=pairs-fm-fc
            if mc<0: continue
            c_g=fam+fc+mc; d_g=fam+fm+fc; m_g=fam+fm+mc
            # cond A: dad in group photos = mom in group photos + 4 ; cond B: child in group = dad in group
            if d_g!=m_g+4: continue
            if c_g!=d_g: continue
            for cs in range(0,s+1):
              for ds in range(0,s-cs+1):
                ms=s-cs-ds
                # cond C: child singles = dad singles + mom singles ; cond D: dad singles = 2 * mom singles
                if cs==ds+ms and ds==2*ms:
                  sol.add((m_g+ms, d_g+ds, c_g+cs, fm,fc,mc,cs,ds,ms))
        if len(sol)==1:
          P('T',T,'p,q',p,q,'s',s,'h',h,'r',r,'fam',fam,'sol(mom,dad,child,fm,fc,mc,cs,ds,ms)',sol)
