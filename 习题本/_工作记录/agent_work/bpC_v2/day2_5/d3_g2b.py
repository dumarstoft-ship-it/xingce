from itertools import combinations, product
M=['赵','钱','孙']; F=['李','刘','王','吴']
ALL=M+F
base=[ {*m,*f} for m in combinations(M,2) for f in combinations(F,2)]
conds=[]
for x in ALL:
    for y in ALL:
        if x==y: continue
        conds.append((f'如果推选{x}，那么推选{y}', lambda s,x=x,y=y: (x not in s) or (y in s)))
        conds.append((f'如果推选{x}，那么不推选{y}', lambda s,x=x,y=y: (x not in s) or (y not in s)))
found=[]
for c1,c2 in combinations(conds,2):
    S=[s for s in base if c1[1](s) and c2[1](s)]
    if len(S)<4: continue
    pairs=list(combinations(ALL,2))
    imp=[p for p in pairs if not any(set(p)<=s for s in S)]
    # 不能是条件句直接禁止的（x->not y 的那对）
    direct=set()
    for c in (c1,c2):
        if '不推选' in c[0]:
            x=c[0][4]; y=c[0][-1]; direct.add(frozenset((x,y)))
    imp=[p for p in imp if frozenset(p) not in direct and not (p[0] in M and p[1] in M and False)]
    # 排除两男两女名额直接导致的（不存在：任意两人都可同时入选）
    if len(imp)==1:
        found.append((c1[0],c2[0],imp,len(S)))
print(len(found))
for f in found[:20]: print(f)
print('----- 混合对')
mixed=[f for f in found if (f[2][0][0] in M) != (f[2][0][1] in M) and '不推选' not in f[0] and '不推选' not in f[1]]
print(len(mixed))
for f in mixed[:40]: print(f)
