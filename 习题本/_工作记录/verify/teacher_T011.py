# teacher_T011  红:白=3:4，放入等量红、白球后变11:13，求原本球数:新加球数
from fractions import Fraction as F

OPTS = {'A': F(7, 17), 'B': F(14, 5), 'C': F(5, 7), 'D': F(7, 5)}
ratios = set()
for k in range(1, 200):              # 原本红3k、白4k
    for m in range(1, 1000):         # 红、白各放入 m 个
        if 13 * (3 * k + m) == 11 * (4 * k + m):
            ratios.add(F(7 * k, 2 * m))
assert len(ratios) == 1, ratios
ans = ratios.pop()
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
assert OPTS['A'] == F(3 + 4, (11 + 13) - (3 + 4))   # 不统一份数直接相减
assert OPTS['C'] == 1 / ans                        # 比例颠倒
print('原本:新加 =', ans)
print(hits[0])
