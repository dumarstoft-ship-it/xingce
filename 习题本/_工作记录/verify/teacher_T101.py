# T101 2022北京：48人去甲，42人未去乙，去丙者中去1、2、3个基地之比3:2:1；仅去2个x人、去3个y人，求x与y关系
import itertools

OPTS = {'A': lambda x, y: x == 4 * y + 6, 'B': lambda x, y: x == 4 * y - 6,
        'C': lambda x, y: x == 3 * y + 6, 'D': lambda x, y: x == 3 * y - 6}

cases = 0
always = {k: True for k in OPTS}
for t in range(1, 8):                     # 去3个基地 y = t
    c_only = 3 * t                        # 丙中只去1个（只去丙）
    for b13 in range(0, 2 * t + 1):       # 甲丙（不含乙）
        b23 = 2 * t - b13                 # 乙丙（不含甲）
        a1 = 42 - c_only - b13            # 未去乙 = 只甲 + 只丙 + 甲丙
        if a1 < 0:
            continue
        b12 = 48 - a1 - b13 - t           # 甲 = 只甲 + 甲乙 + 甲丙 + 三
        if b12 < 0:
            continue
        for a2 in (0, 5, 17):             # 只乙人数不受约束，任取几个值
            regions = [a1, a2, c_only, b12, b13, b23, t]
            N = sum(regions)
            # 校验题设
            assert a1 + b12 + b13 + t == 48 and N - (a2 + b12 + b23 + t) == 42
            assert (c_only, b13 + b23, t) == (3 * t, 2 * t, t)
            x, y = b12 + b13 + b23, t
            cases += 1
            for k, f in OPTS.items():
                if not f(x, y):
                    always[k] = False
hits = [k for k, v in always.items() if v]
assert cases > 0 and len(hits) == 1, (cases, hits)
print('configurations checked:', cases)
print(hits[0])
