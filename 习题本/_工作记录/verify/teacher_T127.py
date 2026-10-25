# teacher T127（2024江苏B）小王0.6、小李0.5、两人都入选0.25，求至少一人入选的概率
from fractions import Fraction as F

OPTS = {'A': F(6, 10), 'B': F(75, 100), 'C': F(8, 10), 'D': F(85, 100)}
PW, PL, PWL = F(6, 10), F(5, 10), F(25, 100)
print('独立吗？', PWL == PW * PL, '(0.6×0.5 =', PW * PL, ')')
# 把样本空间拆成4个互斥原子事件，检验数据自洽
atoms = {'王且李': PWL, '仅王': PW - PWL, '仅李': PL - PWL}
atoms['都不'] = 1 - sum(atoms.values())
assert all(v >= 0 for v in atoms.values()), atoms
P = atoms['王且李'] + atoms['仅王'] + atoms['仅李']
print('P =', P, '| 误按独立用对立事件 =', 1 - (1 - PW) * (1 - PL))
hits = [k for k, v in OPTS.items() if v == P]
assert len(hits) == 1, hits
print(hits[0])
