from itertools import permutations, combinations
P=['甲','乙','丙']; AW=['文旅','生态','数字']
worlds=[]
for a in permutations(AW):
    A=dict(zip(P,a)); W={v:k for k,v in A.items()}
    for inc in permutations([1,2,3]):
        I=dict(zip(P,inc)); worlds.append((A,W,I))
conds=[]
for x in AW:
    for y in P:
        conds.append((f'获{x}奖的村收入高于{y}村',lambda w,x=x,y=y:w[2][w[1][x]]>w[2][y]))
        conds.append((f'{y}村收入高于获{x}奖的村',lambda w,x=x,y=y:w[2][y]>w[2][w[1][x]]))
for y in P:
    conds.append((f'{y}村收入不是最高的',lambda w,y=y:w[2][y]!=3))
    conds.append((f'{y}村收入不是最低的',lambda w,y=y:w[2][y]!=1))
out=[]
for cs in combinations(conds,3):
    S=[w for w in worlds if all(c[1](w) for c in cs)]
    if not S: continue
    awards={tuple(w[0][p] for p in P) for w in S}
    if len(awards)==1 and len(S)>=2:
        # 至少两条比较句
        if sum('获' in c[0] for c in cs)>=2:
            out.append(([c[0] for c in cs],awards,len(S),[tuple(w[2][p] for p in P) for w in S]))
print(len(out))
import random; random.seed(4)
for o in random.sample(out,min(12,len(out))): print(o)
