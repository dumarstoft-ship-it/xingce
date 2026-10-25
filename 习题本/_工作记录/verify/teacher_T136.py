# teacher T136（2022四川下）6月6日开售，每天多1台，6月16日卖22台，求6月总销量
OPTS = {'A': 555, 'B': 600, 'C': 645, 'D': 690}
START, KNOWN_DAY, KNOWN, END = 6, 16, 22, 30
sales = {d: KNOWN + (d - KNOWN_DAY) for d in range(START, END + 1)}
assert all(v > 0 for v in sales.values())
total = sum(sales.values())
print('天数', len(sales), '| 中间项', sales[(START + END) // 2], '| 合计', total)
hits = [k for k, v in OPTS.items() if v == total]
assert len(hits) == 1, hits
print(hits[0])
