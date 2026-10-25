# D01-math-2-v01 校服分两天发运，已知剩余反求原有套数
from fractions import Fraction as Fr

opts = {'A': 360, 'B': 540, 'C': 600, 'D': 648}
p1 = Fr(10, 100)   # 第一天发出总套数的10%
p2 = Fr(40, 100)   # 第二天发出剩余套数的40%
left = 324         # 最后还剩324套

sols = []
for x in range(1, 20001):
    d1 = x * p1
    r1 = x - d1
    d2 = r1 * p2
    r2 = r1 - d2
    if d1.denominator == 1 and d2.denominator == 1 and r2 == left:
        sols.append(x)
assert len(sols) == 1, sols
ans = sols[0]

# 干扰项的错误路径
assert left / (1 - p1 - p2) == opts['D']   # 10%+40%直接相加
assert left / (1 - p2) == opts['B']        # 只还原第二天
assert left / (1 - p1) == opts['A']        # 只还原第一天

hits = [k for k, v in opts.items() if v == ans]
assert len(hits) == 1, hits
print('original sets =', ans)
print(hits[0])
