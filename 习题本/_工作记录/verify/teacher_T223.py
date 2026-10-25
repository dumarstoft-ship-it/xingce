# T223（2011浙江）三位数各位数字和16，十位比个位小3；百位与个位对调后新数比原数大495，求原数。
OPTS = {'A': 169, 'B': 358, 'C': 469, 'D': 736}
sols = []
for n in range(100, 1000):
    a, b, c = n // 100, n // 10 % 10, n % 10
    if a + b + c == 16 and b == c - 3 and c != 0 and (100 * c + 10 * b + a) - n == 495:
        sols.append(n)
assert len(sols) == 1, sols
hits = [k for k, v in OPTS.items() if v == sols[0]]
assert len(hits) == 1, (sols, hits)
print('number =', sols[0])
print(hits[0])
