from itertools import permutations
def sols_line(names, n, conds):
    out=[]
    for p in permutations(range(1,n+1), len(names)):
        s=dict(zip(names,p))
        if all(c(s) for c in conds): out.append(s)
    return out
fmt=lambda s:' '.join(k for k,v in sorted(s.items(), key=lambda kv:kv[1]))
N=['甲','乙','丙','丁','戊','己']
tr={
 'P1':[lambda s:s['乙']==s['甲']+1, lambda s:abs(s['丙']-s['丁'])==2, lambda s:s['戊'] not in (1,6)],
 'P2':[lambda s:s['乙']==s['甲']+1, lambda s:abs(s['丙']-s['丁'])==2, lambda s:s['戊'] not in (1,6), lambda s:abs(s['己']-s['乙'])>1],
 'P3':[lambda s:s['乙']==s['甲']+1, lambda s:s['丁']-s['丙']==2, lambda s:s['戊'] in (1,6), lambda s:s['己']>s['乙']],
}
for t,c in tr.items():
    S=sols_line(N,6,c); print(t,len(S))
N5=['甲','乙','丙','丁','戊']
S=sols_line(N5,5,[lambda s:s['甲']==3, lambda s:abs(s['乙']-s['丙'])==1, lambda s:abs(s['丁']-s['甲'])!=1])
print('5seat',len(S),[fmt(s) for s in S])
