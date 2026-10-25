from itertools import combinations, product
def rr(teams, win=3, draw=1):
    M=list(combinations(teams,2))
    for out in product('WDL', repeat=len(M)):
        pts={t:0 for t in teams}
        for (a,b),o in zip(M,out):
            if o=='W': pts[a]+=win
            elif o=='L': pts[b]+=win
            else: pts[a]+=draw; pts[b]+=draw
        yield dict(zip(M,out)), pts
T=['甲','乙','丙','丁']
for target in [(7,5,4,0),(7,6,3,1),(9,4,3,1)]:
    sols=[o for o,p in rr(T) if tuple(p[t] for t in T)==target]
    print(target, len(sols), sols)
# 5队各不相同，最后一名最多
T5=['A','B','C','D','E']
best=-1; ex=None
for o,p in rr(T5):
    v=sorted(p.values())
    if len(set(v))==5 and v[0]>best: best=v[0]; ex=(o,p)
print('5队积分各不相同时最后一名最多', best, ex[1])
# 4人得分和100，甲>乙>丙>丁，相邻差<=5，甲最大
mx=0
for d in range(0,101):
    for a in range(1,6):
        for b in range(1,6):
            for c in range(1,6):
                bing=d+a; yi=bing+b; jia=yi+c
                if d+bing+yi+jia==100: mx=max(mx,jia)
print('甲最多',mx)
