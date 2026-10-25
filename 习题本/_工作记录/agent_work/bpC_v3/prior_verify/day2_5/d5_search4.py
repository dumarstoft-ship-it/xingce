from itertools import permutations, product, combinations
import random
random.seed(12)
P=['甲','乙','丙']
W=[dict(zip(P,p)) for p in permutations([1,2,3])]
perms=list(permutations([1,2,3]))
out=[]
for vs in combinations(perms,3):
    S=[w for w in W if all(sum(w[P[i]]==vw[i] for i in range(3))==1 for vw in vs)]
    if len(S)==1: out.append((vs,S))
print('G2-a(全排列猜测) 唯一解组合数',len(out))
for o in out[:6]: print('  ',o)
P4=['甲','乙','丙','丁']
W4=[dict(zip(P4,p)) for p in permutations([1,2,3,4])]
perms4=list(permutations([1,2,3,4]))
cnt=0; res=[]
for trial in range(300000):
    vs=random.sample(perms4,4)
    S=[]
    for w in W4:
        c=[sum(w[P4[i]]==vw[i] for i in range(4)) for vw in vs]
        if sorted(c)==[0,1,1,1]: S.append((tuple(w[x] for x in P4),c.index(0)))
    if 1<=len(S)<=2:
        res.append((vs,S))
        if len(res)>=6: break
print('G2-b')
for r in res: print('  ',r)
