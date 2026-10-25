# D06-math-1-v12: 密码末两位 = 数字(1~4) + 字母(A~C)，不重复随机试，恰好第 3 次才打开的概率
from fractions import Fraction as F
from itertools import product, permutations
codes = [d + c for d, c in product('1234', 'ABC')]
good = total = 0
for right in codes:                           # 正确密码等可能
    for tries in permutations(codes, 3):      # 前 3 次不重复的尝试序列等可能
        total += 1
        good += (tries[0] != right and tries[1] != right and tries[2] == right)
ans = F(good, total)
opts = {'A': F(121, 1728), 'B': F(1, 12), 'C': F(1, 10), 'D': F(1, 4)}
hit = [L for L, v in opts.items() if v == ans]
assert len(hit) == 1, (ans, hit)
print('P =', ans)
print(hit[0])
