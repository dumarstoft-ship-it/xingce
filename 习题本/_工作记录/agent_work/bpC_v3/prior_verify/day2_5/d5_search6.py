from itertools import permutations, product, combinations
import random
random.seed(2)
P=['甲','乙','丙']; G=['广东','福建','湖南']; M=['法律','经济','中文']
W=[(dict(zip(P,g)),dict(zip(P,m))) for g in permutations(G) for m in permutations(M)]
stm=[(f'{x}是{g}人且学{m}',x,g,m) for x in P for g in G for m in M]
res=[]
for ss in combinations(stm,3):
    S=[w for w in W if all(((w[0][x]==g)+(w[1][x]==m))==1 for _,x,g,m in ss)]
    if len(S)<=2 and S: res.append(([s[0] for s in ss],S))
print('3句', len(res))
for r in res[:5]: print(r)
res4=[]
for trial in range(50000):
    ss=random.sample(stm,4)
    if len({s[1] for s in ss})<3: continue
    S=[w for w in W if all(((w[0][x]==g)+(w[1][x]==m))==1 for _,x,g,m in ss)]
    if len(S)==1: res4.append(([s[0] for s in ss],S[0]))
    if len(res4)>=5: break
print('4句'); [print(r) for r in res4]
