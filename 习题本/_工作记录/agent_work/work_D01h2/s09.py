from fractions import Fraction as F
rates=[F(x,100) for x in range(-30,61,5)]+[F(x,100) for x in (12,8,6,4,16,24,28,32,36)]
rates=sorted(set(rates))
out=[]
for e1 in rates:      # 2025 M+1 vs 2025 M  (环比)
  for e2 in rates:    # 2025 M+1 vs 2024 M+1 (同比)
    for e3 in rates:  # 2024 M+1 vs 2024 M  (上年环比)
      if 0 in (e1,e2,e3): continue
      ans=(1+e2)*(1+e3)/(1+e1)-1
      if (ans*100).denominator!=1: continue
      a=int(ans*100)
      if not(-30<=a<=60) or a==0: continue
      N1=int((e2+e3-e1)*100)       # additive
      N2=int((e2-e1)*100)          # ignore last year's 环比
      N5=(1+e2)*(1+e3)-1           # D vs A
      N6=(1+e2)/(1+e1)-1           # ignoring e3 multiplicatively
      N7=(1+e2)*(1+e1)/(1+e3)-1    # swapped e1/e3
      c={'ans':a,'N1':N1,'N2':N2}
      for k,v in (('N5',N5),('N6',N6),('N7',N7)):
        if (v*100).denominator==1: c[k]=int(v*100)
      if len(set(c.values()))<len(c): continue
      if len(c)<4: continue
      out.append((int(e1*100),int(e2*100),int(e3*100),c))
print(len(out))
for o in out: 
  if abs(o[0])<=30 and abs(o[1])<=30 and abs(o[2])<=50: print(o)
