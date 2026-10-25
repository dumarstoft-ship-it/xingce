import sys; sys.path.insert(0,'..')
from lib import *
from itertools import permutations, product, combinations
import random
# ---- D2-G1e 匹配×工程：工作量/效率=天数，限制条件下使总工期（最晚完成）最短
tasks={'管网改造':120,'道路修复':90,'绿化提升':60,'立面整治':72}
eff={'甲':30,'乙':24,'丙':18,'丁':12}
ban={('甲','绿化提升'),('乙','立面整治'),('丙','管网改造'),('丁','管网改造')}
best=None; allv=[]
for p in permutations(tasks):
    a=dict(zip(eff,p))
    if any((t,a[t]) in ban for t in eff): continue
    days=[tasks[a[t]]/eff[t] for t in eff]
    allv.append((max(days),a,days))
allv.sort(key=lambda x:x[0])
for v in allv: print(v)
