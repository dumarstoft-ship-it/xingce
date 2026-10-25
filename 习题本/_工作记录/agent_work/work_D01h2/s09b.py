from fractions import Fraction as F
out=[]
for e1 in range(5,51):          # 2025: Mar vs Feb
  for e2 in range(1,21):        # 2025 Mar YoY
    for e3 in range(30,101):    # 2024: Mar vs Feb
      ans=F(100+e2,100)*F(100+e3,100)/F(100+e1,100)-1
      if (ans*100).denominator!=1: continue
      a=int(ans*100)
      if a<=0: continue
      add=e2+e3-e1
      ign=F(100+e2,100+e1)-1
      dir_=F(100+e2,100)*F(100+e1,100)/F(100+e3,100)-1
      DA=F(100+e2,100)*F(100+e3,100)-1
      diff=e3-e1
      c={'ans':a,'add':add,'diff':diff}
      if (DA*100).denominator==1: c['DA']=int(DA*100)
      if len(set(c.values()))<len(c): continue
      if len(c)<4: continue
      # prefer 'nice' inputs (multiples of 5) 
      nice=sum(1 for e in (e1,e2,e3) if e%5==0)
      out.append((nice,e1,e2,e3,c))
out.sort(key=lambda o:-o[0])
for o in out[:60]: print(o)
print(len(out))
