import sys; sys.path.insert(0,'..')
from lib import *
import random
random.seed(7)
# V22-1：每人至少1项、共10项；甲:乙+丙=v1 乙:丙+丁=v2 丙:丁+甲=v3 丁:甲+乙=v4；奇数说真话、偶数说假话
res=[]
for v in product(range(3,9),repeat=4):
    sols=[]
    for a in product(range(1,8),repeat=4):
        if sum(a)!=10: continue
        A,B,C,D=a
        st=[B+C==v[0], C+D==v[1], D+A==v[2], A+B==v[3]]
        if all(st[i]==(a[i]%2==1) for i in range(4)): sols.append(a)
    if len(sols)==1:
        s=sols[0]
        nt=sum(x%2 for x in s)
        if 1<=nt<=3: res.append((v,s,nt))
print('V22-1 候选数',len(res))
for r in res[:30]: print(r)
