# T111 2022国考副省级69：6名专家平均分2组，每组都要有环保专家、旅游专家和懂社交媒体的人
from itertools import combinations

ALL = frozenset('甲乙丙丁戊己')
ENV, TOUR, SOCIAL = set('甲乙丙'), set('丁戊己'), set('甲丁戊')
OPTS = {'A': 12, 'B': 24, 'C': 4, 'D': 8}

def ok(g):
    return bool(g & ENV) and bool(g & TOUR) and bool(g & SOCIAL)

splits = set()
for g in combinations(sorted(ALL), 3):
    g = frozenset(g)
    h = ALL - g
    if ok(g) and ok(h):
        splits.add(frozenset({g, h}))
cnt = len(splits)
hits = [k for k, v in OPTS.items() if v == cnt]
assert len(hits) == 1
print('valid splits =', cnt)
print(hits[0])
