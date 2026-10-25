# teacher T170 母题：12米深井，白天爬3米、夜里滑2米，清晨开始爬，第几天爬出（选项为自拟）
OPTS = {'A': 9, 'B': 10, 'C': 11, 'D': 12}
DEPTH, UP, DOWN = 12, 3, 2
h, day = 0, 0
while True:
    day += 1
    h += UP
    if h >= DEPTH:
        break
    h -= DOWN
print('第', day, '天爬出 | 误算 DEPTH/(UP-DOWN) =', DEPTH // (UP - DOWN))
hits = [k for k, v in OPTS.items() if v == day]
assert len(hits) == 1, hits
print(hits[0])
