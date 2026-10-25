import sys; sys.path.insert(0, '..')
from lib import *
import random

# 24-1/24-2 两层选择（同构 ZJA-102）：小陈、小林、小黄、小周 × {科技, 文化, 生态} × 1–3 个
P = ['陈', '林', '黄', '周']; TY = ['科技', '文化', '生态']
S = []
for ty in product(TY, repeat=4):
    for cn in product([1, 2, 3], repeat=4):
        T = dict(zip(P, ty)); N = dict(zip(P, cn))
        if T['陈'] == T['周'] or N['陈'] == N['周']: continue
        if sorted(cn).count(1) != 1 or sorted(cn).count(2) != 2: continue
        if not (T['林'] == '生态' and N['林'] == 3): continue
        if set(ty) != set(TY) or T['黄'] != '科技' or T['周'] != '科技': continue
        S.append((T, N))
print('24-1 解', S)

# 24-3 5人×3类×1–3个：共选10个、选3个的只有1人
P5 = ['甲', '乙', '丙', '丁', '戊']
random.seed(3)
def cond_pool():
    out = []
    for a, b in combinations(P5, 2):
        out.append((f'{a}和{b}选的类别相同', lambda T, N, a=a, b=b: T[a] == T[b]))
        out.append((f'{a}和{b}选的类别不同', lambda T, N, a=a, b=b: T[a] != T[b]))
        out.append((f'{a}和{b}选的数量相同', lambda T, N, a=a, b=b: N[a] == N[b]))
        out.append((f'{a}和{b}的类别、数量都不同', lambda T, N, a=a, b=b: T[a] != T[b] and N[a] != N[b]))
    for a in P5:
        for t in TY:
            out.append((f'{a}选{t}营', lambda T, N, a=a, t=t: T[a] == t))
    for t in TY:
        out.append((f'选{t}营的只有1人', lambda T, N, t=t: list(T.values()).count(t) == 1))
        out.append((f'选{t}营的人所选数量各不相同', lambda T, N, t=t: len([N[x] for x in P5 if T[x] == t]) == len({N[x] for x in P5 if T[x] == t})))
    return out
POOL = cond_pool()
allsol = []
for ty in product(TY, repeat=5):
    if set(ty) != set(TY): continue
    for cn in product([1, 2, 3], repeat=5):
        if sum(cn) != 10 or cn.count(3) != 1: continue
        allsol.append((dict(zip(P5, ty)), dict(zip(P5, cn))))
print('24-3 基础解数', len(allsol))
found = 0
for trial in range(200000):
    cs = random.sample(POOL, 4)
    S3 = [s for s in allsol if all(f(*s) for _, f in cs)]
    if len(S3) == 1:
        T, N = S3[0]
        print('24-3', [c for c, _ in cs], T, N)
        found += 1
        if found >= 5: break

# 24-5 三人三任务总时间最少
TIME = {'甲': [4, 6, 5], '乙': [5, 3, 7], '丙': [6, 5, 4]}
res = sorted((sum(TIME[p][t] for p, t in zip(TIME, perm)), perm) for perm in permutations(range(3)))
print('24-5', res[:3])
TIME = {'甲': [6, 4, 7], '乙': [5, 3, 4], '丙': [4, 6, 8]}
res = sorted((sum(TIME[p][t] for p, t in zip(TIME, perm)), perm) for perm in permutations(range(3)))
print('24-5b', res[:3])

# 24-6 两道工序流水排序（先审核后复核）
D = {'A': (3, 6), 'B': (5, 2), 'C': (1, 4), 'D': (4, 3)}
def makespan(order):
    t1 = t2 = 0
    for x in order:
        t1 += D[x][0]; t2 = max(t2, t1) + D[x][1]
    return t2
res = sorted((makespan(o), ''.join(o)) for o in permutations('ABCD'))
print('24-6', res[:6])
