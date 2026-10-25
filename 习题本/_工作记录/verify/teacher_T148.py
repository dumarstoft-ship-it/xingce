# teacher T148（2023深圳）页码求和时某页多加一次，结果2003，求该页码
OPTS = {'A': 45, 'B': 50, 'C': 56, 'D': 62}
S = 2003
sols = [(n, S - n * (n + 1) // 2) for n in range(1, S + 1) if 1 <= S - n * (n + 1) // 2 <= n]
print('(总页数, 多加页码) =', sols)
assert len(sols) == 1
hits = [k for k, v in OPTS.items() if v == sols[0][1]]
assert len(hits) == 1, hits
print(hits[0])
