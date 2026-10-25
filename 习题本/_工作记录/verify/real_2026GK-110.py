# real 2026GK-110  7名代表中安排4人发言，满足(1)(2)(3)，下列说法正确的是？
from itertools import combinations

P = ['甲', '乙', '丙', '丁', '戊', '己', '庚']
sols = []
for chosen in combinations(P, 4):
    s = set(chosen)
    if '甲' in s and '丁' in s:                                   # (1) 甲、丁至多一人
        continue
    if ('丙' in s or '戊' in s) and not ('甲' in s and '己' not in s):   # (2)
        continue
    if ('乙' in s or '庚' in s) and not ('丁' in s and '甲' not in s):   # (3)
        continue
    sols.append(s)

for s in sols:
    print(''.join(x for x in P if x in s))
assert sols
OPTS = {'A': {'乙', '庚'}, 'B': {'丙', '丁'}, 'C': {'己', '戊'}, 'D': {'甲', '乙'}}
hits = [k for k, need in OPTS.items() if all(need <= s for s in sols)]
assert len(hits) == 1, hits
print(hits[0])
