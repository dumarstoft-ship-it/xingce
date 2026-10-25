from itertools import combinations, product
from collections import defaultdict
T=['甲','乙','丙','丁']
M=list(combinations(T,2))
res=defaultdict(list)
for out in product('WDL', repeat=len(M)):   # W: first wins
    pts={t:0 for t in T}; rec={t:[0,0,0] for t in T}
    for (a,b),o in zip(M,out):
        if o=='W': pts[a]+=3; rec[a][0]+=1; rec[b][2]+=1
        elif o=='L': pts[b]+=3; rec[b][0]+=1; rec[a][2]+=1
        else: pts[a]+=1; pts[b]+=1; rec[a][1]+=1; rec[b][1]+=1
    key=tuple(pts[t] for t in T)
    res[key].append(dict(zip(M,out)))
# 积分各不相同且按甲>乙>丙>丁 的组合
cands=[k for k in res if k[0]>k[1]>k[2]>k[3]]
print(len(cands))
for k in sorted(cands, key=lambda k:(-k[0],-k[1])):
    outs=res[k]
    # 每场结果是否唯一
    det={m:{o[m] for o in outs} for m in M}
    fixed=sum(1 for m in M if len(det[m])==1)
    draws={sum(1 for m in M if o[m]=='D') for o in outs}
    print(k,'方案数',len(outs),'确定场次',fixed,'平局数',draws)
