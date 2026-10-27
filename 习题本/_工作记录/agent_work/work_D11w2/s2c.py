import itertools, random
from collections import Counter
used={95,33,32,53,34,10,27,21,41}
cnt=Counter(); out=[]
for N in [62,64,66,68,70,72,74,76,78,82,84]:
  for n0 in range(3,9):
    for t in (4,5):
      for ab in range(5,14):
        for ac in range(3,ab):
          for bc in range(2,ac):
            for a in range(8,18):
              for b in range(6,a+1):
                c = N-n0-(a+b+ab+ac+bc+t)
                if c<5 or c>20: cnt['c']+=1; continue
                A=a+ab+ac+t; B=b+ab+bc+t; C=c+ac+bc+t
                AB,AC,BC=ab+t,ac+t,bc+t
                P=AB+AC+BC; S=A+B+C
                ex2=P-3*t; one=a+b+c; al1=N-n0
                opts={ex2,P-2*t,P-t,P}
                if opts & used: cnt['used']+=1; continue
                given={N,n0,A,B,C,AB,AC,BC,t}
                if opts & given: cnt['given']+=1; continue
                if one in opts or al1 in opts: cnt['one']+=1; continue
                out.append((N,n0,t,A,B,C,AB,AC,BC,ex2,P-2*t,P-t,P,one,(a,b,c,ab,ac,bc)))
print(cnt, len(out))
random.seed(17)
for o in random.sample(out,min(30,len(out))): print(o)
