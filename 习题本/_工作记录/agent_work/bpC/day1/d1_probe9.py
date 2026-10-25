from itertools import permutations
P=['甲','乙','丙','丁','戊','己']
def sols(conds):
    out=[]
    for p in permutations(range(1,7)):
        r=dict(zip(P,p))
        if all(c(r) for c in conds): out.append(r)
    return out
base=[lambda r:r['甲']<r['乙']<r['丙'], lambda r:r['戊']<r['丁']<r['丙'], lambda r:r['甲']<r['戊']]
S=sols(base); print('base',len(S))
cands={
 '己第一':lambda r:r['己']==1,
 '己最后':lambda r:r['己']==6,
 '乙比戊低':lambda r:r['乙']>r['戊'],
 '乙比丁低':lambda r:r['乙']>r['丁'],
 '己比丙低':lambda r:r['己']>r['丙'],
 '己比甲高':lambda r:r['己']<r['甲'],
 '乙比戊高且己比丙低':lambda r:r['乙']<r['戊'] and r['己']>r['丙'],
 '丁第四':lambda r:r['丁']==4,
 '己比乙高且比戊低': lambda r: r['己']<r['乙'] and r['己']>r['戊'],
 '己与乙相邻且比乙高': lambda r: r['己']==r['乙']-1,
}
for k,f in cands.items():
    sub=[r for r in S if f(r)]
    print(k,len(sub),'乙名次',sorted({r['乙'] for r in sub}),'己名次',sorted({r['己'] for r in sub}))
