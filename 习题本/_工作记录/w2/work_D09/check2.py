import itertools, math

def ceil(a,b): return -(-a//b)

print("2020SC0725-49: 5 ints sum 500, (a1+a2)/2 = a4+a5; min a3 (distinct and non-distinct)")
for distinct in (True,False):
    best=None
    for a3 in range(1,200):
        rem=500-a3
        if rem%3: continue
        s45=rem//3; s12=2*s45
        # a4,a5 <= a3 (strict if distinct), a1,a2 >= a3
        ok=False
        for a4 in range(1,a3+1):
            a5=s45-a4
            if a5<1 or a5>a4: continue
            if distinct and not (a3>a4>a5): continue
            if not distinct and not (a3>=a4>=a5): continue
            for a2 in range(a3,s12):
                a1=s12-a2
                if a1<a2: break
                if distinct and not (a1>a2>a3): continue
                ok=True;break
            if ok: break
        if ok: best=a3;break
    print(" distinct" if distinct else " nondistinct",best)

print("2025SD-57: N 40..49, N%4==3, N%5==3; 3 groups 11..19 distinct; min (max-min)")
for N in range(40,50):
    if N%4==3 and N%5==3:
        best=min(c-a for a in range(11,20) for b in range(a+1,20) for c in range(b+1,20) if a+b+c==N)
        print(" N",N,"best",best)

print("2021GK-68: 10 distinct ints (0.1万), sum 250, max<=2min; min of min")
for x in range(1,30):
    if x+sum(2*x-i for i in range(9))>=250 and 2*x-8>x:
        print(" x",x/10,"万");break

print("2023HB-73: 10 distinct, sum 230, max<=2min, min of min")
for x in range(1,30):
    if x+sum(2*x-i for i in range(9))>=230 and 2*x-8>x:
        print(" x",x);break

print("2021GK-65:")
best=0
for m in range(1,201):
  pass
# brute force additions a,b,c,d positive integers? amounts in 万; assume integer
base=[150,100,80,120]
best=0;arg=None
for a in range(1,201):
    for b in range(1,201-a):
        for c in range(1,201-a-b):
            d=200-a-b-c
            if d<1: continue
            v=[a,b,c,d]
            if max(v)>2*min(v): continue
            t=[base[i]+v[i] for i in range(4)]
            if max(t)-min(t)>best: best=max(t)-min(t); arg=(v,t)
print(" ",best,arg)

print("2023JSA-64:")
for n in range(2,100):
    if 220*n==260+218*(n-1):
        tot=220*n; print(" n",n,"max", tot-260-(n-2)*200)

print("2025ZJA-57: units forced 3..17; A 50 -> min #units")
s=list(range(3,18)); print(" sum",sum(s))
acc=0
for i,v in enumerate(sorted(s,reverse=True)):
    acc+=v
    if acc>=50: print(" units",i+1);break

print("2023ZJA-65: ages")
best=None
for a1 in range(1,80):
  for a2 in range(a1+1,90):
    for a4 in range(a2+2,100):
      a5=a1+10
      if not a5>a4: continue
      if 4*(a4+a5)!=5*(a1+a2): continue
      if a1+a2+a4+a5+8!=125: continue
      for a3 in range(a2+1,a4):
        if best is None or a3+4>best: best=a3+4; arg=(a1,a2,a3,a4,a5)
print(" ",best,arg)

print("2025ZJA-63: A=32; B=C+4; D< each other; max D")
best=None
for C in range(0,65):
    B=C+4; D=64-B-C
    if D<0: continue
    if D<C and D<B and D<32:
        best=D if best is None else max(best,D)
print(" ",best)

print("2018GK-73: B=24; C=A+6; D< each; min C")
best=None
for A in range(0,48):
    C=A+6; D=48-A-C
    if D<0: continue
    if D<A and D<C and D<24:
        best=C if best is None else min(best,C)
print(" ",best)

print("2021ZJA-56: 45; A=B+4; C=9; D<=each other; min A")
best=None
for B in range(0,45):
    A=B+4; C=9; D=45-A-B-C
    if D<0: continue
    if D<=A and D<=B and D<=C:
        best=A if best is None else min(best,A)
print(" ",best, " (ignoring D<=C):", min(B+4 for B in range(0,45) if 0<=45-2*B-4-9<=B))
