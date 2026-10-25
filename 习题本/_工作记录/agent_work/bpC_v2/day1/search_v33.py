# 搜索：方桌东南西北 + 面向桌心左右手；正确口径唯一解，左右画反时得到另一个唯一解（形成陷阱选项）
from itertools import permutations, combinations
D=['北','东','南','西']   # 俯视顺时针
P=['甲','乙','丙','丁']
def leftof(i, conv):   # 面向桌心时的左手边
    return (i+1)%4 if conv=='ok' else (i-1)%4
conds=[]
for x in P:
    for d in range(4):
        conds.append((f'{x}坐{D[d]}面', lambda s,x=x,d=d,c=None: s[x]==d))
        conds.append((f'{x}不坐{D[d]}面', lambda s,x=x,d=d,c=None: s[x]!=d))
for x in P:
    for y in P:
        if x==y: continue
        conds.append((f'{x}坐在{y}的左手边', lambda s,x=x,y=y,c='ok': None))
def ev(name, s, conv):
    # 重新解析，便于区分口径
    import re
    m=re.match(r'(.)坐在(.)的左手边', name)
    if m: x,y=m.groups(); return s[x]==leftof(s[y],conv)
    m=re.match(r'(.)坐在(.)的右手边', name)
    if m: x,y=m.groups(); return s[y]==leftof(s[x],conv)
    m=re.match(r'(.)坐在(.)的对面', name)
    if m: x,y=m.groups(); return (s[x]-s[y])%4==2
    m=re.match(r'(.)不坐(.)面', name)
    if m: x,d=m.groups(); return s[x]!=D.index(d)
    m=re.match(r'(.)坐(.)面', name)
    if m: x,d=m.groups(); return s[x]==D.index(d)
    raise
names=[]
for x in P:
    for d in D:
        names.append(f'{x}不坐{d}面')
for x,y in permutations(P,2):
    names.append(f'{x}坐在{y}的左手边'); names.append(f'{x}坐在{y}的右手边')
for x,y in combinations(P,2):
    names.append(f'{x}坐在{y}的对面')
seats=[dict(zip(P,p)) for p in permutations(range(4))]
found=[]
for k in (3,):
    for cs in combinations(names,k):
        # 至少一条左右手条件、至少一条方位条件
        if not any('手边' in c for c in cs) or not any('面' in c and '手边' not in c and '对面' not in c for c in cs): continue
        ok=[s for s in seats if all(ev(c,s,'ok') for c in cs)]
        if len(ok)!=1: continue
        bad=[s for s in seats if all(ev(c,s,'rev') for c in cs)]
        if len(bad)!=1 or bad[0]==ok[0]: continue
        found.append((cs, ok[0], bad[0]))
print(len(found))
import random
random.seed(1)
for cs,o,b in random.sample(found, min(25,len(found))):
    print(cs, {x:D[o[x]] for x in P}, '| 画反:', {x:D[b[x]] for x in P})
