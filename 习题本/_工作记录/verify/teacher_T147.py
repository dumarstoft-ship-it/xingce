# teacher T147（2014山东）名次无并列，除小周外其他人名次和为70，求小周名次
OPTS = {'A': 7, 'B': 8, 'C': 9, 'D': 10}
OTHERS = 70
sols = [(n, k) for n in range(1, 500) for k in range(1, n + 1) if n * (n + 1) // 2 - k == OTHERS]
print('(总人数, 小周名次) =', sols)
assert len(sols) == 1
hits = [k for k, v in OPTS.items() if v == sols[0][1]]
assert len(hits) == 1, hits
print(hits[0])
