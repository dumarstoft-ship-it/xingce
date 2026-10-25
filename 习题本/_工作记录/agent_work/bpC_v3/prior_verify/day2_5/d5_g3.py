# 一拖二·条件句预测：3个社区(A,B,C)各选派1人，类别 党员D/退役军人T/志愿者Z（可重复）
from itertools import product, combinations, permutations
import random
U=['A','B','C']; K=['党员','退役军人','志愿者']
W=[dict(zip(U,p)) for p in product(K,repeat=3)]
def atom(u,k,neg=False):
    return (f'{u}社区{"不" if neg else ""}选派{k}', (lambda w,u=u,k=k,neg=neg:(w[u]!=k) if neg else (w[u]==k)))
atoms=[atom(u,k) for u in U for k in K]+[atom(u,k,True) for u in U for k in K]
def mk_imp(p,q): return (f'如果{p[0]}，那么{q[0]}', lambda w,p=p,q=q:(not p[1](w)) or q[1](w))
def mk_only(p,q): return (f'只有{q[0]}，{p[0]}', lambda w,p=p,q=q:(not p[1](w)) or q[1](w))   # p -> q
def mk_unless(p,q): return (f'除非{p[0]}，否则{q[0]}', lambda w,p=p,q=q: p[1](w) or q[1](w))
random.seed(17)
best=None
for trial in range(30000):
    a=random.sample([x for x in atoms if '不' not in x[0]],6)
    preds=[mk_imp(a[0],a[1]), mk_only(a[2],a[3]), mk_unless(a[4],a[5])]
    # 不同社区交叉
    S=[w for w in W if all(p[1](w) for p in preds)]
    S1=[w for w in S if len(set(w.values()))==3]
    if not (1<=len(S1)<=2): continue
    # Q1选项：两条事实；恰1个与S1中某解相容(符合)
    facts=[(f'{u}社区选派{k}',lambda w,u=u,k=k:w[u]==k) for u in U for k in K]
    combos=[(f1,f2) for f1,f2 in combinations(facts,2) if f1[0][0]!=f2[0][0]]
    # 选项必须本身是"三类各不相同"可实现的
    def realizable(fs):
        return any(all(f[1](w) for f in fs) and len(set(w.values()))==3 for w in W)
    good=[c for c in combos if realizable(c) and any(all(f[1](w) for f in c) for w in S1)]
    bad=[c for c in combos if realizable(c) and not any(all(f[1](w) for f in c) for w in S1)]
    if len(good)<1 or len(bad)<3: continue
    # Q2：附加事实X，问"不符合预测"——恰1个选项(单条事实)与 S∧X 不相容
    ok2=None
    for X in facts:
        SX=[w for w in S if X[1](w)]
        if len(SX)<2: continue
        cand=[f for f in facts if f[0][0]!=X[0][0]]
        viol=[f for f in cand if not any(f[1](w) for w in SX)]
        fine=[f for f in cand if any(f[1](w) for w in SX)]
        if len(viol)>=1 and len(fine)>=3:
            ok2=(X,viol,fine); break
    if not ok2: continue
    best=(preds,S,S1,good,bad,ok2); break
preds,S,S1,good,bad,(X,viol,fine)=best
print('预测：'); [print('  ',p[0]) for p in preds]
print('全部符合预测的情况',len(S),S)
print('各不相同时',S1)
print('Q1 符合的选项例',[ (c[0][0],c[1][0]) for c in good][:3])
print('Q1 不符合的选项例',[ (c[0][0],c[1][0]) for c in bad][:6])
print('Q2 附加',X[0],'不符合',[f[0] for f in viol],'符合',[f[0] for f in fine])
