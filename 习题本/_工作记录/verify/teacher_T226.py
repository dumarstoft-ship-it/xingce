# T226（2024浙江A）100个零件，每轮把当前编号为奇数的拿掉、余下重新从1编号，直到剩1个，求其最初编号。
OPTS = {'A': 32, 'B': 50, 'C': 64, 'D': 100}
cur = list(range(1, 101))
while len(cur) > 1:
    cur = [x for i, x in enumerate(cur, 1) if i % 2 == 0]
hits = [k for k, v in OPTS.items() if v == cur[0]]
assert len(hits) == 1, (cur, hits)
print('last =', cur[0])
print(hits[0])
