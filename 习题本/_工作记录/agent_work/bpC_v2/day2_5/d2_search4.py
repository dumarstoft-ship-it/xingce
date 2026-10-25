from itertools import permutations, product, combinations
import random
# G1-d：4x4/5x5 熟悉表，恰2个完美匹配；候选补充信息
def matchings(tab, P, T):
    out=[]
    for p in permutations(T):
        if all(p[i] in tab[P[i]] for i in range(len(P))): out.append(dict(zip(P,p)))
    return out
P=['甲','乙','丙','丁','戊']; T=['登记','咨询','审核','发证','回访']
random.seed(4)
for trial in range(200000):
    tab={x:set(random.sample(T,random.choice([2,2,3]))) for x in P}
    M=matchings(tab,P,T)
    if len(M)!=2: continue
    diff=[x for x in P if M[0][x]!=M[1][x]]
    if len(diff)<3: continue   # 至少三人互相牵连
    # 候选补充信息："X不熟悉Y"（Y原本在X熟悉范围内）
    opts=[]
    for x in P:
        for y in tab[x]:
            t2={k:set(v) for k,v in tab.items()}; t2[x].discard(y)
            n=len(matchings(t2,P,T)); opts.append((f'{x}不熟悉{y}',n))
    uniq=[o for o in opts if o[1]==1]; zero=[o for o in opts if o[1]==0]; two=[o for o in opts if o[1]==2]
    if uniq and zero and len(two)>=2:
        print(tab); print(' 两解',M); print(' 唯一',uniq[:4]); print(' 矛盾',zero[:3]); print(' 仍两解',two[:4]); break
