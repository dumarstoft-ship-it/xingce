# T183（2018浙江选调）30人百分制，成绩为互不相同的正整数，平均80分，问低于60分的最多几人。
N, AVG, FULL, LINE = 30, 80, 100, 60
OPTS = {'A': 7, 'B': 8, 'C': 9, 'D': 10}


def rng(k, lo, hi):
    """k个互不相同整数取自[lo,hi]的和的范围（可达和为区间内全部整数）。"""
    if hi - lo + 1 < k:
        return None
    return sum(range(lo, lo + k)), sum(range(hi - k + 1, hi + 1))


best = None
for k in range(N + 1):
    a, b = rng(k, 1, LINE - 1), rng(N - k, LINE, FULL)
    if a is None or b is None:
        continue
    if a[0] + b[0] <= N * AVG <= a[1] + b[1]:
        best = k
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1, (best, hits)
print('max below 60 =', best)
print(hits[0])
