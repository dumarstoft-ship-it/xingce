# teacher T166（2012北京）1~100中既非3的倍数又非5的倍数的个数
OPTS = {'A': 46, 'B': 47, 'C': 53, 'D': 54}
N = 100
cnt = sum(1 for i in range(1, N + 1) if i % 3 and i % 5)
print('两项都不参加', cnt, '| 忘减交集', N - (N // 3 + N // 5))
hits = [k for k, v in OPTS.items() if v == cnt]
assert len(hits) == 1, hits
print(hits[0])
