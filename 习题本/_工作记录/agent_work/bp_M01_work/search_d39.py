from fractions import Fraction as F
import itertools, math
P=print
P('=== D29-V23 data center (unique, moderate counts)')
for pa,pb,pc in [(1,2,4),(1,2,5),(1,3,5),(2,3,5),(1,3,4),(2,3,6)]:
  for fb,fc in [(F(3,2),F(3,2)),(2,2),(F(3,2),2),(2,F(3,2)),(F(5,4),F(3,2)),(F(4,3),F(3,2))]:
    hits=[]
    for N in range(100,301,20):
      for z in range(20,N):
        for y in range(20,N-z):
          x=N-y-z
          if x<20: continue
          P1=x*pa+y*pb+z*pc
          if fb*y*pb+fc*z*pc==P1 and fb*y==int(fb*y) and fc*z==int(fc*z):
            hits.append((N,x,y,z,P1))
    if hits: P(pa,pb,pc,str(fb),str(fc),hits[:4])

P('=== D39-V3 photos: family of 3 ; singles s ; groups h ; h = p*s + q ; s+h = T ; family = r*h ; child_in_group = (dad_in_group+mom_in_group)/2 ? ; child single = dad+mom single + 1')
# variant: ask dad appearances; add condition: dad-mom pair photos = mom-child pair photos
for T in range(30,90):
  for (p,q) in [(2,-1),(2,1),(F(3,2),0),(2,-2),(F(3,2),1)]:
    for s in range(1,T):
      h=p*s+q
      if h!=int(h) or s+h!=T or h<=0: continue
      for r in [F(1,2),F(2,3),F(3,5),F(2,5),F(1,3)]:
        fam=r*h
        if fam!=int(fam): continue
        pairs=h-fam
        sol=set()
        for fm in range(0,int(pairs)+1):
          for fc in range(0,int(pairs)-fm+1):
            mc=pairs-fm-fc
            if mc<0: continue
            c_g=fam+fc+mc; d_g=fam+fm+fc; m_g=fam+fm+mc
            if 2*c_g!=d_g+m_g: continue
            if fm!=mc: continue  # extra condition: dad-mom pair photos == mom-child pair photos
            for cs in range(0,s+1):
              for ds in range(0,s-cs+1):
                ms=s-cs-ds
                if cs==ds+ms+1 and ds==ms+1:   # extra: dad singles 1 more than mom singles
                  sol.add((d_g+ds, c_g+cs, fm,fc,mc,cs,ds,ms))
        dads=set(x[0] for x in sol)
        if len(sol)==1:
          P('T',T,'p,q',p,q,'s',s,'h',h,'r',r,'fam',fam,'sol',sol)
P('=== D39-V4 talent subsidy chain')
for x in [F(i,10) for i in range(5,60)]:
    ben=F(3,2)*x; mas=ben+1; doc=2*mas
    for ppl in [(10,20,8,2),(5,10,4,1),(10,15,6,2),(8,12,5,1)]:
        per_unit=sum(a*b for a,b in zip(ppl,[x,ben,mas,doc]))
        for k in range(1,50):
            tot=k*per_unit
            if tot==int(tot) and 1000<=tot<=5000 and k*sum(ppl) in (200,250,300,400,500):
                P('zhuanke',x,'ppl ratio',ppl,'k',k,'people',k*sum(ppl),'total',tot)
P('=== D39-V9 three people shopping')
for cost in [100,120,150,200]:
  for f1 in [F(1,4),F(1,3),F(2,7),F(1,5),F(2,9),F(3,7)]:
    for f2 in [F(1,4),F(1,3),F(2,7),F(1,5),F(3,8),F(2,5)]:
      for disc in [F(8,10),F(9,10)]:
        for f3 in [F(1,2),F(1,3),F(2,5),F(3,5),F(1,4)]:
          if f1==f2: continue
          # x - cost = f1*(T - x) -> x = (cost + f1 T)/(1+f1)
          # T = x+y+z
          # solve linear in T: x = (cost + f1*T)/(1+f1); y similar; z = (disc*cost + f3*T)/(1+f3)
          A = f1/(1+f1) + f2/(1+f2) + f3/(1+f3)
          B = cost/(1+f1) + cost/(1+f2) + disc*cost/(1+f3)
          if A==1: continue
          T=B/(1-A)
          if T>0 and T==int(T) and 300<=T<=1500:
            x=(cost+f1*T)/(1+f1); y=(cost+f2*T)/(1+f2); z=(disc*cost+f3*T)/(1+f3)
            if all(v==int(v) and v>cost for v in [x,y,z]):
              P(cost,f1,f2,disc,f3,'T',T,'xyz',x,y,z)
