import sys; sys.path.insert(0,'..')
from lib import *
from itertools import permutations, product, combinations
import random
N=['会展','大学城','科技园','湿地','古镇','港口']
def templ():
    out=[]
    for a,b in permutations(N,2):
        out.append((f'{a}站在{b}站北边且相邻',lambda s,a=a,b=b:s[a]-s[b]==1))
        out.append((f'{a}站在{b}站北边，两站中间隔一站',lambda s,a=a,b=b:s[a]-s[b]==2))
        out.append((f'{a}站在{b}站北边，两站中间隔两站',lambda s,a=a,b=b:s[a]-s[b]==3))
        out.append((f'{a}站在{b}站北边',lambda s,a=a,b=b:s[a]>s[b]))
    for a,b in combinations(N,2):
        out.append((f'{a}站与{b}站相邻',lambda s,a=a,b=b:abs(s[a]-s[b])==1))
        out.append((f'{a}站与{b}站之间隔一站',lambda s,a=a,b=b:abs(s[a]-s[b])==2))
    for a in N:
        out.append((f'{a}站不在两端',lambda s,a=a:s[a] not in (1,6)))
    return out
T=templ()
random.seed(3)
found=0
for trial in range(200000):
    cs=random.sample(T,4)
    names=[c[0] for c in cs]
    if sum('不在两端' in n for n in names)>1: continue
    S=line(N,6,[c[1] for c in cs])
    if not (3<=len(S)<=5): continue
    fixed=[x for x in N if len({s[x] for s in S})==1]
    if len(fixed)!=2: continue
    # 小题2：附加某相邻条件后问"不可能"
    found+=1
    print(names,'解数',len(S),'确定',fixed)
    for s in S: print('     ',fmt_line(s))
    if found>=5: break
