from itertools import product, combinations
P=['甲','乙','丙','丁']
conds=[]
for x,y in combinations(P,2):
    conds.append((f'{x}和{y}性别相同', lambda G,H,x=x,y=y: G[x]==G[y]))
    conds.append((f'{x}和{y}性别不同', lambda G,H,x=x,y=y: G[x]!=G[y]))
    conds.append((f'{x}和{y}职称情况相同', lambda G,H,x=x,y=y: H[x]==H[y]))
    conds.append((f'{x}和{y}不都是高级职称', lambda G,H,x=x,y=y: not(H[x] and H[y])))
for x in P:
    conds.append((f'{x}不是高级职称', lambda G,H,x=x: H[x]==0))
    conds.append((f'{x}是男性', lambda G,H,x=x: G[x]=='男'))
worlds=[]
for g in product('男女',repeat=4):
    if g.count('男')!=2: continue
    for h in product([0,1],repeat=4):
        if sum(h)!=2: continue
        G=dict(zip(P,g)); H=dict(zip(P,h))
        L=[x for x in P if G[x]=='女' and H[x]==1]
        if len(L)!=1: continue   # 组长唯一存在
        worlds.append((G,H,L[0]))
print('基础世界数',len(worlds))
out=[]
for cs in combinations(conds,3):
    S=[w for w in worlds if all(c[1](w[0],w[1]) for c in cs)]
    if not S: continue
    leaders={w[2] for w in S}
    if len(leaders)==1 and len(S)>=2:
        out.append(([c[0] for c in cs], leaders, len(S)))
print(len(out))
import random; random.seed(1)
for o in random.sample(out,12): print(o)
