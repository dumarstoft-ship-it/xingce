from itertools import permutations, product, combinations
import random
random.seed(3)
# G1-a: 3人3部门，3条猜测（可含否定），"只有一个猜测是错的"，唯一解
P=['甲','乙','丙']; D=['组织部','宣传部','统战部']
W=[dict(zip(P,p)) for p in permutations(D)]
atoms=[(f'{x}去{d}',lambda w,x=x,d=d:w[x]==d) for x in P for d in D]+[(f'{x}不去{d}',lambda w,x=x,d=d:w[x]!=d) for x in P for d in D]
res=[]
for g in combinations(atoms,3):
    if len({a[0][0] for a in g})!=3: continue   # 三句分别说三个人
    S=[w for w in W if sum(a[1](w) for a in g)==2]
    if len(S)==1:
        # 无矛盾/反对关系（三句话说不同的人，天然无矛盾）
        res.append(([a[0] for a in g],S[0]))
print('G1-a 候选数',len(res))
for r in random.sample(res,6): print('  ',r)
# G1-b: 4人4岗，4条猜测（各说不同的人），只有一句真
P4=['甲','乙','丙','丁']; J=['综合','财务','人事','信息']
W4=[dict(zip(P4,p)) for p in permutations(J)]
atoms4=[(f'{x}在{d}岗',lambda w,x=x,d=d:w[x]==d) for x in P4 for d in J]+[(f'{x}不在{d}岗',lambda w,x=x,d=d:w[x]!=d) for x in P4 for d in J]
res4=[]
for trial in range(60000):
    g=random.sample(atoms4,4)
    if len({a[0][0] for a in g})!=4: continue
    S=[w for w in W4 if sum(a[1](w) for a in g)==1]
    if len(S)==1: res4.append(([a[0] for a in g],S[0]))
    if len(res4)>=5: break
print('G1-b 例'); [print('  ',r) for r in res4]
