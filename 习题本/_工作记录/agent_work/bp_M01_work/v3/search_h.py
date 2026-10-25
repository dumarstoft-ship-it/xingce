from fractions import Fraction as F
import itertools
print("== 1-4-1 clinic: total ratio r1, average ratio r2, doctors D, visits V")
for r1 in [F(6,5),F(5,4),F(4,3),F(9,10),F(3,4),F(7,5)]:
  for r2 in [F(3,4),F(9,10),F(2,3),F(3,5),F(4,5)*0+F(7,10),F(5,6)]:
    c=r1/r2
    if c in (F(3,2),) or r1 in (F(4,5),F(3,2)) or r2 in (F(4,5),F(3,2)): continue
    for D in range(30,70):
      n1=D/(1+c); n2=D-n1
      if n1.denominator!=1: continue
      for V in range(400,1500,10):
        t1=V/(1+r1); t2=V-t1
        if t1.denominator!=1: continue
        a1=t1/n1; a2=t2/n2
        if a1.denominator==1 and a2.denominator==1 and a2!=a1 and F(V,D).denominator<=5:
          print('r1',r1,'r2',r2,'c',c,'D',D,'V',V,'n',n1,n2,'t',t1,t2,'avg',a1,a2,'V/D',float(F(V,D)), 't2/n1', t2/n1)
          break
      else: continue
      break
