# real 2026ZJA-97  6张专辑放1~6号货架；C在2号、E在4号时，哪项可能为真？
from itertools import permutations

ALB = 'ABCDEF'           # 甲：A、B；乙：C、D；丙：E、F
sols = []
for perm in permutations(range(1, 7)):
    p = dict(zip(ALB, perm))
    if p['C'] != 2 or p['E'] != 4:
        continue
    if abs(p['A'] - p['C']) == 1:          # (1) A、C不相邻
        continue
    if abs(p['F'] - p['C']) == 1:          # (2) F、C不相邻
        continue
    if sum(p[x] in (1, 6) for x in 'AB') != 1:   # (3) 有且仅有一张甲的专辑在最边上
        continue
    sols.append(p)

for s in sols:
    print(''.join(a for a, _ in sorted(s.items(), key=lambda kv: kv[1])))
OPTS = {'A': ('B', 1), 'B': ('B', 5), 'C': ('D', 5), 'D': ('D', 6)}
hits = [k for k, (a, pos) in OPTS.items() if any(s[a] == pos for s in sols)]
assert len(hits) == 1, hits
print(hits[0])
