# teacher T146（2014黑龙江）超额第1辆奖100，第2、3、4…辆奖300、500、700…，两人合计奖金1万，合计超额几辆
OPTS = {'A': 15, 'B': 16, 'C': 17, 'D': 14}
TOTAL = 10000

def bonus(n):
    return sum(100 + 200 * (k - 1) for k in range(1, n + 1))

sols = {(m, n) for m in range(1, 101) for n in range(m, 101) if bonus(m) + bonus(n) == TOTAL}
totals = {m + n for m, n in sols}
print(sols, totals)
assert len(totals) == 1
t = totals.pop()
hits = [k for k, v in OPTS.items() if v == t]
assert len(hits) == 1, hits
print(hits[0])
