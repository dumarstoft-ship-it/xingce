# real 2026GD-62  6个职能局一排就座（位置1~6从左到右），农业局与财政局相邻时必然正确的是？
from itertools import permutations

NAMES = ['教育', '住建', '交通', '农业', '人社', '财政']
sols = []
for perm in permutations(range(1, 7)):
    p = dict(zip(NAMES, perm))
    if p['财政'] != p['人社'] + 1:          # ①财政局在人社局右手边且相邻
        continue
    if p['住建'] - p['财政'] < 2:           # ①财政局在住建局左边但不相邻
        continue
    if abs(p['教育'] - p['交通']) != 2:     # ②教育局与交通局之间隔一个
        continue
    if abs(p['农业'] - p['财政']) != 1:     # 附加：农业局与财政局相邻
        continue
    sols.append(p)

for s in sols:
    print(' '.join(n for n, _ in sorted(s.items(), key=lambda kv: kv[1])))
assert sols
OPTS = {
    'A': lambda p: p['教育'] == 7 - 3,   # 从右到左第三位 = 从左数第4位
    'B': lambda p: p['住建'] == 7 - 2,   # 从右到左第二位 = 从左数第5位
    'C': lambda p: p['交通'] == 3,
    'D': lambda p: p['人社'] == 2,
}
hits = [k for k, f in OPTS.items() if all(f(s) for s in sols)]
assert len(hits) == 1, hits
print(hits[0])
