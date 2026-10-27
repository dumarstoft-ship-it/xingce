from math import gcd, lcm
import itertools
def count(L, per): return (L-1)//per + 1
res=[]
for P in itertools.combinations(range(4,17),3):
    if any(gcd(a,b)==1 for a,b in itertools.combinations(P,2)): continue
    if any(b%a==0 for a,b in itertools.combinations(P,2)): continue
    if P==(4,6,10): continue
    for L in range(30,76):
        s=[count(L,p) for p in P]
        pr=[count(L,lcm(a,b)) for a,b in itertools.combinations(P,2)]
        t=count(L,lcm(*P))
        ex1=sum(s)-2*sum(pr)+3*t; un=sum(s)-sum(pr)+t
        endk=sum((L-1)%p==0 for p in P)
        if endk<2: continue
        prp=[count(L,a*b) for a,b in itertools.combinations(P,2)]
        tp=count(L,P[0]*P[1]*P[2])
        e_prod=sum(s)-2*sum(prp)+3*tp
        e_coef1=sum(s)-2*sum(pr)+t
        Q=tuple(p-1 for p in P)
        s2=[count(L,q) for q in Q]; pr2=[count(L,lcm(a,b)) for a,b in itertools.combinations(Q,2)]; t2=count(L,lcm(*Q))
        e_n=sum(s2)-2*sum(pr2)+3*t2
        for third,name in ((e_coef1,'coef1'),(e_n,'n')):
            v=[ex1,e_prod,un,third]
            if len(set(v))<4: continue
            if min(abs(x-y) for i,x in enumerate(v) for y in v[i+1:])<2: continue
            res.append((P,L,endk,s,pr,t,{'ex1':ex1,'prod':e_prod,'union':un,name:third}))
for r in res: print(r)
