import itertools, random
used={65,77,86,95,15,20,33,38,24,32,35,40,9,53,85,110,21,27,34,41,10,18,19,90,80,126,88,79,16,58,48,44,7,14}
random.seed(17)
seen=set(); out=[]
for N in [62,64,66,68,70,72,74,76,78,82,84]:
  for n0 in range(3,9):
    for t in (4,5):
      for ab in range(5,14):
        for ac in range(3,ab):
          for bc in range(2,ac):
            for a in range(8,18):
              for b in range(6,a+1):
                c = N-n0-(a+b+ab+ac+bc+t)
                if c<5 or c>20: continue
                A=a+ab+ac+t; B=b+ab+bc+t; C=c+ac+bc+t
                if len({A,B,C})<3: continue
                AB,AC,BC=ab+t,ac+t,bc+t
                P=AB+AC+BC; S=A+B+C
                ex2=P-3*t; one=a+b+c; al1=N-n0
                opts={ex2,P-2*t,P-t,P}
                if opts & used: continue
                given={N,n0,A,B,C,AB,AC,BC,t}
                if opts & given: continue
                if one in opts or al1 in opts: continue
                # non-standard reading must be impossible (non-integer or negative t')
                tp2 = S-P-al1
                if tp2>=0 and tp2%2==0: continue
                key=(N,n0,t,A,B,C,AB,AC,BC)
                out.append(key+(ex2,P-2*t,P-t,P,one,(a,b,c,ab,ac,bc)))
print(len(out))
for o in random.sample(out,30): print(o)
