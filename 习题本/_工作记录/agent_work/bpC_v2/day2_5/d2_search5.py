from itertools import permutations, product, combinations
import random
n=4
rows=list(permutations(range(n)))
LS=[]
for r0 in rows:
    for r1 in rows:
        if any(r0[k]==r1[k] for k in range(n)): continue
        for r2 in rows:
            if any(r2[k] in (r0[k],r1[k]) for k in range(n)): continue
            for r3 in rows:
                if any(r3[k] in (r0[k],r1[k],r2[k]) for k in range(n)): continue
                LS.append((r0,r1,r2,r3))
cells=[(i,m) for i in range(n) for m in range(n)]
def comps(giv, pool=LS): return [L for L in pool if all(L[i][m]==c for (i,m),c in giv.items())]
P=['张','王','李','杨']; C=['广州','深圳','汕头','湛江']
# G2-b：3~4 已知格，多解；候选补充格：恰1个使唯一、1个矛盾、2个仍多解
random.seed(21)
done=0
for trial in range(50000):
    L=random.choice(LS)
    gc=random.sample(cells,4)
    giv={c:L[c[0]][c[1]] for c in gc}
    S=comps(giv)
    if not (3<=len(S)<=5): continue
    cand=[]
    for d in cells:
        if d in giv: continue
        used={v for (a,b),v in giv.items() if a==d[0] or b==d[1]}
        for v in range(n):
            if v in used: continue
            k=len([s for s in S if s[d[0]][d[1]]==v])
            cand.append((d,v,k))
    uniq=[x for x in cand if x[2]==1]; zero=[x for x in cand if x[2]==0]; many=[x for x in cand if x[2]>=2]
    if uniq and zero and len(many)>=2:
        f=lambda x:(f'{P[x[0][0]]}{x[0][1]+1}月在{C[x[1]]}',x[2])
        print('已知',{f'{P[i]}{m+1}月':C[v] for (i,m),v in giv.items()},'完成数',len(S))
        print('  唯一',[f(x) for x in uniq][:5]); print('  矛盾',[f(x) for x in zero][:5]); print('  多解',[f(x) for x in many][:5])
        done+=1
        if done>=3: break
