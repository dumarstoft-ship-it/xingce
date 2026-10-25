# T178（2018四川下）6所大学共招500人，两两不同；A最少且恰为B的一半，B最多。求A至少多少人。
TOTAL, N = 500, 6
OPTS = {'A': 48, 'B': 47, 'C': 46, 'D': 45}


def reachable(k, lo, hi):
    dp = [set() for _ in range(k + 1)]
    dp[0].add(0)
    for v in range(lo, hi + 1):
        for c in range(k, 0, -1):
            dp[c] |= {s + v for s in dp[c - 1]}
    return dp[k]


def feasible(a):
    b = 2 * a
    # 其余4所严格介于a与b之间且互不相同
    return (TOTAL - a - b) in reachable(N - 2, a + 1, b - 1)


best = next(a for a in range(1, TOTAL) if feasible(a))
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1, (best, hits)
print('min A =', best)
print(hits[0])
