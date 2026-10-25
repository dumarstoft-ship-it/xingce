from fractions import Fraction as F
# mixed: 甲 O->P2 ; 乙 O->D ; 丙 P1->D ; segments O-P1 (甲乙), P1-P2 (甲乙丙), P2-D (乙丙)
out=[]
for r in (F(5,2),2,3,4):
  for d1 in range(2,25):
    for d2 in range(2,25):
      for d3 in range(2,25):
        f1,f2,f3=r*d1,r*d2,r*d3
        if any(x.denominator!=1 if isinstance(x,F) else False for x in (f1,f2,f3)): continue
        Ft=f1+f2+f3
        pay={'甲':F(f1,2)+F(f2,3),'乙':F(f1,2)+F(f2,3)+F(f3,2),'丙':F(f2,3)+F(f3,2)}
        if any(v.denominator!=1 for v in pay.values()): continue
        dist={'甲':d1+d2,'乙':d1+d2+d3,'丙':d2+d3}; S=sum(dist.values())
        prop={k:F(Ft*v,S) for k,v in dist.items()}
        eq=F(Ft,3)
        for who in ('乙','丙'):
            e_all3 = {'乙':F(f1,3)+F(f2,3)+F(f3,2),'丙':F(f1,3)+F(f2,3)+F(f3,2)}[who]  # 丙 assumed on from start
            vals=[pay[who],prop[who],eq,e_all3]
            if any(v.denominator!=1 for v in vals): continue
            if len(set(vals))<4: continue
            if Ft>160: continue
            out.append((who,r,(d1,d2,d3),(f1,f2,f3),Ft,{k:int(v) for k,v in pay.items()},int(prop[who]),int(eq),int(e_all3)))
for o in out: print(o)
print(len(out))
