# teacher_T012  红:白=3:4，拿出一定量红球、同时放入等量白球后变1:2，求新红球数:原红球数
# （题干已按老师的计算更正为"拿出红球、放入白球"；原表述"放入红球、拿出白球"无解，见下方断言）
from fractions import Fraction as F

OPTS = {'A': F(1, 3), 'B': F(7, 9), 'C': F(9, 7), 'D': F(7, 12)}
ratios = set()
for k in range(1, 300):              # 原本红3k、白4k
    for m in range(1, 3 * k):        # 拿出 m 个红球、放入 m 个白球
        if 2 * (3 * k - m) == 4 * k + m:
            ratios.add(F(3 * k - m, 3 * k))
assert len(ratios) == 1, ratios
ans = ratios.pop()
# 原表述（放入红球、拿出白球）：红球占比只升不降，不可能变成1:2
assert not any(2 * (3 * k + m) == 4 * k - m for k in range(1, 300) for m in range(1, 4 * k))
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
assert OPTS['A'] == F(1, 3)          # 不通分，直接拿1份比3份
assert OPTS['C'] == 1 / ans          # 比例颠倒
print('新红:原红 =', ans)
print(hits[0])
