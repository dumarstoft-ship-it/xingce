from itertools import permutations, combinations
import random
random.seed(7)
T=['管网改造','道路修复','绿化提升','立面整治']
P=['甲','乙','丙','丁']
res=[]
for trial in range(200000):
    W=random.sample([60,72,90,120,144,180],4)
    E=random.sample([12,15,18,20,24,30,36],4)
    tasks=dict(zip(T,W)); eff=dict(zip(P,E))
    # 所有天数为整数
    if any(w%e for w in W for e in E): continue
    bans=random.sample([(p,t) for p in P for t in T],3)
    allv=[]
    for p in permutations(T):
        a=dict(zip(P,p))
        if any((x,a[x]) in bans for x in P): continue
        days=[tasks[a[x]]//eff[x] for x in P]
        allv.append((max(days),sum(days),a))
    if len(allv)<4: continue
    allv.sort(key=lambda x:x[0])
    if allv[0][0]==allv[1][0]: continue
    # 贪心陷阱：最大工作量给最高效率者 是否被禁止或非最优
    res.append((tasks,eff,bans,allv[0],allv[1][0]))
print(len(res))
for r in res[:15]: print(r)
