import sys; sys.path.insert(0, '..')
from lib import *
import random
P = ['甲', '乙', '丙', '丁']
R = ['选调生', '教师', '医生', '律师']

def pred_templates(sp):
    out = []
    for x in P:
        for r in R:
            who = '我' if x == sp else x
            out.append((f'{who}会成为{r}', lambda a, x=x, r=r: a[x] == r))
            out.append((f'{who}不会成为{r}', lambda a, x=x, r=r: a[x] != r))
    return out
T = {p: pred_templates(p) for p in P}
random.seed(21)
v7 = []
for trial in range(80000):
    st = {p: random.choice(T[p]) for p in P}
    sols = []
    for perm in permutations(R):
        a = dict(zip(P, perm))
        tv = {p: st[p][1](a) for p in P}
        if sum(tv.values()) == 1 and tv[[p for p in P if a[p] == '选调生'][0]]:
            sols.append(perm)
    if len(sols) == 1:
        v7.append(({p: st[p][0] for p in P}, sols[0]))
        if len(v7) >= 10: break
print('v7')
for d in v7: print(d)

# v8：丁的预测是与身份无关的事件E（"我以后会去西藏支教"），真假未知
random.seed(22)
v8 = []
for trial in range(80000):
    st = {p: random.choice(T[p]) for p in P[:3]}
    sols = []
    for perm in permutations(R):
        a = dict(zip(P, perm))
        for E in (True, False):
            tv = {p: st[p][1](a) for p in P[:3]}; tv['丁'] = E
            g = [p for p in P if a[p] == '选调生'][0]
            if sum(tv.values()) == 1 and tv[g]:
                sols.append((perm, E))
    if len(sols) == 1:
        v8.append(({p: st[p][0] for p in P[:3]}, sols[0]))
        if len(v8) >= 10: break
print('v8')
for d in v8: print(d)

# v9：名次预测，只有冠军的预测对了
def rank_templates(sp):
    out = []
    for x in P:
        who = '我' if x == sp else x
        for k in (1, 2, 3, 4):
            out.append((f'{who}是第{k}名', lambda r, x=x, k=k: r[x] == k))
            out.append((f'{who}不是第{k}名', lambda r, x=x, k=k: r[x] != k))
        for y in P:
            if y != x:
                wy = '我' if y == sp else y
                out.append((f'{who}比{wy}名次高', lambda r, x=x, y=y: r[x] < r[y]))
    return out
T9 = {p: rank_templates(p) for p in P}
random.seed(23)
v9 = []
for trial in range(80000):
    st = {p: random.choice(T9[p]) for p in P}
    sols = []
    for perm in permutations([1, 2, 3, 4]):
        r = dict(zip(P, perm))
        champ = [p for p in P if r[p] == 1][0]
        if all(st[p][1](r) == (p == champ) for p in P):
            sols.append(perm)
    if len(sols) == 1:
        v9.append(({p: st[p][0] for p in P}, sols[0]))
        if len(v9) >= 10: break
print('v9')
for d in v9: print(d)
