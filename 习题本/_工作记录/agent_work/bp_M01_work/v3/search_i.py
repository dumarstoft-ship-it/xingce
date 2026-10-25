from fractions import Fraction as F
print("== 39-5-1: per-worker ratio e, total ratio R, transfer k")
for e in [F(5,4),F(4,3),F(3,2),F(6,5),F(5,3)]:
  for R in [F(5,4),F(4,3),F(8,5),F(5,3),F(7,4),F(2),F(9,5)]:
    if e==F(6,5) or R==F(3,2): continue
    for k in [10,12,15,16,18,20,24,25,30]:
      n1=2*k*R/(R-1); n2=e*n1/R
      if n1.denominator!=1 or n2.denominator!=1: continue
      naive=n1/R
      # wrong: transferred at B's efficiency: e(n1-k) = n2 + k with e n1 = R n2
      # solve: e n1 - e k = e n1/R + k -> n1 (e - e/R) = e k + k
      w1=(e*k+k)/(e-e/R); w2=e*w1/R
      if naive.denominator==1 and naive!=n2 and w2.denominator==1 and w2!=n2 and n1<300:
        print('e',e,'R',R,'k',k,'n1',n1,'n2',n2,'naive n2',naive,'wrong n2',w2)
print("== 29-8-1: total growth G, A +d, B down p and B25 = A25/2, C up q and C24 = A24+B24")
for G in [F(1,4),F(3,10),F(3,20),F(1,5)*0+F(1,10)]:
  for d in [100,120,150,200,240,300]:
    for p in [F(1,4),F(1,5),F(1,3)]:
      for q in [F(2,5),F(1,2),F(3,10),F(1,4)]:
        for a in range(10,3000,10):
          j25=a+d; y25=F(j25,2); y24=y25/(1-p); b24=a+y24; b25=(1+q)*b24
          if (j25+y25+b25)==(1+G)*(a+y24+b24) and y24.denominator==1 and b25.denominator==1:
            t25=j25+y25+b25; t24=a+y24+b24
            print('G',G,'d',d,'p',p,'q',q,'a',a,'y24',y24,'b24',b24,'b25',b25,'share',float(b25/t25),'s24',float(b24/t24),'mix',float(b25/t24),float(b24/t25))
