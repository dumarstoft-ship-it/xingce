from itertools import permutations, product, combinations
import random
# G2-d 施工队×周×标段：条件=2个已知格(以"某标段某周是某队"或"某队某周在某标段"表述)+1个关联+1个否定；问不可能
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
TM=['甲','乙','丙','丁']; SEC=['一','二','三','四']
cells=[(i,w) for i in range(4) for w in range(4)]
random.seed(31)
found=0
for trial in range(100000):
    T=random.choice(LS)
    g=random.sample(cells,2)
    rels=[(i,a,j,b) for i in range(4) for a in range(4) for j in range(4) for b in range(4) if i!=j and a!=b and T[i][a]==T[j][b]]
    r=random.choice(rels)
    negs=[(i,w,v) for i in range(4) for w in range(4) for v in range(4) if T[i][w]!=v]
    ng=random.choice(negs)
    def ok(L):
        return all(L[i][w]==T[i][w] for i,w in g) and L[r[0]][r[1]]==L[r[2]][r[3]] and L[ng[0]][ng[1]]!=ng[2]
    S=[L for L in LS if ok(L)]
    if not (3<=len(S)<=4): continue
    # 候选选项：某队某周在某标段（与已知格不直接冲突）
    def direct_conflict(i,w,v):
        for gi,gw in g:
            if (gi==i and gw==w and T[gi][gw]!=v) or (gi==i and gw!=w and T[gi][gw]==v) or (gw==w and gi!=i and T[gi][gw]==v): return True
        return False
    imp=[(i,w,v) for i in range(4) for w in range(4) for v in range(4) if not direct_conflict(i,w,v) and (i,w)!=(ng[0],ng[1]) and not any(L[i][w]==v for L in S)]
    pos=[(i,w,v) for i in range(4) for w in range(4) for v in range(4) if any(L[i][w]==v for L in S) and not all(L[i][w]==v for L in S)]
    if len(imp)<1 or len(pos)<3: continue
    print('已知格',[f'{TM[i]}队第{w+1}周在{SEC[T[i][w]]}标段' for i,w in g],'| 关联',f'{TM[r[0]]}队第{r[1]+1}周所在标段=就是{TM[r[2]]}队第{r[3]+1}周所在标段','| 否定',f'{TM[ng[0]]}队第{ng[1]+1}周不在{SEC[ng[2]]}标段','| 解数',len(S))
    print('   不可能(非直接冲突)',[f'{TM[i]}队第{w+1}周在{SEC[v]}标段' for i,w,v in imp][:6])
    print('   可能',[f'{TM[i]}队第{w+1}周在{SEC[v]}标段' for i,w,v in pos][:6])
    for L in S: print('     ',{TM[i]:''.join(SEC[v] for v in L[i]) for i in range(4)})
    found+=1
    if found>=2: break
