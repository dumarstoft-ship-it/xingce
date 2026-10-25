from itertools import permutations, product, combinations
import random
random.seed(21)
P=['甲','乙','丙']
W=[dict(zip(P,p)) for p in permutations([1,2,3])]
def atoms_for(x):
    return [(f'{x}是第{r}名',lambda w,x=x,r=r:w[x]==r) for r in (1,2,3)]+[(f'{x}不是第{r}名',lambda w,x=x,r=r:w[x]!=r) for r in (1,2,3)]
A={x:atoms_for(x) for x in P}
views=list(product(A['甲'],A['乙'],A['丙']))
res=[]
for trial in range(200000):
    vs=random.sample(views,3)
    S=[w for w in W if all(sum(a[1](w) for a in v)==1 for v in vs)]
    if len(S)==1:
        neg=sum('不是' in a[0] for v in vs for a in v)
        if 2<=neg<=4: res.append(([[a[0] for a in v] for v in vs],S[0]))
    if len(res)>=6: break
for r in res: print(r)
