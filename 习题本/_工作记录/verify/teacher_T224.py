# T224（2017天津选调）五位数左边三位数是右边两位数的5倍；把右边两位移到前面，新五位数比原数的2倍多75，求原数。
OPTS = {'A': 22545, 'B': 17535, 'C': 12525, 'D': 11575}
sols = []
for n in range(10000, 100000):
    left, right = n // 100, n % 100
    if right < 10 or left != 5 * right:
        continue
    new = right * 1000 + left
    if new == 2 * n + 75:
        sols.append(n)
assert len(sols) == 1, sols
hits = [k for k, v in OPTS.items() if v == sols[0]]
assert len(hits) == 1, (sols, hits)
print('number =', sols[0])
print(hits[0])
