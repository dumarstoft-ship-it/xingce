# real 2026ZJA-48: 8点同时出发，甲每小时比乙多走1千米；11点甲休息1小时，乙在12点赶上甲；求此时乙走了多少千米
from fractions import Fraction as F

DV = 1
START, REST_FROM, REST_TO, CATCH = 8, 11, 12, 12
OPTS = {'A': 9, 'B': 12, 'C': 15, 'D': 18}

def pos_jia(t, va):
    if t <= REST_FROM:
        return va * (t - START)
    if t <= REST_TO:
        return va * (REST_FROM - START)
    return va * (t - START - (REST_TO - REST_FROM))

sols = set()
for k in range(1, 3001):                     # 乙速 0.01~30 千米/时
    vb = F(k, 100)
    va = vb + DV
    # 12点两人位置相同
    if vb * (CATCH - START) != pos_jia(F(CATCH), va):
        continue
    # 12点之前乙一直在甲后面（“赶上”发生在12点）
    assert all(vb * (t - START) < pos_jia(t, va)
               for t in [START + F(i, 60) for i in range(1, (CATCH - START) * 60)])
    sols.add(vb * (CATCH - START))
assert len(sols) == 1, sols
ans = sols.pop()
hit = [k for k, v in OPTS.items() if v == ans]
assert len(hit) == 1, (ans, hit)
assert ans * 3 // 4 == OPTS['A']             # 按3小时算乙的路程
print('乙走了', ans, '千米')
print(hit[0])
