from fractions import Fraction as F
import itertools
def isint(x): return x.denominator==1 and x>0
out=[]
for f1 in [F(1,2),F(1,3),F(2,3),F(1,4),F(3,4)]:
  for f2 in [F(3,8),F(1,4),F(1,3),F(2,5),F(3,10),F(3,7),F(2,7),F(5,12),F(1,6),F(3,5)]:
    for N in range(60,121):
      for a in range(6,31):
        for n in range(4,21):
          B = N-a-n
          C = f2*B
          if not isint(C): continue
          abc = f1*C
          if not isint(abc): continue
          bc = C-abc
          if bc<=0: continue
          for ab in range(3,16):
            b = B-ab-C
            if b<=2: continue
            A = a+ab+abc
            e={}
            e['E1_forget_abc']=a+ab
            B2=N-n; C2=f2*B2; 
            if isint(C2) and isint(f1*C2): e['E2_B=N-n']=a+ab+f1*C2
            B3=N-a; C3=f2*B3
            if isint(C3) and isint(f1*C3): e['E3_B=N-a']=a+ab+f1*C3
            bc5=f2*B
            if isint(bc5) and f1<1:
                abc5=f1*bc5/(1-f1)
                if isint(abc5): e['E5_bc=f2B']=a+ab+abc5
            e['E8_abc=A/2'] = 2*(a+ab) if f1==F(1,2) else None
            e={k:v for k,v in e.items() if v is not None}
            vals=[int(v) for v in e.values()]
            if A in vals or len(set(vals))<len(vals): continue
            if len(vals)>=4:
                out.append((f1,f2,N,a,n,ab,'B',B,'C',C,'abc',abc,'bc',bc,'b',b,'A',A,{k:int(v) for k,v in e.items()}))
print(len(out))
import random
random.seed(3)
for o in random.sample(out,min(40,len(out))): print(o)
