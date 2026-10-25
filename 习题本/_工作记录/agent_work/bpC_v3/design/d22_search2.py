import sys; sys.path.insert(0, '..')
from lib import *
import random
# V22-4：5人×4项判断，每人恰对一项；闭世界唯一
random.seed(11)
X = ['王', '李', '陈', '黄']; G = ['男', '女']; E = ['本科', '硕士', '博士']; K = ['综合科', '财务科', '法规科', '信息科']
J = ['甲', '乙', '丙', '丁', '戊']
found = []
for trial in range(200000):
    tab = {j: (random.choice(X), random.choice(G), random.choice(E), random.choice(K)) for j in J}
    dims = [sorted({v[i] for v in tab.values()}) for i in range(4)]
    if len(dims[0]) < 4 or len(dims[3]) < 3 or len(dims[2]) < 3:
        continue
    S = [c for c in product(*dims) if all(sum(v[i] == c[i] for i in range(4)) == 1 for v in tab.values())]
    if len(S) == 1:
        found.append((tab, S[0]))
        if len(found) >= 6:
            break
for t, s in found:
    print(s)
    for j in J:
        print('  ', j, t[j])

# V22-10：3 名岛民（实话者/说谎者），从语句模板中找唯一解
P = ['甲', '乙', '丙']
def stmts(sp):
    others = [x for x in P if x != sp]
    out = []
    for o in others:
        out.append((f'{o}是说谎者', lambda t, o=o: not t[o]))
        out.append((f'{o}是实话者', lambda t, o=o: t[o]))
    a, b = others
    out.append((f'{a}和{b}是同一类人', lambda t, a=a, b=b: t[a] == t[b]))
    out.append((f'{a}和{b}不是同一类人', lambda t, a=a, b=b: t[a] != t[b]))
    out.append((f'我和{a}是同一类人', lambda t, a=a, sp=sp: t[a] == t[sp]))
    out.append((f'我和{b}是同一类人', lambda t, b=b, sp=sp: t[b] == t[sp]))
    for k in (0, 1, 2, 3):
        out.append((f'我们三人中恰有{k}个实话者', lambda t, k=k: sum(t.values()) == k))
    out.append(('我们三人中至少有一个说谎者', lambda t: sum(t.values()) <= 2))
    return out
ST = {p: stmts(p) for p in P}
good = []
for sa in ST['甲']:
    for sb in ST['乙']:
        for sc in ST['丙']:
            sols = []
            for tv in product([True, False], repeat=3):
                t = dict(zip(P, tv))
                if all(f(t) == t[p] for p, (txt, f) in zip(P, (sa, sb, sc))):
                    sols.append(tv)
            if len(sols) == 1 and 1 <= sum(sols[0]) <= 2:
                good.append((sa[0], sb[0], sc[0], sols[0]))
print('V22-10 唯一解设计数', len(good))
random.seed(3)
for g in random.sample(good, min(25, len(good))):
    print(g)
