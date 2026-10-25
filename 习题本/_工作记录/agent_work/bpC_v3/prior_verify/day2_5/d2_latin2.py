from itertools import permutations
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
P=['张','王','李','杨']; C=['广州','深圳','汕头','湛江']
cells=[(i,m) for i in range(n) for m in range(n)]
def comps(giv): return [L for L in LS if all(L[i][m]==c for (i,m),c in giv.items())]
def cand(giv,c):
    i,m=c
    used={v for (a,b),v in giv.items() if a==i or b==m}
    return [v for v in range(n) if v not in used]
random.seed(9)
out=[]
for trial in range(20000):
    L=random.choice(LS)
    gc=random.sample(cells,5)
    giv={c:L[c[0]][c[1]] for c in gc}
    S=comps(giv)
    if not (2<=len(S)<=3): continue
    fixed=[c for c in cells if c not in giv and len({s[c[0]][c[1]] for s in S})==1]
    fixed=[c for c in fixed if len(cand(giv,c))>=2]
    if len(fixed)!=1: continue
    c=fixed[0]
    # 选项：必然格(真)、两个"可能非必然"、一个"不可能但不与已知格直接冲突"
    poss=[(d,v) for d in cells if d not in giv and d!=c for v in range(n) if any(s[d[0]][d[1]]==v for s in S) and not all(s[d[0]][d[1]]==v for s in S)]
    imp=[(d,v) for d in cells if d not in giv for v in cand(giv,d) if not any(s[d[0]][d[1]]==v for s in S)]
    if len(poss)<2 or not imp: continue
    out.append((giv,S,c,poss,imp))
    if len(out)>=5: break
for giv,S,c,poss,imp in out:
    print('已知',{f'{P[i]}{m+1}月':C[v] for (i,m),v in giv.items()},'完成数',len(S))
    print('   必然格',f'{P[c[0]]}{c[1]+1}月',C[S[0][c[0]][c[1]]],'| 可能(非必然)例',[(f'{P[d[0]]}{d[1]+1}月',C[v]) for d,v in poss[:4]],'| 不可能例',[(f'{P[d[0]]}{d[1]+1}月',C[v]) for d,v in imp[:4]])
    for s in S: print('     ', {P[i]:[C[v] for v in s[i]] for i in range(n)})
