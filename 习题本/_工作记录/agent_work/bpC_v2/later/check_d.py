import sys; sys.path.insert(0,'..')
from lib import *
from itertools import permutations, product, combinations
def rr(teams, win=3, draw=1):
    M=list(combinations(teams,2))
    for out in product('WDL',repeat=len(M)):
        pts={t:0 for t in teams}
        for (a,b),o in zip(M,out):
            if o=='W': pts[a]+=win
            elif o=='L': pts[b]+=win
            else: pts[a]+=draw; pts[b]+=draw
        yield dict(zip(M,out)),pts
T4=['甲','乙','丙','丁']
S=[o for o,p in rr(T4) if (p['甲'],p['乙'],p['丙'],p['丁'])==(7,6,3,1)]
print('D9 积分7/6/3/1 赛果数',len(S),'乙丙之战',{o[('乙','丙')] for o in S},'平局数',{sum(v=='D' for v in o.values()) for o in S})
T5=['A','B','C','D','E']
best=-1;bestv=None; cnt_by_last={}
allpts=[]
for o,p in rr(T5):
    v=sorted(p.values())
    allpts.append((tuple(sorted(p.values(),reverse=True)),sum(x=='D' for x in o.values())))
    if len(set(v))==5:
        cnt_by_last.setdefault(v[0],set()).add(tuple(sorted(v,reverse=True)))
print('D9 5队各不相同 最后一名可能分值',sorted(cnt_by_last), '最大时例', sorted(cnt_by_last[max(cnt_by_last)])[:3])
# D26 5队积分 10,8,6,3,1 是否可实现、平局数
ok=[d for v,d in allpts if v==(10,8,6,3,1)]
print('D26 10/8/6/3/1 可实现?',len(ok)>0,'平局数',set(ok))
# 第三名胜场
cnt=set()
for o,p in rr(T5):
    if tuple(sorted(p.values(),reverse=True))==(10,8,6,3,1):
        third=[t for t in T5 if p[t]==6][0]
        w=sum(1 for (a,b),r in o.items() if (a==third and r=='W') or (b==third and r=='L'))
        cnt.add(w)
print('   第三名(6分)胜场',cnt)
# D9 4人和100，甲>乙>丙>丁，相邻差<=5（整数），甲最大
mx=max(j for j in range(0,101) for d1 in range(1,6) for d2 in range(1,6) for d3 in range(1,6) if (lambda yi,bing,ding: yi>bing>ding>=0 and j+yi+bing+ding==100)(j-d1,j-d1-d2,j-d1-d2-d3))
print('D9 甲最多',mx)
# D9 投壶 0/2/5 投8次 可能总分
feas={sum(c) for c in product([0,2,5],repeat=8)}
print('D9 投壶不可能总分(0..40)',[x for x in range(41) if x not in feas])
# D26 平均积分 6.5 6队
print('D26 6队平均6.5→总39→平局',45-39)
