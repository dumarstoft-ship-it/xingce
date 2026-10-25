# T118 2018广西选调：8人已围圆桌就座，3名加班员工在他们中间加座；加班员工彼此不相邻，且每名已就座员工最多与1名加班员工相邻
from itertools import product, permutations

SEATED, NEW = 8, 3
OPTS = {'A': 336, 'B': 96, 'C': 48, 'D': 30}

arrangements = set()
for gaps in product(range(SEATED), repeat=NEW):      # 每名加班员工插入的空（空i在第i人与第i+1人之间）
    by_gap = {}
    for w, g in enumerate(gaps):
        by_gap.setdefault(g, []).append(w)
    # 同一空里多人时还要考虑先后顺序
    orders = [list(permutations(ws)) for ws in by_gap.values()]
    for choice in product(*orders):
        seq_in_gap = dict(zip(by_gap.keys(), choice))
        circle = []
        for i in range(SEATED):
            circle.append(('S', i))
            circle.extend(('W', w) for w in seq_in_gap.get(i, ()))
        n = len(circle)
        ok = True
        for i in range(n):
            a, b = circle[i], circle[(i + 1) % n]
            if a[0] == 'W' and b[0] == 'W':
                ok = False                         # 加班员工相邻
        for i in range(n):
            if circle[i][0] == 'S':
                nb = [circle[(i - 1) % n][0], circle[(i + 1) % n][0]]
                if nb.count('W') > 1:
                    ok = False                     # 已就座员工挨着2名加班员工
        if ok:
            arrangements.add(tuple(circle))
cnt = len(arrangements)
hits = [k for k, v in OPTS.items() if v == cnt]
assert len(hits) == 1
print('ways =', cnt)
print(hits[0])
