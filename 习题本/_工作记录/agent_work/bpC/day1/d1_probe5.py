from itertools import permutations, combinations
def sols_line(names, n, conds):
    out=[]
    for p in permutations(range(1,n+1), len(names)):
        s=dict(zip(names,p))
        if all(c(s) for c in conds): out.append(s)
    return out
fmt=lambda s:' '.join(k for k,v in sorted(s.items(), key=lambda kv:kv[1]))
N=['甲','乙','丙','丁','戊','己']
trials = {
 'T1':[lambda s:abs(s['甲']-s['乙'])==1, lambda s:s['丙']==s['丁']+2, lambda s:abs(s['甲']-s['丁'])==3, lambda s:s['戊']<s['己']],
 'T2':[lambda s:abs(s['甲']-s['乙'])==1, lambda s:s['丙']==s['丁']+3, lambda s:abs(s['甲']-s['丁'])==2, lambda s:s['戊']<s['己']],
 'T3':[lambda s:abs(s['甲']-s['乙'])==1, lambda s:s['丙']-s['丁']==3, lambda s:abs(s['甲']-s['丙'])==2, lambda s:s['戊']>s['乙']],
 'T4':[lambda s:abs(s['甲']-s['乙'])==1, lambda s:s['丁']<s['丙'], lambda s:abs(s['甲']-s['丙'])==3, lambda s:s['丙']-s['戊']==3],
}
for t,conds in trials.items():
    S=sols_line(N,6,conds)
    print(t,len(S))
    for s in S: print('   ',fmt(s))
    inv=[]
    for a,b in combinations(N,2):
        ds={abs(s[a]-s[b]) for s in S}
        if len(ds)==1: inv.append((a,b,ds.pop()))
    print('   invariant distances',inv)
    pos_inv=[(x,S[0][x]) for x in N if len({s[x] for s in S})==1]
    print('   invariant positions',pos_inv)
