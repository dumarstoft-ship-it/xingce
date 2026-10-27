from fractions import Fraction as F
def isint(x): return x.denominator==1 and x>0
out=[]
f1=F(1,2)
for f2 in [F(1,3),F(2,5),F(3,8),F(1,4),F(2,7),F(3,10),F(3,7)]:
    for N in range(70,111):
      for a in range(6,31):
        for n in range(5,21):
          B = N-a-n
          C = f2*B
          if not isint(C): continue
          abc = f1*C
          if not isint(abc): continue
          bc = C-abc
          for ab in range(4,16):
            b = B-ab-C
            if b<=4: continue
            A = a+ab+abc
            e={}
            e['E1']=a+ab
            B3=N-a; C3=f2*B3
            if not (isint(C3) and isint(f1*C3)): continue
            e['E3']=a+ab+f1*C3
            bc5=f2*B
            abc5=bc5
            e['E5']=a+ab+abc5
            B2=N-n; C2=f2*B2
            if isint(C2) and isint(f1*C2): e['E2']=a+ab+f1*C2
            vals=[int(v) for v in e.values()]
            if A in vals or len(set(vals))<len(vals): continue
            regs=[a,b,ab,bc,abc,n]
            if len(set(regs))<5: continue  # bc==abc forced
            if len({B,C,A,N}|set(regs))<len(regs)+4-1: continue
            out.append((str(f2),N,'a',a,'n',n,'ab',ab,'B',B,'C',int(C),'abc',int(abc),'b',int(b),'A',int(A),{k:int(v) for k,v in e.items()}))
print(len(out))
import random
random.seed(5)
for o in random.sample(out,min(50,len(out))): print(o)
