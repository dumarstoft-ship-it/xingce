# teacher_T006  两袋米共440kg，甲吃1/3、乙吃1/2后剩余比8:5，求两袋原重
from fractions import Fraction as F

TOTAL = 440
EAT_JIA, EAT_YI = F(1, 3), F(1, 2)
RATIO = F(8, 5)
OPTS = {'A': (80, 100), 'B': (160, 100), 'C': (200, 240), 'D': (240, 200)}

sols = [(x, TOTAL - x) for x in range(1, TOTAL)
        if (1 - EAT_JIA) * x / ((1 - EAT_YI) * (TOTAL - x)) == RATIO]
assert len(sols) == 1, sols
ans = sols[0]
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
assert OPTS['B'] == ((1 - EAT_JIA) * ans[0], (1 - EAT_YI) * ans[1])   # 答成剩余量
assert OPTS['A'] == (EAT_JIA * ans[0], EAT_YI * ans[1])               # 答成吃掉的量
assert OPTS['C'] == ans[::-1]                                         # 比例颠倒
print('甲, 乙 =', ans)
print(hits[0])
