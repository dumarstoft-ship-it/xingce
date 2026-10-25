import sys; sys.path.insert(0, '..')
from lib import *
import random

P = ['甲', '乙', '丙', '丁']
# ---------- v2：4人获奖数各不相同、共10项（=1,2,3,4 的排列）；获奖最多者说假话，其余说真话
def tmpl(sp):
    out = []
    others = [x for x in P if x != sp]
    for a in P:
        for b in P:
            if a == b: continue
            for d in (1, 2):
                out.append((f'{a}比{b}多{d}项', lambda v, a=a, b=b, d=d: v[a] - v[b] == d))
    for a in P:
        out.append((f'{a}不是最少的', lambda v, a=a: v[a] != 1))
        out.append((f'{a}获得了{3}项', lambda v, a=a: v[a] == 3))
    for a, b in combinations(P, 2):
        out.append((f'{a}和{b}相差1项', lambda v, a=a, b=b: abs(v[a] - v[b]) == 1))
        out.append((f'{a}和{b}共获5项', lambda v, a=a, b=b: v[a] + v[b] == 5))
    return out
random.seed(5)
T = {p: tmpl(p) for p in P}
designs = []
for trial in range(60000):
    st = {p: random.choice(T[p]) for p in P}
    sols = []
    for perm in permutations([1, 2, 3, 4]):
        v = dict(zip(P, perm))
        mx = max(v, key=v.get)
        if all(st[p][1](v) == (p != mx) for p in P):
            sols.append(perm)
    if len(sols) == 1 and sols[0][0] != 4:
        designs.append(({p: st[p][0] for p in P}, sols[0]))
        if len(designs) >= 12: break
print('v2 设计')
for d in designs: print(d)

# ---------- v5：4人×4项，每人恰对两项，唯一
random.seed(9)
U = ['市发改局', '市工信局', '市科技局']; Q = ['天河区', '黄埔区', '南沙区']; Y = ['新材料', '生物医药', '人工智能']; Z = ['一等奖', '二等奖', '三等奖']
J = ['甲', '乙', '丙', '丁']
found = []
for trial in range(300000):
    tab = {j: (random.choice(U), random.choice(Q), random.choice(Y), random.choice(Z)) for j in J}
    dims = [sorted({v[i] for v in tab.values()}) for i in range(4)]
    if any(len(d) < 2 for d in dims): continue
    S = [c for c in product(*dims) if all(sum(v[i] == c[i] for i in range(4)) == 2 for v in tab.values())]
    if len(S) == 1:
        found.append((tab, S[0]))
        if len(found) >= 4: break
print('v5 设计')
for t, s in found:
    print(s)
    for j in J: print('  ', j, t[j])

# ---------- v6：4人×3项（籍贯、专业、院校），猜对个数各不相同（3、2、1、0）
random.seed(13)
A1 = ['广州', '汕头', '湛江', '韶关']; A2 = ['法学', '经济学', '中文']; A3 = ['中山大学', '暨南大学', '华南师大']
found = []
for trial in range(300000):
    tab = {j: (random.choice(A1), random.choice(A2), random.choice(A3)) for j in J}
    if len({tab[j] for j in J}) < 4: continue
    dims = [sorted({v[i] for v in tab.values()}) for i in range(3)]
    S = []
    for c in product(*dims):
        cnt = sorted(sum(v[i] == c[i] for i in range(3)) for v in tab.values())
        if cnt == [0, 1, 2, 3]: S.append(c)
    if len(S) == 1:
        found.append((tab, S[0]))
        if len(found) >= 4: break
print('v6 设计')
for t, s in found:
    print(s, '全对者', [j for j in J if t[j] == s])
    for j in J: print('  ', j, t[j])
