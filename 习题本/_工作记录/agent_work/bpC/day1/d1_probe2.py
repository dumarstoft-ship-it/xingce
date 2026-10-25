from itertools import permutations
def sols_line(names, n, conds):
    out=[]
    for p in permutations(range(1,n+1), len(names)):
        s=dict(zip(names,p))
        if all(c(s) for c in conds): out.append(s)
    return out
N=['A','B','C','D','E','F']
base=[lambda s:s['A']==s['B']+1, lambda s:s['C']-s['A']>=2, lambda s:s['E']==s['D']+2]
S=sols_line(N,6,base)
print('V2 base count',len(S))
for s in S: print('   ', ''.join(k for k,v in sorted(s.items(), key=lambda kv:kv[1])))
cands={
 'F在最左端':lambda s:s['F']==1, 'D在最右端':lambda s:s['D']==6, 'E在最右端':lambda s:s['E']==6,
 'C在5号':lambda s:s['C']==5, 'F在最右端':lambda s:s['F']==6, 'B在最左端':lambda s:s['B']==1,
 'C在最右端':lambda s:s['C']==6, 'D与C相邻':lambda s:abs(s['D']-s['C'])==1, 'E在3号':lambda s:s['E']==3,
 'F与A相邻':lambda s:abs(s['F']-s['A'])==1, 'B在2号':lambda s:s['B']==2, 'F在3号':lambda s:s['F']==3,
 'D在1号':lambda s:s['D']==1, 'E与C相邻':lambda s:abs(s['E']-s['C'])==1, 'F与D相邻':lambda s:abs(s['F']-s['D'])==1,
 'D在A右边':lambda s:s['D']>s['A'], 'F在B左边':lambda s:s['F']<s['B'], 'C在E左边':lambda s:s['C']<s['E'],
}
for k,f in cands.items():
    sub=[s for s in S if f(s)]
    print('  ',k,len(sub), [''.join(x for x,v in sorted(s.items(), key=lambda kv:kv[1])) for s in sub])
