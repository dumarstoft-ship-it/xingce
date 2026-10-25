from itertools import permutations, product, combinations
import random
P4=['甲','乙','丙','丁']; J=['综合','财务','人事','信息']
W4=[dict(zip(P4,p)) for p in permutations(J)]
per={x:[(f'{x}在{d}岗',lambda w,x=x,d=d:w[x]==d) for d in J]+[(f'{x}不在{d}岗',lambda w,x=x,d=d:w[x]!=d) for d in J] for x in P4}
res=[];res3=[]
for g in product(*[per[x] for x in P4]):
    S=[w for w in W4 if sum(a[1](w) for a in g)==1]
    if len(S)==1: res.append(([a[0] for a in g],S[0]))
    S3=[w for w in W4 if sum(a[1](w) for a in g)==3]
    if len(S3)==1: res3.append(([a[0] for a in g],S3[0]))
print('只有一句真 唯一',len(res)); 
random.seed(5)
for r in random.sample(res,min(8,len(res))): print('  ',r)
print('只有一句假 唯一',len(res3))
for r in random.sample(res3,min(5,len(res3))): print('  ',r)
