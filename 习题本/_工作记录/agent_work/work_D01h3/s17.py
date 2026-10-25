from fractions import Fraction as F
# scenario A: all start together; 甲 off after seg1, 乙 off after seg2, 丙 to end
print("== drop-off scenario")
for r in (2,3,4,5):
  for d1 in range(3,21):
    for d2 in range(3,21):
      for d3 in range(3,21):
        f1,f2,f3=r*d1,r*d2,r*d3
        Ftot=f1+f2+f3
        pay={'甲':F(f1,3),'乙':F(f1,3)+F(f2,2),'丙':F(f1,3)+F(f2,2)+f3}
        if any(v.denominator!=1 for v in pay.values()): continue
        dist={'甲':d1,'乙':d1+d2,'丙':d1+d2+d3}
        S=sum(dist.values())
        prop={k:F(Ftot*v,S) for k,v in dist.items()}
        eq=F(Ftot,3)
        for who in ('丙',):
            vals=[pay[who],prop[who],eq]
            if any(v.denominator!=1 for v in vals): continue
            if len(set(vals))<3: continue
            if Ftot>150: continue
            print(who,'r',r,'d',(d1,d2,d3),'fares',(f1,f2,f3),'F',Ftot,'pay',{k:int(v) for k,v in pay.items()},'prop',{k:str(v) for k,v in prop.items()},'eq',eq)
