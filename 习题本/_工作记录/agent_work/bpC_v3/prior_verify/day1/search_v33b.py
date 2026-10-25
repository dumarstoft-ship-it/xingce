from itertools import permutations, combinations
import random, re
D=['北','东','南','西']
P=['甲','乙','丙','丁']
def leftof(i, conv): return (i+1)%4 if conv=='ok' else (i-1)%4
def ev(name, s, conv):
    m=re.match(r'(.)坐在(.)的左手边$', name)
    if m: x,y=m.groups(); return s[x]==leftof(s[y],conv)
    m=re.match(r'(.)坐在(.)的右手边$', name)
    if m: x,y=m.groups(); return s[y]==leftof(s[x],conv)
    m=re.match(r'(.)坐在(.)的对面$', name)
    if m: x,y=m.groups(); return (s[x]-s[y])%4==2
    m=re.match(r'(.)不坐(.)面$', name)
    if m: x,d=m.groups(); return s[x]!=D.index(d)
    m=re.match(r'(.)坐(.)面或(.)面$', name)
    if m: x,d1,d2=m.groups(); return s[x] in (D.index(d1),D.index(d2))
    raise Exception(name)
names=[]
for x in P:
    for d in D: names.append(f'{x}不坐{d}面')
    for d1,d2 in combinations(D,2): names.append(f'{x}坐{d1}面或{d2}面')
for x,y in permutations(P,2):
    names.append(f'{x}坐在{y}的左手边'); names.append(f'{x}坐在{y}的右手边')
for x,y in combinations(P,2): names.append(f'{x}坐在{y}的对面')
seats=[dict(zip(P,p)) for p in permutations(range(4))]
found=[]
for k in (3,):
    for cs in combinations(names,k):
        nh=sum('手边' in c for c in cs); nd=sum(('不坐' in c or '或' in c) for c in cs)
        if nh!=1 or nd<1: continue
        ok=[s for s in seats if all(ev(c,s,'ok') for c in cs)]
        if len(ok)!=1: continue
        bad=[s for s in seats if all(ev(c,s,'rev') for c in cs)]
        if len(bad)!=1 or bad[0]==ok[0]: continue
        # 每个人只被提到少量
        found.append((cs, ok[0], bad[0]))
print(len(found))
random.seed(3)
for cs,o,b in random.sample(found, min(30,len(found))):
    print(cs, {x:D[o[x]] for x in P}, '| 画反:', {x:D[b[x]] for x in P})
