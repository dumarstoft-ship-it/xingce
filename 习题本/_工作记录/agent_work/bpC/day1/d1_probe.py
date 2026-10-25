from itertools import permutations, product, combinations
def sols_line(names, n, conds):
    out=[]
    for p in permutations(range(1,n+1), len(names)):
        s=dict(zip(names,p))
        if all(c(s) for c in conds): out.append(s)
    return out

# V1：窗口 必然->可能
N=['社保','医保','税务','公积金','不动产','户政']
S=sols_line(N,6,[lambda s:s['税务']==s['社保']+1, lambda s:s['公积金']-s['税务']>=2, lambda s:abs(s['医保']-s['户政'])==3, lambda s:s['不动产']==6])
print('V1',S)

# V2：补条件唯一确定（基础条件）
N=['A','B','C','D','E','F']
base=[lambda s:s['A']==s['B']+1, lambda s:s['C']-s['A']>=2, lambda s:abs(s['D']-s['E'])==2]
S=sols_line(N,6,base)
print('V2 base count',len(S))
cands={
 'F在最左端':lambda s:s['F']==1,
 'D在最右端':lambda s:s['D']==6,
 'E与B相邻':lambda s:abs(s['E']-s['B'])==1,
 'C在5号':lambda s:s['C']==5,
 'F在最右端':lambda s:s['F']==6,
 'B在最左端':lambda s:s['B']==1,
 'C在最右端':lambda s:s['C']==6,
 'D与C相邻':lambda s:abs(s['D']-s['C'])==1,
 'E在3号':lambda s:s['E']==3,
 'F与A相邻':lambda s:abs(s['F']-s['A'])==1,
 'B在2号':lambda s:s['B']==2,
 'D在1号且F在6号':lambda s:s['D']==1 and s['F']==6,
 'F在3号':lambda s:s['F']==3,
 'A在4号':lambda s:s['A']==4,
 'E在6号':lambda s:s['E']==6,
}
for k,f in cands.items():
    sub=[s for s in S if f(s)]
    # 唯一确定：在满足的解中，所有对象位置唯一（不区分对称）
    print('  ',k,len(sub), sub if len(sub)<=2 else '')
