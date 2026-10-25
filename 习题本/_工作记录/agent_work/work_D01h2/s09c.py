from fractions import Fraction as F
out=[]
for e1 in range(-40,61):
  for e2 in range(-20,41):
    for e3 in range(-40,101):
      if 0 in (e1,e2,e3): continue
      f1,f2,f3=F(100+e1,100),F(100+e2,100),F(100+e3,100)
      ans=f2*f3/f1-1
      if (ans*100).denominator!=1: continue
      a=int(ans*100)
      if a==0: continue
      c={'ans':a,'add':e2+e3-e1}
      base=f2*f3*(2-f1)-1
      if (base*100).denominator==1: c['base']=int(base*100)
      DA=f2*f3-1
      if (DA*100).denominator==1: c['DA']=int(DA*100)
      ign=f2/f1-1
      if (ign*100).denominator==1: c['ign']=int(ign*100)
      c['diff']=e3-e1
      if 'base' not in c: continue
      vals=list(c.values())
      if len(set(vals))<len(vals): continue
      nice=sum(1 for e in (e1,e2,e3) if e%5==0)
      if nice<3: continue
      if not all(-30<=v<=80 for v in (c['ans'],c['add'],c['base'])): continue
      out.append((e1,e2,e3,c))
for o in out: print(o)
print(len(out))
