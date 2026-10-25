from itertools import permutations
def sols(P,n,conds):
    out=[]
    for p in permutations(range(1,n+1),len(P)):
        r=dict(zip(P,p))
        if all(c(r) for c in conds): out.append(r)
    return out
fmt=lambda s:' '.join(k for k,v in sorted(s.items(), key=lambda kv:kv[1]))
# V10
P=['甲','乙','丙','丁','戊','己','庚']
S=sols(P,7,[lambda r:r['甲']<r['乙']<r['丙']<r['丁']<r['戊'], lambda r:r['甲']<r['己']<r['丙'], lambda r:r['庚']>r['丁']])
print('V10',len(S),[fmt(s) for s in S])
det=[x for x in P if len({s[x] for s in S})==1]; print('determined',det)
# V11
P=['发改','财政','人社','住建','交通','文旅']
base=[lambda r:r['财政']==r['发改']+2, lambda r:r['住建']==r['人社']+1, lambda r:r['交通'] not in (1,6), lambda r:r['文旅']<r['财政']]
S=sols(P,6,base); print('V11 base',len(S),[fmt(s) for s in S])
S1=[s for s in S if s['发改']==1]; print('if 发改1',[fmt(s) for s in S1])
for x in P: print('  ',x,sorted({s[x] for s in S1}))
S2=[s for s in S if s['交通']==2]; print('if 交通2',[fmt(s) for s in S2])
