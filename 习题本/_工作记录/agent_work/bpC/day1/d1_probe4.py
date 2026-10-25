from itertools import permutations
def sols_line(names, n, conds):
    out=[]
    for p in permutations(range(1,n+1), len(names)):
        s=dict(zip(names,p))
        if all(c(s) for c in conds): out.append(s)
    return out
fmt=lambda s:' '.join(k for k,v in sorted(s.items(), key=lambda kv:kv[1]))
N=['甲1','甲2','乙1','乙2','丙1','丙2']
brand=lambda x:x[0]
def notadj_same(s):
    for b in '甲乙丙':
        if abs(s[b+'1']-s[b+'2'])==1: return False
    return True
def ends_same(s):
    at={v:k for k,v in s.items()}
    return brand(at[1])==brand(at[6])
base=[notadj_same, ends_same, lambda s:s['乙1']<s['甲1']]
S=sols_line(N,6,base)
print('base',len(S))
for extra_name, extra in [('丙1在3号',lambda s:s['丙1']==3), ('甲1在4号',lambda s:s['甲1']==4), ('乙2在2号',lambda s:s['乙2']==2), ('丙2在5号',lambda s:s['丙2']==5)]:
    sub=[s for s in S if extra(s)]
    print(extra_name,len(sub))
    for s in sub: print('   ',fmt(s))
