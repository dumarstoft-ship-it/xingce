import itertools, random
random.seed(7)
cands=[]
for N in [62,64,66,68,70,72,74,76,78,80]:
  for n0 in range(3,9):
    for t in range(3,6):
      # regions
      for _ in range(3000):
        ab,ac,bc = [random.randint(2,12) for _ in range(3)]
        a,b = random.randint(4,16), random.randint(4,16)
        c = N-n0-(a+b+ab+ac+bc+t)
        if c<3: continue
        A=a+ab+ac+t; B=b+ab+bc+t; C=c+ac+bc+t
        AB,AC,BC=ab+t,ac+t,bc+t
        P=AB+AC+BC; S=A+B+C
        ex2=P-3*t; one=a+b+c; al1=N-n0
        opts={ex2,P-2*t,P-t,P}
        given={N,n0,A,B,C,AB,AC,BC}
        if len(opts)<4: continue
        if one in opts or al1 in opts: continue
        if opts & given: continue
        if len({A,B,C})<3 or len({AB,AC,BC})<3: continue
        if not (A>B>C) : continue
        if not (AB>AC>BC): continue
        cands.append((N,n0,t,A,B,C,AB,AC,BC,ex2,P-2*t,P-t,P,one,(a,b,c,ab,ac,bc)))
print(len(cands))
seen=set()
for c in random.sample(cands,40):
    print(c)
