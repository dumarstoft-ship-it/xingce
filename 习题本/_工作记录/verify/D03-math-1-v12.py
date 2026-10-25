# D03-math-1-v12: 全程140千米；乙晚出发，在距出发地60千米处追上甲，比甲早24分钟到达；求乙晚出发多少分钟
from fractions import Fraction as F

TOTAL, CATCH, EARLY = 140, 60, F(24, 60)
OPTS = {'A': 18, 'B': 24, 'C': 32, 'D': 42}

delays = set()
count = 0
# 穷举两车速度（0.5千米/时步长，至 150），由“在60千米处追上”确定晚出发时间，再检验“早到24分钟”
for a2 in range(2, 301):
    va = F(a2, 2)
    for b2 in range(a2 + 1, 301):
        vb = F(b2, 2)
        delay = CATCH / va - CATCH / vb               # 两车同时到达追上点
        if TOTAL / va - (delay + TOTAL / vb) == EARLY:
            # 复核：追上之前乙始终在甲后面，追上之后乙在甲前面
            t_catch = CATCH / va
            for frac in (F(1, 4), F(1, 2), F(3, 4)):
                tt = t_catch * frac
                if tt > delay:
                    assert vb * (tt - delay) < va * tt
            tt = t_catch + F(1, 10)
            assert vb * (tt - delay) > va * tt
            delays.add(delay * 60)
            count += 1
assert count > 1                     # 速度不唯一……
assert len(delays) == 1, delays      # ……但晚出发时间唯一
ans = delays.pop()
hit = [k for k, v in OPTS.items() if v == ans]
assert len(hit) == 1, (ans, hit)
# 干扰项来源
assert EARLY * 60 == OPTS['B']                                   # 以为时间差不变
assert EARLY * 60 * F(TOTAL - CATCH, CATCH) == OPTS['C']         # 比例用反
assert ans + EARLY * 60 == OPTS['D']                             # 求成全程少用的时间
print('速度组数', count, '晚出发', ans, '分钟')
print(hit[0])
