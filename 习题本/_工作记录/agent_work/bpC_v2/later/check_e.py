from itertools import product, combinations
def rr(teams, win=3, draw=1):
    M=list(combinations(teams,2))
    for out in product('WDL',repeat=len(M)):
        pts={t:0 for t in teams}; dr={t:0 for t in teams}
        for (a,b),o in zip(M,out):
            if o=='W': pts[a]+=win
            elif o=='L': pts[b]+=win
            else: pts[a]+=draw; pts[b]+=draw; dr[a]+=1; dr[b]+=1
        yield dict(zip(M,out)),pts,dr
T=['甲','乙','丙','丁']
# 只有一队没有平局、冠军比亚军多2分、积分各不相同
res=set()
for o,p,d in rr(T):
    v=sorted(p.values(),reverse=True)
    if len(set(v))!=4: continue
    if sum(1 for t in T if d[t]==0)!=1: continue
    if v[0]-v[1]!=2: continue
    res.add(tuple(v))
print('只有一队无平局+冠亚差2+各不相同:',res)
# 胜2平1负0，积分5,4,2,1
S=[(o,p) for o,p,d in rr(T,2,1) if (p['甲'],p['乙'],p['丙'],p['丁'])==(5,4,2,1)]
print('2/1/0 积分5,4,2,1 赛果数',len(S))
M=list(combinations(T,2))
for m in M:
    vals={o[m] for o,p in S}
    print('  ',m,vals)
print('  平局数',{sum(v=='D' for v in o.values()) for o,p in S})
