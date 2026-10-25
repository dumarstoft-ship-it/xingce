from itertools import permutations, product, combinations
import random
random.seed(8)
# G2-a 3观众×3句（名次），每人恰对1句
P=['甲','乙','丙']
W=[dict(zip(P,p)) for p in permutations([1,2,3])]
st=[(f'{x}第{r}',lambda w,x=x,r=r:w[x]==r) for x in P for r in (1,2,3)]
out=[]
for trial in range(40000):
    views=[]
    for v in range(3):
        rr=random.sample([1,2,3],3) if random.random()<0.5 else [random.randint(1,3) for _ in P]
        views.append([(f'{P[i]}第{rr[i]}名',(lambda w,x=P[i],r=rr[i]:w[x]==r)) for i in range(3)])
    S=[w for w in W if all(sum(a[1](w) for a in vw)==1 for vw in views)]
    if len(S)==1:
        out.append(([[a[0] for a in vw] for vw in views],S[0]))
    if len(out)>=4: break
print('G2-a'); [print('  ',o) for o in out]
# G2-b 4观众×4句，一人全错、其余各对1
P4=['甲','乙','丙','丁']
W4=[dict(zip(P4,p)) for p in permutations([1,2,3,4])]
out=[]
for trial in range(200000):
    views=[random.sample([1,2,3,4],4) for _ in range(4)]
    S=[]
    for w in W4:
        c=[sum(w[P4[i]]==vw[i] for i in range(4)) for vw in views]
        if sorted(c)==[0,1,1,1]: S.append((w,c.index(0)))
    if len(S)==1:
        out.append((views,S))
    if len(out)>=4: break
print('G2-b'); [print('  ',o) for o in out]
