from itertools import permutations
def sols_line(names, n, conds):
    out=[]
    for p in permutations(range(1,n+1), len(names)):
        s=dict(zip(names,p))
        if all(c(s) for c in conds): out.append(s)
    return out
fmt=lambda s:' '.join(k for k,v in sorted(s.items(), key=lambda kv:kv[1]))
# V3：1..6 自西向东
N=['凉茶','云吞','肠粉','烧腊','糖水','早茶']
base=[lambda s:s['云吞']==s['凉茶']+1, lambda s:s['肠粉']==s['云吞']+2, lambda s:s['烧腊'] not in (1,6), lambda s:s['糖水']<s['早茶']]
S=sols_line(N,6,base)
print('V3 count',len(S))
for s in S: print('  ',fmt(s))
E=lambda x:7-x  # 从东往西数第几家
from collections import defaultdict
for name in N:
    print(name,'自西向东可能位置',sorted({s[name] for s in S}),'从东往西可能',sorted({E(s[name]) for s in S}))
