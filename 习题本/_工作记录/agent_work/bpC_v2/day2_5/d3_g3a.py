from itertools import product, combinations
NEW=['甲','乙','丙']; OLD=['张','李','王']; PP=NEW+OLD; PT='ABCD'
def base_ok(s):
    for p in PT:
        here=[x for x in PP if s[x]==p]
        if len(here)>2: return False                     # 每个点最多2人
        if any(x in NEW for x in here) and not any(x in OLD for x in here): return False
    return True
W=[dict(zip(PP,a)) for a in product(PT,repeat=6)]
W=[s for s in W if base_ok(s)]
print('基础世界',len(W))
fixed=[lambda s:s['张'] in 'AB', lambda s:s['乙']=='D', lambda s:s['甲']!='A']
W2=[s for s in W if all(f(s) for f in fixed)]
print('固定条件后',len(W2))
for x in PP:
    for p in PT:
        S=[s for s in W2 if s[x]==p]
        if not S: continue
        musts=[(y,q) for y in PP for q in PT if y!=x and all(s[y]==q for s in S)]
        if 1<=len(musts)<=2: print(f'如果{x}去{p}', len(S), musts)
