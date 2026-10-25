# D05-math-2-v03：3 面相同红旗、2 面相同黄旗、1 面蓝旗全部挂成一列，最上、最下都不能是红旗。
# 枚举 6 面旗的全部排列，按颜色序列去重（同色旗不区分），再筛选两端条件。
from itertools import permutations

OPTIONS = {'A': 8, 'B': 12, 'C': 24, 'D': 60}

flags = ['红'] * 3 + ['黄'] * 2 + ['蓝']
signals = set(permutations(flags))          # 不同的颜色序列 = 不同的信号
count = sum(1 for s in signals if s[0] != '红' and s[-1] != '红')

hits = [k for k, v in OPTIONS.items() if v == count]
assert len(hits) == 1, (count, hits)
print('signals total =', len(signals), 'valid =', count)
print(hits[0])
