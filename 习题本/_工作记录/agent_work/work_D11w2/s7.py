from math import gcd, lcm
import itertools
def count(L, per):  # days 1..L with (d-1)%per==0
    return (L-1)//per + 1
def stats(L, P):
    p1,p2,p3=P
    s=[count(L,p) for p in P]
    pr=[count(L,lcm(a,b)) for a,b in ((p1,p2),(p1,p3),(p2,p3))]
    t=count(L,lcm(p1,p2,p3))
    ex1=sum(s)-2*sum(pr)+3*t
    un=sum(s)-sum(pr)+t
    al2=sum(pr)-2*t
    return s,pr,t,ex1,un,al2
def brute(L,P):
    ex1=0
    for d in range(1,L+1):
        k=sum((d-1)%p==0 for p in P)
        ex1+= (k==1)
    return ex1
res=[]
for P in itertools.combinations(range(4,13),3):
    if any(gcd(a,b)==1 for a,b in itertools.combinations(P,2)): continue
    if any(b%a==0 for a,b in itertools.combinations(P,2)): continue
    for L in range(30,76):
        s,pr,t,ex1,un,al2=stats(L,P)
        assert ex1==brute(L,P)
        # end day on a common pair/triple period
        endk=sum((L-1)%p==0 for p in P)
        if endk<2: continue
        # error paths
        # E_prod: pairwise as products, triple as product
        p1,p2,p3=P
        prp=[count(L,a*b) for a,b in ((p1,p2),(p1,p3),(p2,p3))]
        tp=count(L,p1*p2*p3)
        e_prod=sum(s)-2*sum(prp)+3*tp
        e_un=un
        e_coef1=sum(s)-2*sum(pr)+t
        e_coef2=sum(s)-sum(pr)+t  # = union
        # E_n: every n days as period n (每隔n天 -> period n-1 interpreted)
        Q=tuple(p-1 for p in P)
        if min(Q)>=2:
            s2=[count(L,q) for q in Q]
            pr2=[count(L,lcm(a,b)) for a,b in ((Q[0],Q[1]),(Q[0],Q[2]),(Q[1],Q[2]))]
            t2=count(L,lcm(*Q))
            e_n=sum(s2)-2*sum(pr2)+3*t2
        else: e_n=None
        # exclude start day
        e_nostart=ex1  # start day has all three -> not exactly one, so same
        e_sub3=sum(s)-3*sum(pr)+3*t  # wrong coefficient for pairs
        o={'ex1':ex1,'prod':e_prod,'union':e_un,'coef1':e_coef1,'n':e_n,'al2':al2}
        res.append((P,L,endk,s,pr,t,o))
good=[]
for P,L,endk,s,pr,t,o in res:
    keys=['prod','union','coef1','n']
    vals=[o['ex1']]+[o[k] for k in keys if o[k] is not None]
    if len(set(vals))<len(vals): continue
    if len(vals)<5: continue
    good.append((P,L,endk,s,pr,t,o))
print(len(good))
for g in good: 
    if g[1] in (59,61,62,60,31,30,62,92,91,45,40,50,56,63,70,72,73,49,57,65,66,67,68,69,71,74,75): print(g)
