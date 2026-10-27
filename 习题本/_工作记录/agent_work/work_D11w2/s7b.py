from math import gcd, lcm
import itertools
def count(L, per): return (L-1)//per + 1
def ex1_of(L,P):
    s=[count(L,p) for p in P]
    pr=[count(L,lcm(a,b)) for a,b in itertools.combinations(P,2)]
    t=count(L,lcm(*P))
    return s,pr,t,sum(s)-2*sum(pr)+3*t, sum(s)-sum(pr)+t
res=[]
for P in itertools.combinations(range(4,17),3):
    if any(gcd(a,b)==1 for a,b in itertools.combinations(P,2)): continue
    if any(b%a==0 for a,b in itertools.combinations(P,2)): continue
    for L in (30,31,59,60,61,62,91,92):
        s,pr,t,ex1,un=ex1_of(L,P)
        endk=sum((L-1)%p==0 for p in P)
        prp=[count(L,a*b) for a,b in itertools.combinations(P,2)]
        tp=count(L,P[0]*P[1]*P[2])
        e_prod=sum(s)-2*sum(prp)+3*tp
        e_coef1=sum(s)-2*sum(pr)+t
        Q=tuple(p-1 for p in P)
        s2=[count(L,q) for q in Q]; pr2=[count(L,lcm(a,b)) for a,b in itertools.combinations(Q,2)]; t2=count(L,lcm(*Q))
        e_n=sum(s2)-2*sum(pr2)+3*t2
        o={'ex1':ex1,'prod':e_prod,'union':un,'coef1':e_coef1,'n':e_n}
        if e_prod==ex1: continue
        if un in (ex1,e_prod): continue
        others=[v for k,v in o.items() if k not in('ex1','prod','union')]
        if all(v in (ex1,e_prod,un) for v in others): continue
        if pr!=prp or True:
            res.append((P,L,endk,s,pr,t,o))
for r in res: print(r)
