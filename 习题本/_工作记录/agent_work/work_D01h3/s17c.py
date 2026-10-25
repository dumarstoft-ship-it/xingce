from fractions import Fraction as F
out=[]
for D in range(18,61):
  for d1 in range(2,D):
    for d2 in range(2,D-d1):
      d3=D-d1-d2
      if d3<2: continue
      for Ft in range(60,241,10):
        r=F(Ft,D)
        f1,f2,f3=r*d1,r*d2,r*d3
        pay={'甲':f1/2+f2/3,'乙':f1/2+f2/3+f3/2,'丙':f2/3+f3/2}
        if any(v.denominator!=1 for v in (f1,f2,f3)) or any(v.denominator!=1 for v in pay.values()): continue
        dist={'甲':d1+d2,'乙':D,'丙':d2+d3}; S=sum(dist.values())
        prop={k:Ft*F(v,S) for k,v in dist.items()}
        eq=F(Ft,3)
        for who in ('乙','丙'):
            e3={'乙':f1/3+f2/3+f3/2,'丙':f1/3+f2/3+f3/2}[who]
            vals=[pay[who],prop[who],eq,e3]
            if any(v.denominator!=1 for v in vals) or len(set(vals))<4: continue
            if D==30 or Ft in (144,240,200,180,90): continue
            if r.denominator!=1 and r!=F(5,2): continue
            out.append((who,D,(d1,d2,d3),Ft,str(r),(int(f1),int(f2),int(f3)),{k:int(v) for k,v in pay.items()},int(prop[who]),int(eq),int(e3)))
for o in out: print(o)
print(len(out))
