# T227（2014天津）100张骨牌按"偶、偶、奇、奇"位置循环拿走（按当前剩余牌的位置），求最后剩下的编号。
OPTS = {'A': 77, 'B': 53, 'C': 39, 'D': 27}
PATTERN = ['even', 'even', 'odd', 'odd']
cur, step = list(range(1, 101)), 0
while len(cur) > 1:
    rm = PATTERN[step % 4]
    cur = [x for i, x in enumerate(cur, 1) if (i % 2 == 1) == (rm == 'even')]
    step += 1
hits = [k for k, v in OPTS.items() if v == cur[0]]
assert len(hits) == 1, (cur, hits)
print('rounds =', step, 'last =', cur[0])
print(hits[0])
