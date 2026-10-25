from itertools import permutations, combinations, product
import random
random.seed(5)
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
print('4阶拉丁方个数',len(LS))
P=['张','王','李','杨']; C=['广州','深圳','汕头','湛江']
cells=[(i,m) for i in range(n) for m in range(n)]
def comps(giv):
    return [L for L in LS if all(L[i][m]==c for (i,m),c in giv.items())]
# (a) 4~5 个已知格，完成方式 2~3 种，且存在非已知的"必然格"
random.seed(2)
cnt=0
for trial in range(4000):
    L=random.choice(LS)
    k=random.choice([4,5])
    gc=random.sample(cells,k)
    # 每人至多出现2个已知格，避免过于直接
    giv={c:L[c[0]][c[1]] for c in gc}
    S=comps(giv)
    if not (2<=len(S)<=3): continue
    fixed=[c for c in cells if c not in giv and len({s[c[0]][c[1]] for s in S})==1]
    if len(fixed)!=1: continue
    poss=[(c,v) for c in cells if c not in giv for v in range(n) if any(s[c[0]][c[1]]==v for s in S) and not all(s[c[0]][c[1]]==v for s in S)]
    imp=[(c,v) for c in cells if c not in giv for v in range(n) if not any(s[c[0]][c[1]]==v for s in S)]
    print('已知',{f'{P[i]}{m+1}月':C[v] for (i,m),v in giv.items()},'完成数',len(S),'必然格',[(f'{P[c[0]]}{c[1]+1}月',C[S[0][c[0]][c[1]]]) for c in fixed])
    cnt+=1
    if cnt>=6: break
