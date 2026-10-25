from itertools import permutations, product
P=['甲','乙','丙','丁','戊']
def partitions(n):
    # restricted growth strings
    def rec(i, cur, m):
        if i==n: yield tuple(cur); return
        for v in range(m+1):
            yield from rec(i+1, cur+[v], max(m, v+1) if v==m else m)
    yield from rec(0, [], 0)
parts=list(partitions(5))
print('partitions',len(parts))
S=[]
for p in permutations(range(1,6)):
    r=dict(zip(P,p)); at={v:k for k,v in r.items()}
    for u in parts:
        U=dict(zip(P,u)); same=lambda a,b:U[a]==U[b]
        # ① 甲和第二名同单位且名次比他低（甲不是第二名）
        if at[2]=='甲' or not same('甲',at[2]) or not r['甲']>2: continue
        # ② 乙和甲不同单位；乙和第四名同单位（乙不是第四名）
        if same('乙','甲') or at[4]=='乙' or not same('乙',at[4]): continue
        # ③ 丙名次比丁高
        if not r['丙']<r['丁']: continue
        # ④ 第一名和第五名同单位
        if not same(at[1],at[5]): continue
        S.append((r,U))
print('sol count',len(S))
from collections import Counter
print('甲名次',Counter(r['甲'] for r,U in S))
print('乙名次',Counter(r['乙'] for r,U in S))
print('丙名次',Counter(r['丙'] for r,U in S))
print('丁名次',Counter(r['丁'] for r,U in S))
print('戊名次',Counter(r['戊'] for r,U in S))
rk=set(tuple(r[x] for x in P) for r,U in S)
print('rank patterns',sorted(rk))
