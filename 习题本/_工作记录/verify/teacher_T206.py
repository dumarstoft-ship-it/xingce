# T206（2022江苏B）可以分解为三个质数相乘的最小三位数。
OPTS = {'A': 100, 'B': 102, 'C': 104, 'D': 105}


def omega(n):                       # 质因数个数（计重数）
    c, p = 0, 2
    while p * p <= n:
        while n % p == 0:
            n //= p
            c += 1
        p += 1
    return c + (1 if n > 1 else 0)


ans = next(n for n in range(100, 1000) if omega(n) == 3)
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print({k: (v, omega(v)) for k, v in OPTS.items()}, 'smallest =', ans)
print(hits[0])
