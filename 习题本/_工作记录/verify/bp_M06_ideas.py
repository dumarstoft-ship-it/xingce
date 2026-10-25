# M06 蓝图：所有改编 idea 中给出的数据与预期答案，逐条暴力枚举核对。
# 键 = 蓝图里的编号（天-组-序号）。每条都从题面条件出发枚举计数，不代公式；最后断言与蓝图写的预期答案一致。
import itertools, datetime
from math import comb
from functools import lru_cache
P = itertools.permutations; Cb = itertools.combinations; prod = itertools.product
got = {}
def r(k, v): got[k] = v

def adjacent_ok(seq, a, b): return abs(seq.index(a) - seq.index(b)) == 1
def circ_adj(p, a, b):
    n = len(p); i, j = p.index(a), p.index(b)
    return (i - j) % n in (1, n - 1)
def circ_classes(people, pred):          # 圆桌：旋转视为同一种
    seen, cnt = set(), 0
    for p in P(people):
        if p in seen: continue
        seen |= {p[i:] + p[:i] for i in range(len(p))}
        cnt += bool(pred(p))
    return cnt
def matchings(items):                    # 两两配对（无序配对集合）
    if not items: return [[]]
    a, res = items[0], []
    for i in range(1, len(items)):
        rest = items[1:i] + items[i+1:]
        for m in matchings(rest): res.append([(a, items[i])] + m)
    return res
def lattice(E, N, block=None, via=None):
    cnt = 0
    for seq in set(P('E'*E + 'N'*N)):
        x = y = 0; ok = True; hit = via is None
        for s in seq:
            x, y = (x+1, y) if s == 'E' else (x, y+1)
            if block and (x, y) == block: ok = False
            if via and (x, y) == via: hit = True
        cnt += ok and hit
    return cnt

# ================= Day 5 =================
r('5-1-1', [s for s in range(2, 12) if comb(s+2, 2)*comb(s, 2) == 90])
c = 0
for f in prod(range(5), repeat=9):   # 0-4 男 5-8 女；0 检录 1 计时 2 篮球 3 跳水 4 不去
    g = [[i for i in range(9) if f[i] == k] for k in range(4)]
    c += (len(g[0]) == 1 and g[0][0] < 5 and len(g[1]) == 1 and g[1][0] < 5 and len(g[2]) == 2
          and sum(i < 5 for i in g[2]) == 1 and len(g[3]) == 2 and min(g[3]) >= 5)
r('5-1-2', c)
r('5-1-3', sum(sum(1 for i in s if i < 3) for s in Cb(range(6), 4) if sum(i >= 3 for i in s) >= 2))
r('5-1-4', sum(1 for p in P(range(1, 9)) if set(p[:4]) == {3,4,5,6} and set(p[4:6]) == {7,8}
               and set(p[6:]) == {1,2} and abs(p[0]-p[1]) != 1))
routes = ['高铁']*3 + ['城际']*2
r('5-1-5', sum(1 for a in routes for b in '甲乙' if not (a == '城际' and b == '甲')) + 2)
r('5-2-1', sum(1 for s in Cb(range(9), 3) if sum(i < 6 for i in s) <= 2))
r('5-2-2', [x for x in range(3, 12) if sum(1 for s in Cb(range(x+3), 3) if 0 < sum(i < x for i in s) < 3) == 63])
reg = ['粤']*4 + ['港']*3 + ['澳']*2
r('5-2-3', sum(1 for s in Cb(range(9), 4) if len({reg[i] for i in s}) == 3))
r('5-2-4', sum(1 for p in P(range(6)) if p[0] != 0 and p[5] != 1))
r('5-2-5', sum(1 for t in prod('12345ABC', repeat=3) if any(ch.isdigit() for ch in t) and any(ch.isalpha() for ch in t)))
c = 0
for p in P(['A1','A2','B1','B2','B3','C1','C2','C3']):
    if p[0][0] != 'A': continue
    c += all(max(i for i, x in enumerate(p) if x[0] == d) - min(i for i, x in enumerate(p) if x[0] == d)
             == sum(x[0] == d for x in p) - 1 for d in 'ABC')
r('5-3-1', c)
r('5-3-2', sum(1 for p in P(['主','副1','副2','甲','乙','丙','丁'])
               if p[3] == '主' and {p[2], p[4]} == {'副1','副2'} and adjacent_ok(p, '甲', '乙')))
r('5-3-3', sum(1 for p in P('甲乙丙丁戊')
               if sum(1 for a, b in Cb(sorted(p.index(x) for x in '甲乙丙'), 2) if b - a == 1) == 1))
r('5-3-4', sum(1 for p in P(['动1','动2','a','b','c','d'])
               if adjacent_ok(p, '动1', '动2') and ({p.index('动1'), p.index('动2')} & {0, 5})))
r('5-4-1', sum(1 for s in P(range(7), 3) if all(abs(a-b) >= 2 for a, b in Cb(s, 2))))
r('5-4-2', sum(1 for s in Cb(range(1, 16), 4) if all(s[i+1]-s[i] >= 3 for i in range(3))))
r('5-4-3', sum(1 for s in Cb(range(7), 3) if 6 in s and all(s[i+1]-s[i] >= 2 for i in range(2))))
r('5-4-4', sum(1 for s in P(range(1, 13), 3) if all(abs(a-b) >= 3 for a, b in Cb(s, 2))))
r('5-4-5', sum(1 for p in P(['M甲','M2','M3','M4','F1','F2','F3'])
               if all(p[i][0] != p[i+1][0] for i in range(6)) and p[0] != 'M甲'))
r('5-4-6', sum(1 for s in Cb(range(2, 10), 3) if all(s[i+1]-s[i] >= 2 for i in range(2))))
r('5-5-1', len({p for p in P(['o1','o2','o3','o4','o5','n1','n2']) if [x for x in p if x[0] == 'o'] == ['o1','o2','o3','o4','o5']}))
r('5-5-2', sum(1 for p in P('甲乙丙丁戊己') if p.index('甲') < p.index('乙') < p.index('丙')))
r('5-5-3', sum(1 for f in set(P('RRRYYB')) if f[0] != 'R' and f[-1] != 'R'))
r('5-5-4', lattice(4, 3, block=(2, 1)))
r('5-6-1', sum(1 for f in prod(range(3), repeat=6) if sorted(f.count(k) for k in range(3)) == [1,2,3]))
r('5-6-2', sum(1 for f in prod(range(3), repeat=6) if [f.count(k) for k in range(3)] == [2,2,2] and f[0] == f[1]))
r('5-6-3', sum(1 for f in prod(range(3), repeat=5) if len(set(f)) == 3))
M8 = matchings(list(range(8)))
r('5-6-4', sum(1 for m in M8 if (0, 1) not in m))
r('5-7-1', sum(1 for t in prod(range(13), repeat=3) if sum(t) == 12 and min(t) >= 2))
r('5-7-2', sum(1 for t in prod(range(1, 5), repeat=4) if sum(t) == 10))
r('5-7-3', sum(1 for t in prod(range(1, 11), repeat=3) if sum(t) == 10 and t[0] % 2 == 0))

# ================= Day 19 =================
grain = [s for k in (1, 2) for s in Cb(['小米','红豆','绿豆'], k)]
r('19-1-1', sum(1 for g in Cb(range(6), 3) for s in grain if 0 not in g or '小米' in s))
r('19-1-2', [n for n in range(3, 12) if comb(n, 2)*sum(comb(4, k) for k in range(3)) == 165])
r('19-2-1', sum(1 for s in Cb(range(7), 3) if all((b-a) % 7 not in (1, 6) for a, b in Cb(s, 2))))
r('19-2-2', sum(1 for d in P(range(1, 11), 3) if all(b-a >= 3 for a, b in zip(sorted(d), sorted(d)[1:])) and d[0] == min(d)))
r('19-2-3', sum(1 for a in range(1, 13) for b in range(1, 13) if a != b and abs(a-b) >= 3 and (a+b) % 2 == 0))
r('19-3-1', sum(1 for f in prod(range(3), repeat=5) if f.count(0) <= 1 and f.count(1) >= 1 and f.count(2) >= 1))
r('19-3-2', sum(1 for f in prod(range(4), repeat=5) if f.count(0) >= 2 and f.count(1) >= 2 and f.count(2) <= 1 and f.count(3) <= 1))
r('19-3-3', sum(1 for f in prod(range(4), repeat=4) if len(set(f)) == 2))
def part3(items):
    items = list(items); a = items[0]; res = []
    for pr in Cb(items[1:], 2):
        g1 = (a,) + pr; rest = [x for x in items if x not in g1]; b = rest[0]
        for pr2 in Cb(rest[1:], 2):
            g2 = (b,) + pr2; res.append((g1, g2, tuple(x for x in rest if x not in g2)))
    return res
r('19-3-4', sum(1 for gs in part3(range(9))       # 0-2 环保；3 甲 4 乙
                if all(sum(x < 3 for x in g) == 1 for g in gs) and not any(3 in g and 4 in g for g in gs)))
r('19-3-5', sum(1 for gz in P(range(3)) for sz in P(range(3)) if gz[0] != 0 and sz[0] != 1))
r('19-3-6', sum(1 for m in M8 if (0, 1) not in m and (2, 3) not in m))
c = 0
for f in prod(range(2), repeat=6):
    g = [[i for i in range(6) if f[i] == k] for k in range(2)]
    if min(map(len, g)) >= 2: c += max(0, len(g[0]) - 2) * max(0, len(g[1]) - 2)
r('19-4-1', c)
cap5 = [('S',), ('S',), ('H',), ('S','H'), ('S','H')]
r('19-4-2', sum(1 for s in Cb(range(5), 3) if sum('S' in cap5[i] for i in s) >= 2 and sum('H' in cap5[i] for i in s) >= 2))
r('19-4-3', sum(1 for f in prod(range(3), repeat=5) if len(set(f)) == 3 and f[0] != 0 and f[1] != 0))
assert [n for n in range(7) if 4 + 3 - 1 + n == 6] == [0]
sk = ['Y','Y','Y','E','E','YE']
r('19-4-4', sum(1 for f in prod(range(3), repeat=6) if [f.count(k) for k in range(3)] == [2,2,2]
                and all(any('Y' in sk[i] for i in range(6) if f[i] == k) for k in range(3))
                and any('E' in sk[i] for i in range(6) if f[i] == 0)))
both = 3 + 5 - (8 - 2); assert both == 2
lang = ['P']*(3-both) + ['E']*(5-both) + ['PE']*both + ['', '']
r('19-4-5', sum(1 for s in Cb(range(8), 2) if any('P' in lang[i] for i in s) and any('E' in lang[i] for i in s)))
r('19-5-1', sum(1 for t in prod(range(4, 18), repeat=3) if sum(t) == 17 and max(t) == 7))
def dists(n): return [a for a in prod(range(1, n+1), repeat=3) if sum(a) == n]
r('19-5-2', sum(1 for a in dists(5) for b in dists(5) if a[0] > b[0]))
r('19-5-3', sum(1 for t in prod(range(1, 10), repeat=3) if sum(t) == 9 and t.count(max(t)) == 1))
r('19-6-1', sum(1 for t in prod([30,25,20,15,10,5,4,1,0], repeat=3) if sum(t) == 30))
sc = [5]*2 + [4]*4 + [3]*3 + [2]*4
r('19-6-2', sum(1 for s in Cb(range(13), 3) if sum(sc[i] for i in s) == 12))
c = 0
for x in range(9):
    if 120*x + 80*(8-x) > 800: continue
    c += sum(1 for S in Cb(range(8), x) if sum(i < 2 for i in S) == min(x, 2))
r('19-6-3', c)
dim = [24, 18, 12, 12, 6, 6]
r('19-6-4', sum(1 for k in range(1, 7) for s in Cb(range(6), k) if sum(dim[i] for i in s) == 48))
def ring(k, center=False):
    reg_ = list('ABCD') + (['E'] if center else [])
    adj = [('A','B'),('B','C'),('C','D'),('D','A')] + ([(x, 'E') for x in 'ABCD'] if center else [])
    return sum(1 for col in prod(range(k), repeat=len(reg_)) if all(dict(zip(reg_, col))[x] != dict(zip(reg_, col))[y] for x, y in adj))
r('19-7-1', ring(3))
r('19-7-2', circ_classes('甲乙丙丁戊己', lambda p: circ_adj(p, '甲', '乙')))
r('19-7-3', ring(5, True))
r('19-7-4', comb(len([(u, d) for u in range(4) for d in range(4) if u != d]), 3))
der = lambda n: sum(1 for p in P(range(n)) if all(p[i] != i for i in range(n)))
r('19-8-1', der(5))
r('19-8-2', sum(1 for p in P(range(6)) if sum(p[i] == i for i in range(6)) == 2))
r('19-8-3', sum(1 for p in P(range(4)) if all(p[i] != i for i in range(4)) and p[0] != 1 and p[1] != 0))

# ================= Day 33 =================
r('33-1-1', sum(1 for p in P(range(8), 4) if p[0] // 4 != p[1] // 4))
r('33-1-2', sum(1 for p in P(range(8), 4) if len({x // 4 for x in p}) == 2 and p[0] not in (0, 3, 4, 7)))
idt = ['党']*4 + ['团']*3 + ['群']*2
r('33-1-3', sum(1 for p in P(range(9), 3) if len({idt[i] for i in p}) >= 2))
cells = [(a, b) for a in range(2) for b in range(3)]
r('33-2-1', sum(1 for p in P(cells) if p[0][0] == p[1][0] and abs(p[0][1] - p[1][1]) == 1))
g33 = [(a, b) for a in range(3) for b in range(3) if (a, b) != (1, 1)]
r('33-2-2', sum(1 for y, b, d in P(g33, 3) if y[1] == b[1] and abs(y[0]-b[0]) == 1 and abs(d[0]-1) + abs(d[1]-1) != 1))
r('33-2-3', sum(1 for p in P(['S1','S2','舞','杂','小品','魔术','相声','朗诵'])
                if {p[0], p[7]} == {'S1','S2'} and adjacent_ok(p, '舞', '杂')
                and all(abs(a-b) != 1 for a, b in Cb([p.index(x) for x in ('小品','魔术','相声')], 2))))
r('33-2-4', circ_classes(['粤1','粤2','港1','港2','澳1','澳2'], lambda p: all(circ_adj(p, d+'1', d+'2') for d in '粤港澳')))
c = 0
for order in P(['R1','R2','F1','F2']):
    for sz in prod((1, 2, 3), repeat=2):
        if sum(sz) + 2 == 6 and all(order[i][0] != order[i+1][0] for i in range(3)): c += 1
r('33-3-1', c)
kinds = ['D']*5 + ['F']*3
r('33-3-2', sum(1 for p in P(range(8), 4) if len({kinds[i] for i in p}) == 2 and all(kinds[p[i]] != kinds[p[i+1]] for i in range(3))))
r('33-3-3', sum(1 for p in P(['A1','A2','B1','B2','C','D']) if not adjacent_ok(p, 'A1', 'A2') and not adjacent_ok(p, 'B1', 'B2')))
r('33-3-4', sum(1 for s in P(range(2, 8), 3) if all(abs(a-b) >= 2 for a, b in Cb(s, 2))))
r('33-4-1', len({p for p in P(['o1','o2','o3','o4','o5','o6','n1','n2','n3'])
                 if [x for x in p if x[0] == 'o'] == ['o1','o2','o3','o4','o5','o6'] and p[0][0] == 'o' and p[-1][0] == 'o'
                 and not any(p[i][0] == 'n' == p[i+1][0] for i in range(8))}))
r('33-4-2', sum(1 for p in P('甲乙丙丁戊己庚') if p.index('甲') < p.index('乙') and adjacent_ok(p, '丙', '丁')))
r('33-4-3', sum(1 for f in set(P('RRRRYYY')) if 'YY' not in ''.join(f)))
r('33-4-4', sum(1 for f in set(P('EEEENN')) if 'NN' not in ''.join(f)))
r('33-5-1', sum(1 for p in P(range(1, 10), 3) if (100*p[0] + 10*p[1] + p[2]) % 15 == 0))
c = 0
for t in range(13*3600, 14*3600):
    d = f'{t // 3600:02d}{(t // 60) % 60:02d}{t % 60:02d}'
    c += len(set(d)) == 6
r('33-5-2', c)
LW = [(l, 90 - l) for l in range(45, 90) if l * (90 - l) == 2000]
assert LW == [(50, 40)]
sq = [(a, b) for a in range(4) for b in range(5)]
r('33-5-3', sum(1 for s in Cb(sq, 3) if len({x[0] for x in s}) == 3 and len({x[1] for x in s}) == 3))
r('33-5-4', lattice(5, 3, via=(2, 2)))
import math
pts = [(round(math.cos(2*math.pi*k/8), 9), round(math.sin(2*math.pi*k/8), 9)) for k in range(8)]
def right(a, b, c_):
    for p, q, s in ((a, b, c_), (b, a, c_), (c_, a, b)):
        if abs((q[0]-p[0])*(s[0]-p[0]) + (q[1]-p[1])*(s[1]-p[1])) < 1e-6: return True
    return False
r('33-5-5', sum(1 for s in Cb(pts, 3) if right(*s)))
def climb(n, parts, banned=()):
    @lru_cache(None)
    def f(k):
        if k in banned: return 0
        if k == 0: return 1
        return sum(f(k - p) for p in parts if k - p >= 0)
    return f(n)
r('33-6-1', climb(10, (1, 2)))
r('33-6-2', climb(10, (1, 2), banned=(6,)))
def ballot(n, start, floor):
    c = 0
    for seq in prod((1, -1), repeat=n):
        s, ok = start, True
        for x in seq:
            s += x
            if s < floor: ok = False; break
        c += ok
    return c
r('33-6-3', ballot(6, 0, 0))
r('33-6-4', climb(8, (1, 2)))
r('33-6-5', sum(1 for t in prod('01', repeat=8) if '11' not in ''.join(t)))
bad = {frozenset(x) for x in [('a','b'),('b','c'),('c','d')]}
r('33-7-1', sum(1 for p in P('abcde') if all(frozenset(p[i:i+2]) not in bad for i in range(4))))
pr5 = list(Cb(range(5), 2))
r('33-7-2', sum(1 for s in prod(pr5, repeat=3) if not any(set(s[i]) & set(s[i+1]) for i in range(2)) and set().union(*map(set, s)) == set(range(5))))
r('33-7-3', sum(1 for f in prod(range(4), repeat=5) if len(set(f)) == 4 and all(f[i] != f[i+1] for i in range(4)) and f[0] != 0))
r('33-7-4', sum(1 for p in P(['巡堤','转移','物资','通讯','宣传'])
                if p.index('巡堤') < p.index('转移') and p[0] != '物资' and not adjacent_ok(p, '通讯', '宣传')))
r('33-8-1', sum(1 for p in P(range(6)) if sum(p[i] == i for i in range(6)) == 3))
r('33-8-2', sum(1 for p in P(range(6)) if all(p[i] != i for i in range(3))))
r('33-8-3', sum(1 for p in P(range(5)) if all(p[i] != i for i in range(5)) and p[0] == 1))

# ================= Day 41 =================
r('41-1-1', sum(1 for s in Cb(range(1, 21), 5) if all(s[i+1]-s[i] >= 4 for i in range(4))))
r('41-1-2', sum(1 for s in Cb(range(10), 4) if 0 < sum(i < 6 for i in s) < 4))
r('41-1-3', sum(1 for p in P('ABCDEF') if p.index('A') < p.index('B') and p.index('C') < p.index('D')))
r('41-1-4', sum(1 for f in prod(range(3), repeat=4) if len(set(f)) == 3 and f[0] != 0))
r('41-1-5', sum(1 for t in prod(range(1, 9), repeat=3) if sum(t) == 8 and t[0] > t[1]))
r('41-1-6', sum(1 for s in P(range(8), 3) if all((a-b) % 8 not in (1, 7) for a, b in Cb(s, 2))))
r('41-2-1', sum(1 for p in P(['A1','A2','B1','B2','C']) if not adjacent_ok(p, 'A1', 'A2') and not adjacent_ok(p, 'B1', 'B2')))
r('41-2-2', sum(1 for p in P(['A1','A2','B1','B2','C1','C2']) if sum(adjacent_ok(p, d+'1', d+'2') for d in 'ABC') == 1))
r('41-2-3', sum(1 for p in P(['正1','正2','甲','乙','丙','丁']) if adjacent_ok(p, '正1', '正2') and not adjacent_ok(p, '甲', '乙')))
def teams(cap, nteam, rule, allow_idle=True, sizes=None):
    c = 0
    for f in prod(range(nteam + (1 if allow_idle else 0)), repeat=len(cap)):
        if sizes and [f.count(k) for k in range(nteam)] != sizes: continue
        ok = True
        for t in range(nteam):
            mem = [cap[i] for i in range(len(cap)) if f[i] == t]
            if not rule(sum('S' in m for m in mem), sum('H' in m for m in mem)): ok = False; break
        c += ok
    return c
cap7 = ['S']*3 + ['H']*2 + ['SH']*2
r('41-3-1', teams(cap7, 2, lambda s, h: s == 2 and h == 1))
cap6 = ['S']*2 + ['H']*2 + ['SH']*2
r('41-3-2', teams(cap6, 2, lambda s, h: s >= 2 and h >= 2, allow_idle=False))
capL = ['Y', 'Y', 'E', 'YE', 'YE']
r('41-3-3', sum(sum(1 for i in s if capL[i] == 'YE') for s in Cb(range(5), 3)
                if sum('Y' in capL[i] for i in s) >= 2 and sum('E' in capL[i] for i in s) >= 2))
bL = 5 + 4 - 7; assert bL == 2
lang7 = ['Y']*3 + ['E']*2 + ['YE']*2
r('41-3-4', sum(1 for hk in Cb(range(7), 3) if sum('E' in lang7[i] for i in hk) >= 2
                and sum('E' in lang7[i] for i in range(7) if i not in hk) >= 2))
r('41-3-5', teams(cap6, 3, lambda s, h: s >= 1 and h >= 1, allow_idle=False, sizes=[2, 2, 2]))
r('41-4-1', sum(1 for a in dists(6) for b in dists(5) if a[0]+b[0] > a[1]+b[1] and a[0]+b[0] > a[2]+b[2] and a[2] == b[2]))
r('41-4-2', sum(1 for a in dists(6) for b in dists(6) if a[0] > b[0] and b[1] > a[1] and a[2] == b[2]))
r('41-4-3', sum(1 for t in prod(range(3, 8), repeat=4) if sum(t) == 20))
c = 0
for x in range(11):
    if 150*x + 100*(10-x) > 1300: continue
    c += sum(1 for S in Cb(range(10), x) if sum(i < 4 for i in S) == min(x, 4))
r('41-5-1', c)
sol = [(a, b, cc) for a in range(1, 40) for b in range(1, 40) for cc in range(1, 40) if 2*a == b + cc and 4*b == a + b + cc and cc == a + 1]
assert sol == [(4, 3, 5)]
r('41-5-2', sum(comb(4, x)*comb(3, y)*comb(5, z) for x in (2, 3) for y in (2, 3) for z in (2, 3) if x + y + z == 7))
items = [20]*3 + [30]*4
r('41-5-3', sum(1 for k in range(1, 8) for s in Cb(range(7), k) if sum(items[i] for i in s) == 120))
vou = [50]*2 + [30]*3 + [20]*2
r('41-5-4', len({tuple(vou[i] for i in p) for k in range(1, 8) for p in P(range(7), k) if sum(vou[i] for i in p) == 100}))
r('41-6-1', len({tuple(sorted((10*p[0]+p[1], 10*p[2]+p[3], 10*p[4]+p[5]))) for p in P(range(1, 7)) if 10*(p[0]+p[2]+p[4]) + p[1]+p[3]+p[5] == 111}))
cells9 = [(a, b) for a in range(3) for b in range(3)]
rot = lambda x: (x[1], 2 - x[0])
def canon(s):
    best, cur = None, frozenset(s)
    for _ in range(4):
        t = tuple(sorted(cur)); best = t if best is None or t < best else best
        cur = frozenset(rot(x) for x in cur)
    return best
r('41-6-2', len({canon(s) for s in Cb(cells9, 2)}))
r('41-6-3', sum(1 for t in P(range(10), 3) if sum(t) == 12))
def near(n, d): return sum(1 for p in P(range(n)) if all(abs(p[i]-i) <= d for i in range(n)))
r('41-7-1', near(8, 1) - 1)
c = 0
def bt(i, n, used, cur):
    global c
    if i == n:
        if sum(1 for k in range(n-1) if cur[k] == k+1 and cur[k+1] == k) == 2: c += 1
        return
    for j in (i-1, i, i+1):
        if 0 <= j < n and not (used >> j) & 1: bt(i+1, n, used | (1 << j), cur + [j])
bt(0, 10, 0, [])
r('41-7-2', c)
r('41-7-3', sum(1 for k in range(1, 9) for s in prod((1, 2), repeat=k) if sum(s) == 8 and all(not (s[i] == 2 == s[i+1]) for i in range(k-1))))
c = 0
for seq in prod(range(5), repeat=4):
    cur, ok = 0, True
    for x in seq:
        if x == cur: ok = False; break
        cur = x
    c += ok and cur == 0
r('41-7-4', c)
r('41-8-1', sum(1 for f in prod(range(4), repeat=5) if len(set(f)) == 4 and all(f[i] != f[0] for i in range(1, 5))
                and f[1] == f[2] and f[3] > f[4] and f[0] not in (0, 3)))
r('41-8-2', sum(1 for s in prod(pr5, repeat=4) if not any(set(s[i]) & set(s[i+1]) for i in range(3))
                and set().union(*map(set, s)) == set(range(5)) and 2 not in s[0] and 4 not in s[0] and 0 in s[3]))
badp = {frozenset(x) for g in ['abc', 'cde', 'ef'] for x in Cb(g, 2)}
r('41-8-3', sum(1 for p in P('abcdef') if all(frozenset(p[i:i+2]) not in badp for i in range(5))))
r('41-8-4', sum(1 for p in P(['发改','财政','人社','自然资源','住建','交通'])
                if not adjacent_ok(p, '住建', '交通') and p.index('财政') == p.index('发改') + 1
                and p.index('人社') not in (0, 5) and p.index('自然资源') < p.index('住建')))
ptsL = [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 3), (5, 2)]
col = lambda a, b, c_: (b[0]-a[0])*(c_[1]-a[1]) - (c_[0]-a[0])*(b[1]-a[1]) == 0
assert sum(1 for s in Cb(ptsL, 3) if col(*s)) == 4
r('41-9-1', sum(1 for s in Cb(ptsL, 3) if not col(*s)))
assert datetime.date(2026, 12, 1).weekday() == 1   # 周二
we = [datetime.date(2026, 12, d) for d in range(1, 32) if datetime.date(2026, 12, d).weekday() >= 5]
r('41-9-2', sum(1 for s in Cb(we, 3) if len({d.isocalendar()[1] for d in s}) == 3))
r('41-9-3', [n for n in range(7, 40) if n*6 == comb(n, 2) + comb(6, 2)])
r('41-9-4', min(k for k in range(2, 8) if sum(1 for cc in prod(range(k), repeat=5) if all(cc[i] != cc[i+1] for i in range(4))) >= 300))

expect = {
 '5-1-1':[4],'5-1-2':720,'5-1-3':21,'5-1-4':48,'5-1-5':10,
 '5-2-1':64,'5-2-2':[6],'5-2-3':72,'5-2-4':504,'5-2-5':360,
 '5-3-1':144,'5-3-2':16,'5-3-3':72,'5-3-4':96,
 '5-4-1':60,'5-4-2':126,'5-4-3':6,'5-4-4':336,'5-4-5':108,'5-4-6':20,
 '5-5-1':42,'5-5-2':120,'5-5-3':12,'5-5-4':17,
 '5-6-1':360,'5-6-2':18,'5-6-3':150,'5-6-4':90,
 '5-7-1':28,'5-7-2':44,'5-7-3':16,
 '19-1-1':90,'19-1-2':[6],'19-2-1':7,'19-2-2':40,'19-2-3':40,
 '19-3-1':100,'19-3-2':80,'19-3-3':84,'19-3-4':72,'19-3-5':16,'19-3-6':78,
 '19-4-1':20,'19-4-2':7,'19-4-3':62,'19-4-4':60,'19-4-5':16,
 '19-5-1':9,'19-5-2':11,'19-5-3':24,
 '19-6-1':34,'19-6-2':32,'19-6-3':25,'19-6-4':7,
 '19-7-1':18,'19-7-2':48,'19-7-3':420,'19-7-4':220,
 '19-8-1':44,'19-8-2':135,'19-8-3':4,
 '33-1-1':960,'33-1-2':816,'33-1-3':474,
 '33-2-1':192,'33-2-2':24,'33-2-3':48,'33-2-4':16,
 '33-3-1':24,'33-3-2':240,'33-3-3':336,'33-3-4':24,
 '33-4-1':60,'33-4-2':720,'33-4-3':10,'33-4-4':10,
 '33-5-1':20,'33-5-2':360,'33-5-3':240,'33-5-4':24,'33-5-5':24,
 '33-6-1':89,'33-6-2':24,'33-6-3':20,'33-6-4':34,'33-6-5':55,
 '33-7-1':20,'33-7-2':60,'33-7-3':108,'33-7-4':30,
 '33-8-1':40,'33-8-2':426,'33-8-3':11,
 '41-1-1':56,'41-1-2':194,'41-1-3':180,'41-1-4':24,'41-1-5':9,'41-1-6':96,
 '41-2-1':48,'41-2-2':288,'41-2-3':144,
 '41-3-1':36,'41-3-2':10,'41-3-3':10,'41-3-4':18,'41-3-5':60,
 '41-4-1':7,'41-4-2':10,'41-4-3':85,
 '41-5-1':37,'41-5-2':360,'41-5-3':7,'41-5-4':13,
 '41-6-1':18,'41-6-2':10,'41-6-3':60,
 '41-7-1':33,'41-7-2':28,'41-7-3':19,'41-7-4':52,
 '41-8-1':6,'41-8-2':24,'41-8-3':12,'41-8-4':24,
 '41-9-1':31,'41-9-2':32,'41-9-3':[10],'41-9-4':4,
}
bad = [(k, got.get(k), v) for k, v in expect.items() if got.get(k) != v]
extra = sorted(set(got) - set(expect))
print('ideas checked:', len(expect), ' mismatches:', bad, ' unchecked keys:', extra)
assert not bad and not extra
