# D05-math-h-v02：9 名网格员（3 名新入职、6 名有一线经验）组成 3 个小组，每组 3 人：
# 2 个小组到同一小区开展完全相同的入户走访（两组不作区分），1 个小组到商业街做消防检查；
# 每个小组至少有 1 名有经验的网格员。问不同的分组安排有多少种。
# 暴力枚举：遍历 9 人的全部排列，前 3 人为检查组、后 6 人按顺序切成两个走访组；
# 两个走访组不作区分，所以记成"检查组 + 走访组的无序集合"去重，再按条件筛选。
from itertools import permutations

OPTIONS = {'A': 270, 'B': 780, 'C': 810, 'D': 1620}

people = ['新1', '新2', '新3', '老1', '老2', '老3', '老4', '老5', '老6']
newcomers = {'新1', '新2', '新3'}

plans = set()
for order in permutations(people):
    check_group = frozenset(order[0:3])
    visit_groups = frozenset([frozenset(order[3:6]), frozenset(order[6:9])])
    plans.add((check_group, visit_groups))


def ok(plan):
    check_group, visit_groups = plan
    return all(len(g - newcomers) >= 1 for g in [check_group, *visit_groups])


count = sum(1 for p in plans if ok(p))

hits = [k for k, v in OPTIONS.items() if v == count]
assert len(hits) == 1, (count, hits)
print('all plans =', len(plans), 'valid =', count)
print(hits[0])
