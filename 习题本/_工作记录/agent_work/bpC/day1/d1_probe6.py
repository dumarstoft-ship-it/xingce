from itertools import permutations
def sols_line(names, n, conds):
    out=[]
    for p in permutations(range(1,n+1), len(names)):
        s=dict(zip(names,p))
        if all(c(s) for c in conds): out.append(s)
    return out
N=['甲','乙','丙','丁','戊','己','庚']
trials={
 'A':[lambda s:abs(s['甲']-s['乙'])==3, lambda s:s['丁']==s['丙']+1, lambda s:abs(s['戊']-s['己'])==2, lambda s:s['庚'] not in (1,7)],
 'B':[lambda s:abs(s['甲']-s['乙'])==3, lambda s:s['丁']==s['丙']+1, lambda s:abs(s['戊']-s['己'])==2, lambda s:s['庚'] in (1,7)],
 'C':[lambda s:abs(s['甲']-s['乙'])==4, lambda s:s['丁']==s['丙']+2, lambda s:abs(s['戊']-s['己'])==3, lambda s:abs(s['庚']-s['甲'])==1],
 'D':[lambda s:abs(s['甲']-s['乙'])==4, lambda s:abs(s['丙']-s['丁'])==3, lambda s:abs(s['戊']-s['己'])==2],
}
for t,conds in trials.items():
    S=sols_line(N,7,conds)
    print(t,len(S))
    for x in N:
        print('   ',x,sorted({s[x] for s in S}))
