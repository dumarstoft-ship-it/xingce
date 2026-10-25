# -*- coding: utf-8 -*-
"""独立穷举求解 5 道无官方答案的综合推理真题（从题面条件出发，不代入预期答案）。"""
from itertools import permutations, product

def judge(name, option_checks, mode):
    """option_checks: dict letter -> list of bool over all solutions. mode: must/possible/impossible."""
    res = {}
    for k, vals in option_checks.items():
        if mode == 'must':
            res[k] = all(vals)
        elif mode == 'possible':
            res[k] = any(vals)
        elif mode == 'impossible':
            res[k] = not any(vals)
    good = [k for k, v in res.items() if v]
    print(f"{name}: 选项成立情况 {res} -> 答案 {good}")
    return good

# ---------------- 2026GD-62 ----------------
# 6 个职能局坐一排，位置 1..6 从左到右。
names = ['教育', '住建', '交通', '农业', '人社', '财政']
sols = []
for p in permutations(range(1, 7)):
    pos = dict(zip(names, p))
    # ① 财政在人社右手边且相邻；在住建左手边但不相邻
    if pos['财政'] != pos['人社'] + 1: continue
    if not (pos['财政'] < pos['住建'] and pos['住建'] - pos['财政'] >= 2): continue
    # ② 教育与交通之间隔着一个
    if abs(pos['教育'] - pos['交通']) != 2: continue
    # 附加：农业与财政相邻
    if abs(pos['农业'] - pos['财政']) != 1: continue
    sols.append(pos)
print('2026GD-62 解的个数', len(sols), sols)
R = lambda x: 7 - x  # 从右到左的序号
judge('2026GD-62', {
    'A': [R(s['教育']) == 3 for s in sols],
    'B': [R(s['住建']) == 2 for s in sols],
    'C': [s['交通'] == 3 for s in sols],
    'D': [s['人社'] == 2 for s in sols],
}, 'must')

# ---------------- 2026ZJA-97 ----------------
albums = ['A', 'B', 'C', 'D', 'E', 'F']
sols = []
for p in permutations(range(1, 7)):
    pos = dict(zip(albums, p))
    if abs(pos['A'] - pos['C']) == 1: continue
    if abs(pos['F'] - pos['C']) == 1: continue
    edge = [x for x in ('A', 'B') if pos[x] in (1, 6)]
    if len(edge) != 1: continue
    if pos['C'] != 2 or pos['E'] != 4: continue
    sols.append(pos)
print('2026ZJA-97 解', sols)
judge('2026ZJA-97', {
    'A': [s['B'] == 1 for s in sols],
    'B': [s['B'] == 5 for s in sols],
    'C': [s['D'] == 5 for s in sols],
    'D': [s['D'] == 6 for s in sols],
}, 'possible')

# ---------------- 2026GK-110 ----------------
P = ['甲', '乙', '丙', '丁', '戊', '己', '庚']
sols = []
for bits in product([0, 1], repeat=7):
    s = dict(zip(P, bits))
    if sum(bits) != 4: continue
    if s['甲'] and s['丁']: continue                         # (1) 至多其一
    if (s['丙'] or s['戊']) and not (s['甲'] and not s['己']): continue  # (2)
    if (s['乙'] or s['庚']) and not (s['丁'] and not s['甲']): continue  # (3)
    sols.append(s)
print('2026GK-110 解', [[k for k in P if s[k]] for s in sols])
judge('2026GK-110', {
    'A': [s['乙'] and s['庚'] for s in sols],
    'B': [s['丙'] and s['丁'] for s in sols],
    'C': [s['己'] and s['戊'] for s in sols],
    'D': [s['甲'] and s['乙'] for s in sols],
}, 'must')

# ---------------- 2026ZJA-98 ----------------
P = ['琪琪', '依依', '冰冰', '鑫鑫', '磊磊', '静静']
sols = []
for prize in product([1, 2, 3], repeat=6):
    s = dict(zip(P, prize))
    if prize.count(1) != 1 or prize.count(2) != 2 or prize.count(3) != 3: continue
    # (1) 除非琪琪二等，否则冰冰一等： 非(琪琪二) -> 冰冰一
    if not (s['琪琪'] == 2 or s['冰冰'] == 1): continue
    # (2) 只有 鑫鑫三且静静二，琪琪和依依才能至少一人二等： (琪二 或 依二) -> (鑫三 且 静二)
    if (s['琪琪'] == 2 or s['依依'] == 2) and not (s['鑫鑫'] == 3 and s['静静'] == 2): continue
    # (3) 鑫鑫三 -> 冰冰二 且 依依非三
    if s['鑫鑫'] == 3 and not (s['冰冰'] == 2 and s['依依'] != 3): continue
    sols.append(s)
print('2026ZJA-98 解', sols)
judge('2026ZJA-98', {
    'A': [s['冰冰'] != 1 for s in sols],
    'B': [s['琪琪'] == 2 for s in sols],
    'C': [s['鑫鑫'] != 1 for s in sols],
    'D': [s['磊磊'] == 3 for s in sols],
}, 'must')

# ---------------- 2026GD-63 ----------------
# 4 村各获一奖；收入允许相等（"相当"），用 0..3 的整数等级表示（允许并列）。
V = ['甲', '乙', '丙', '丁']
AW = ['文旅', '非遗', '生态', '数字']
sols = []
for perm in permutations(AW):
    award = dict(zip(V, perm))           # 村 -> 奖
    who = {a: v for v, a in award.items()}  # 奖 -> 村
    for inc_t in product(range(4), repeat=4):
        inc = dict(zip(V, inc_t))
        top = max(inc_t)
        if not inc[who['文旅']] > inc['丙']: continue                    # ①
        if not (inc['甲'] == inc[who['数字']] and who['数字'] != '甲'): continue  # ② 相当（且是两个不同主体）
        if inc['甲'] == top or inc[who['数字']] == top: continue        # ② 都不是最高
        if not inc[who['生态']] > inc['丁']: continue                    # ③
        if not inc['丙'] > inc[who['非遗']]: continue                    # ④
        sols.append((award, inc))
awards_set = sorted({tuple(a[v] for v in V) for a, _ in sols})
print('2026GD-63 可能的获奖分配(甲乙丙丁):', awards_set)
def rank_second(inc, v):
    # 位列第二：恰有 1 个村严格高于它
    return sum(1 for u in V if inc[u] > inc[v]) == 1
judge('2026GD-63', {
    'A': [rank_second(inc, '甲') for a, inc in sols],
    'B': [a['乙'] == '文旅' for a, inc in sols],
    'C': [a['丙'] == '数字' for a, inc in sols],
    'D': [a['丁'] == '非遗' for a, inc in sols],
}, 'must')
# 稳健性：若把"相当"理解为严格排名中相邻（无并列）则②无法满足，说明题意必须是收入相等
