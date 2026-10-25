# real 2026GD-63  4村4奖项 + 经济收入比较（允许并列），哪项必然正确？
from itertools import permutations, product

VIL = ['甲', '乙', '丙', '丁']
AWD = ['文旅', '非遗', '生态', '数字']

def solve(require_jia_not_digital=True):
    out = []
    for perm in permutations(AWD):
        aw = dict(zip(VIL, perm))                 # 村 → 奖项
        who = {v: k for k, v in aw.items()}       # 奖项 → 村
        for lv in product(range(4), repeat=4):    # 收入等级，数值越大越高，可并列
            inc = dict(zip(VIL, lv))
            top = max(lv)
            if not inc[who['文旅']] > inc['丙']:                  # ①
                continue
            d = who['数字']                                       # ②
            if require_jia_not_digital and d == '甲':
                continue
            if inc['甲'] != inc[d] or inc['甲'] == top:            # 相当且都不是最高
                continue
            if not inc[who['生态']] > inc['丁']:                  # ③
                continue
            if not inc['丙'] > inc[who['非遗']]:                  # ④
                continue
            out.append((aw, inc))
    return out

def rank(inc, v):          # 名次 = 1 + 收入严格高于它的村庄数
    return 1 + sum(inc[u] > inc[v] for u in VIL)

OPTS = {
    'A': lambda aw, inc: rank(inc, '甲') == 2,
    'B': lambda aw, inc: aw['乙'] == '文旅',
    'C': lambda aw, inc: aw['丙'] == '数字',
    'D': lambda aw, inc: aw['丁'] == '非遗',
}

sols = solve()
seen = set()
for aw, inc in sols:
    key = tuple(aw[v] for v in VIL)
    order = sorted(VIL, key=lambda v: -inc[v])
    pat = ''.join(order[i] + ('' if i == 3 else ('=' if inc[order[i]] == inc[order[i + 1]] else '>')) for i in range(4))
    if (key, pat) not in seen:
        seen.add((key, pat))
        print(dict(aw), pat)
assert sols
# 稳健性：即使不显式排除"甲本身就是数字农业村"，B 仍必然成立
assert all(OPTS['B'](aw, inc) for aw, inc in solve(False))
hits = [k for k, f in OPTS.items() if all(f(aw, inc) for aw, inc in sols)]
assert len(hits) == 1, hits
print(hits[0])
