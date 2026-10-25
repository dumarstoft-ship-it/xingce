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
P=['甲','乙','丙','丁']; COL=['红','黄','蓝','绿']
pool=[L for L in LS if L[0]==(0,1,2,3)]
print('甲行固定后拉丁方数',len(pool))
random.seed(13)
rels_all=[(i,a,j,b) for i in range(4) for a in range(4) for j in range(4) for b in range(4) if i!=j and a!=b]
for trial in range(20000):
    T=random.choice(pool)
    rels=[r for r in rels_all if T[r[0]][r[1]]==T[r[2]][r[3]]]
    pick=random.sample(rels,3)
    if any(r[0]==0 and r[2]==0 for r in pick): continue
    S=[L for L in pool if all(L[i][a]==L[j][b] for i,a,j,b in pick)]
    if len(S)!=2: continue
    # 选项：乙/丙/丁的颜色序列；恰一个出现在某个解中（可能），其余三个不出现、且与甲行逐轮不冲突
    possible_rows={(k,S[s][k]) for s in range(len(S)) for k in (1,2,3)}
    good=[(k,r) for (k,r) in possible_rows]
    bad=[(k,r) for k in (1,2,3) for r in rows if all(r[m]!=m for m in range(4)) and (k,r) not in possible_rows]
    print('关系',[f'{P[i]}第{a+1}轮=与{P[j]}第{b+1}轮相同' for i,a,j,b in pick])
    for s in S: print('   解',{P[k]:''.join(COL[v] for v in s[k]) for k in range(4)})
    break
