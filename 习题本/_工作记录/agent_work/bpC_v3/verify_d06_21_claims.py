# -*- coding: utf-8 -*-
"""第6–21天改编 idea 中写明了答案/数据的部分：逐条独立验算（v3）。"""
from lib import *

# ---------- Day 6 一拖二·龙舟泊位（1..6 由北向南）
P = ['甲', '乙', '丙', '丁', '戊', '己']
S = line(P, 6, [lambda s: abs(s['甲'] - s['乙']) == 1, lambda s: s['丁'] - s['丙'] == 3,
                lambda s: abs(s['甲'] - s['戊']) == 2, lambda s: s['己'] not in (1, 6)])
print('D6 龙舟 解', [fmt_line(s) for s in S])
judge('D6-一拖二-1', S, {'A': lambda s: s['戊'] == 1, 'B': lambda s: s['戊'] == 2, 'C': lambda s: s['戊'] == 4, 'D': lambda s: s['戊'] == 5}, 'possible', 'C')
S2 = [s for s in S if s['乙'] == 6]
judge('D6-一拖二-2', S2, {'A': lambda s: s['甲'] == 4, 'B': lambda s: s['己'] == 2, 'C': lambda s: s['丁'] == 3, 'D': lambda s: s['戊'] == 4}, 'must', 'B')
# 排序链+概率
from fractions import Fraction
P = ['甲', '乙', '丙', '丁', '戊']
S = line(P, 5, [lambda r: r['甲'] < r['乙'] < r['丙']])
print('D6 概率: 丁高于甲', Fraction(sum(r['丁'] < r['甲'] for r in S), len(S)), ' 戊第三', Fraction(sum(r['戊'] == 3 for r in S), len(S)))

# ---------- Day 8 至少选4种
T = ['荔枝', '龙眼', '菠萝', '香蕉', '芒果', '杨桃']
S = []
for b in product([0, 1], repeat=6):
    s = dict(zip(T, b))
    if sum(b) < 4: continue
    if s['荔枝'] and (s['龙眼'] or s['菠萝']): continue
    if not (s['香蕉'] or s['芒果']): continue
    if s['杨桃'] + s['龙眼'] != 1: continue
    S.append(s)
print('D8 选法', [''.join(k for k in T if s[k]) for s in S])
judge('D8-至少4种', S, {'A': lambda s: s['香蕉'], 'B': lambda s: s['荔枝'], 'C': lambda s: not s['菠萝'], 'D': lambda s: s['杨桃']}, 'must', 'A')

# ---------- Day 9 积分
def rr_results(teams, pts_rule=(3, 1, 0)):
    games = list(combinations(teams, 2))
    for res in product('WDL', repeat=len(games)):
        pts = {t: 0 for t in teams}; draws = 0; dr = {t: 0 for t in teams}
        for (a, b), r in zip(games, res):
            if r == 'W': pts[a] += pts_rule[0]; pts[b] += pts_rule[2]
            elif r == 'L': pts[b] += pts_rule[0]; pts[a] += pts_rule[2]
            else: pts[a] += pts_rule[1]; pts[b] += pts_rule[1]; draws += 1; dr[a] += 1; dr[b] += 1
        yield dict(zip(games, res)), pts, draws, dr
T4 = ['甲', '乙', '丙', '丁']
S = [g for g, p, d, dr in rr_results(T4) if [p[t] for t in T4] == [7, 6, 3, 1]]
print('D9 积分7/6/3/1 赛果数', len(S), '乙丙之战', {g[('乙', '丙')] for g in S})
# 只有一队没有平局 + 冠军比亚军多2 + 积分各不相同 → 亚军
combos = set()
for g, p, d, dr in rr_results(T4):
    sc = sorted(p.values(), reverse=True)
    if len(set(sc)) != 4: continue
    if sum(dr[t] == 0 for t in T4) != 1: continue
    if sc[0] - sc[1] != 2: continue
    combos.add(tuple(sc))
print('D9 只有一队无平局 积分组合', combos)
# 胜2平1负0：甲5 乙4 丙2 丁1
S = [(g, d) for g, p, d, dr in rr_results(T4, (2, 1, 0)) if [p[t] for t in T4] == [5, 4, 2, 1]]
print('D9 胜2平1 赛果数', len(S), '平局数可能', sorted({d for g, d in S}))
def lost(g, t): return any((t == a and r == 'L') or (t == b and r == 'W') for (a, b), r in g.items())
judge('D9-胜2平1', [g for g, d in S], {'A': lambda g: sum(r == 'D' for r in g.values()) == 2, 'B': lambda g: not lost(g, '甲'),
                                      'C': lambda g: g[('乙', '丙')] == 'D', 'D': lambda g: g[('丙', '丁')] == 'W'}, 'must', 'B')
# 5队单循环 积分各不相同，最后一名最多几分
T5 = ['A', 'B', 'C', 'D', 'E']
best = -1; ex = None
for g, p, d, dr in rr_results(T5):
    v = sorted(p.values())
    if len(set(v)) == 5 and v[0] > best: best = v[0]; ex = sorted(p.values(), reverse=True)
print('D9 5队各不相同 最后一名最多', best, '例', ex)
# 4人总分100，甲>乙>丙>丁，相邻差<=5，甲最多
mx = max(a for a in range(26, 60) for b in range(a - 5, a) for c in range(b - 5, b) for dd in [100 - a - b - c] if 0 < dd < c and c - dd <= 5)
print('D9 甲最多', mx)
# 投壶 0/2/5 ×8 次
feas = {2 * x + 5 * y for x in range(9) for y in range(9) if x + y <= 8}
print('D9 投壶 0-40 不可能的总分', [t for t in range(41) if t not in feas])
# 档位人数
print('D9 档位', [(a, b, 10 - a - b) for a in range(2, 9) for b in range(2, 9) if 10 - a - b >= 2 and a < b < 10 - a - b])
# 15人三组
print('D9 三组', [(a, b, c) for a in range(3, 13) for b in range(3, 13) for c in range(3, 13) if a + b + c == 15 and len({a, b, c}) == 3 and a == c + 2 and b > a and b > c])

# ---------- Day 10 城际线（1..6 由南向北）
P = ['会展', '大学城', '科技园', '湿地', '古镇', '港口']
S = line(P, 6, [lambda s: s['古镇'] - s['湿地'] == 3, lambda s: s['古镇'] not in (1, 6),
                lambda s: abs(s['会展'] - s['大学城']) == 2, lambda s: abs(s['古镇'] - s['港口']) == 1])
print('D10 城际线 解', [fmt_line(s) for s in S], '确定', determined(S, P))
value('D10-一拖二-1', len(determined(S, P)), {'A': 1, 'B': 2, 'C': 3, 'D': 4}, 'B')
S2 = [s for s in S if s['会展'] == 1]
judge('D10-一拖二-2', S2, {'A': lambda s: s['港口'] == 6, 'B': lambda s: s['科技园'] == 6, 'C': lambda s: s['大学城'] == 3,
                           'D': lambda s: abs(s['大学城'] - s['古镇']) == 1}, 'impossible', 'D')

# ---------- Day 11 圆桌 8人：党员5、女性4，每位女性两侧都是党员
sols = set()
for fem in combinations(range(8), 4):
    for par in combinations(range(8), 5):
        F = set(fem); Pp = set(par)
        if all(((i - 1) % 8 in Pp and (i + 1) % 8 in Pp) for i in F):
            sols.add(len(F & Pp))
print('D11 女党员人数可能', sols)

# ---------- Day 14 3的倍数＋上下限；恰有一人说谎反推次数；积分报数只有一队报错；门牌号；年龄
feas = {sum(c) for c in product([3, 6, 9, 12], repeat=5)}
print('D14 报错人数', sum(x not in feas for x in (15, 28, 45, 63)))
for n in (5, 6, 7):
    fs = {sum(c) for c in product([1, 3, 5, 7, 9], repeat=n)}
    print('D14 次数', n, '说谎人数', sum(x not in fs for x in (10, 21, 30, 32)))
valid = set()
for g, p, d, dr in rr_results(T4):
    valid.add(tuple(p[t] for t in T4))
rep = (7, 6, 4, 2)
cands = []
for i in range(4):
    for v in range(0, 10):
        if v == rep[i]: continue
        t = list(rep); t[i] = v
        if tuple(t) in valid: cands.append((T4[i], v))
print('D14 只有一队报错：可能的(报错队,真实分)', cands)
door = [n for n in range(100, 1000) if len(set(str(n))) == 3 and sum(map(int, str(n))) == 13
        and int(str(n)[0]) - int(str(n)[2]) == 2 and n % 4 == 0 and str(n)[1] != '0']
print('D14 门牌号候选', door)
print('D14 年龄 和为100时孙子年龄', 76 / 8, ' 和为104时', (104 - 24) / 8)
summary()
