from fractions import Fraction as F
out=[]
for A in (60,80,90,100,120):
  for D in (20,30,40,50,60):
    B=A-D
    if B<=0: continue
    for C in range(20,101,10):
      for m in range(4,12):
        for k in (F(3,2),F(2),F(5,2),F(3),F(4)):
          T=k*C*(13-m)                       # 乙 weight
          w=(T+A-13*B)/F(A-B)
          if w.denominator!=1 or not 2<=w<=12: continue
          w=int(w)
          if w==m: continue
          pend=w-1
          pe3=w-F(A,A-B)
          pc=(k*C*(12-m)+A-13*B)/F(A-B)       # 丙 months counted 12-m
          pe1=w+F(B,A-B)
          cand={'end':pend}
          if pe3.denominator==1 and pe3>=1: cand['e3']=int(pe3)
          if pc.denominator==1 and pc>=1: cand['c']=int(pc)
          vals=list(cand.values())
          if len(cand)<3 or len(set(vals))<3 or w in vals: continue
          out.append((A,D,B,C,m,str(k),w,cand,'e1',pe1))
for o in out: print(o)
print(len(out))
