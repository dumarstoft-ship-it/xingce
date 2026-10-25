# search data for v07 (capital x months)
from fractions import Fraction as F
res=[]
for a in range(10,61,5):
  for b in range(20,81,10):
    for d in range(10,b,10):
      for m1 in range(3,11):       # 乙 m1月初撤回 d
        for c in range(10,81,10):
          for m2 in range(4,12):   # 丙 m2月初加入
            wa=12*a; wb=b*(m1-1)+(b-d)*(13-m1); wc=c*(13-m2)
            W=wa+wb+wc
            for r in (F(1,5),F(1,4),F(2,5)):
              for P in (60,75,80,90,100,120,125,150,160,180,200,240,250,300):
                S=P*(1-r)*F(wc,W)
                if S.denominator!=1: continue
                if S<5 or S>60: continue
                # distractors
                P1=S*F(W,wc)                         # forget retention
                W2=wa+12*(b-d)+wc; P2=S*F(W2,wc)/(1-r)  # yi at reduced all year
                W3=wa+12*b+wc; P3=S*F(W3,wc)/(1-r)      # yi at b all year
                wc5=c*(12-m2); W5=wa+wb+wc5; P5=S*F(W5,wc5)/(1-r) if wc5>0 else None
                P7=P1*(1+r)                          # times (1+r)
                cands={'P':P,'P1':P1,'P2':P2,'P3':P3,'P5':P5,'P7':P7}
                ints={k:v for k,v in cands.items() if v is not None and v.denominator==1}
                if len(ints)<5: continue
                vals=list(ints.values())
                if len(set(vals))<len(vals): continue
                res.append((a,b,d,m1,c,m2,str(r),P,S,W,wa,wb,wc,{k:int(v) for k,v in ints.items()}))
print(len(res))
import random
random.seed(1)
for x in random.sample(res,min(60,len(res))): print(x)
