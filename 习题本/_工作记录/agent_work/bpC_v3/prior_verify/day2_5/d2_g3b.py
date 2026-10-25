from itertools import product, combinations
P=['甲','乙','丙','丁','戊']
worlds=[]
for m in product([0,1],repeat=5):
    if sum(m)!=2: continue
    for d in product([0,1],repeat=5):
        if sum(d)!=3: continue
        for j in product([0,1],repeat=5):
            if sum(j)!=1: continue
            M=dict(zip(P,m));D=dict(zip(P,d));J=dict(zip(P,j))
            if any(not(M[x] or D[x] or J[x]) for x in P): continue
            L=[x for x in P if M[x] and D[x] and J[x]]
            if len(L)!=1: continue
            worlds.append((M,D,J,L[0]))
conds=[]
for x,y in combinations(P,2):
    conds.append((f'{x}和{y}性别相同',lambda w,x=x,y=y:w[0][x]==w[0][y]))
    conds.append((f'{x}是党员当且仅当{y}是党员',lambda w,x=x,y=y:w[1][x]==w[1][y]))
    conds.append((f'{x}和{y}不全是党员',lambda w,x=x,y=y:not(w[1][x] and w[1][y])))
    conds.append((f'{x}和{y}性别不同',lambda w,x=x,y=y:w[0][x]!=w[0][y]))
for x in P:
    conds.append((f'{x}没有基层经历',lambda w,x=x:w[2][x]==0))
    conds.append((f'{x}不是党员',lambda w,x=x:w[1][x]==0))
out=[]
for cs in combinations(conds,4):
    names=[c[0] for c in cs]
    if sum('当且仅当' in n for n in names)!=1 or sum('不全是' in n for n in names)!=1: continue
    S=[w for w in worlds if all(c[1](w) for c in cs)]
    if len(S)<1: continue
    if len({w[3] for w in S})==1:
        out.append((names,S[0][3],len(S)))
print(len(out))
import random; random.seed(2)
for o in random.sample(out,min(15,len(out))): print(o)
