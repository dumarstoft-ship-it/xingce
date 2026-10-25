from itertools import product, combinations
T4=['甲','乙','丙','丁']
games=list(combinations(range(4),2))
valid=set()
for res in product('WDL',repeat=6):
    p=[0]*4
    for (a,b),r in zip(games,res):
        if r=='W': p[a]+=3
        elif r=='L': p[b]+=3
        else: p[a]+=1; p[b]+=1
    valid.add(tuple(p))
print('合法积分表数', len(valid))
good=[]
for rep in product(range(10),repeat=4):
    if list(rep)!=sorted(rep,reverse=True) or len(set(rep))<4: continue
    if rep in valid: continue
    cand=[(i,v) for i in range(4) for v in range(10) if v!=rep[i] and tuple(rep[:i])+(v,)+tuple(rep[i+1:]) in valid]
    teams={i for i,v in cand}
    if len(teams)==1:
        good.append((rep,cand))
for g in good[:40]: print(g)
print(len(good))
