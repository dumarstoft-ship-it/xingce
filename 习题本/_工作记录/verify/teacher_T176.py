# T176（2023江西）230盒口罩分给10栋楼，两两数量不同，且最多与最少"相差不超过1倍"（最多≤2×最少），
# 求派发最少的那栋楼最少可派发多少盒。
TOTAL, N = 230, 10
OPTS = {'A': 18, 'B': 15, 'C': 14, 'D': 12}


def reachable(k, lo, hi):
    """从[lo,hi]中取k个互不相同的整数，所有可能的和（DP精确计算）。"""
    dp = [set() for _ in range(k + 1)]
    dp[0].add(0)
    for v in range(lo, hi + 1):
        for c in range(k, 0, -1):
            dp[c] |= {s + v for s in dp[c - 1]}
    return dp[k]


def feasible(m):
    # 最少的一栋为m，其余9栋取自(m, 2m]内互不相同的整数
    return (TOTAL - m) in reachable(N - 1, m + 1, 2 * m)


best = next(m for m in range(1, TOTAL + 1) if feasible(m))
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1, (best, hits)
print('min of smallest =', best)
print(hits[0])
