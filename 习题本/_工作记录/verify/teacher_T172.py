# teacher T172（2012国考）乙7:00步行，甲9:00出发跑速为乙的2.5倍，每跑半小时休息半小时，何时追上
from fractions import Fraction as F

OPTS = {'A': (10, 20), 'B': (12, 10), 'C': (14, 30), 'D': (16, 10)}
V_YI, V_JIA, JIA_START, RUN, REST = F(1), F(5, 2), F(2), F(1, 2), F(1, 2)   # 时间以7:00为0，单位小时

def catch_time():
    t, p = JIA_START, F(0)                        # 当前时刻、甲的位置
    while True:
        s = (V_JIA * t - p) / (V_JIA - V_YI)      # 若一直跑，追上的时刻
        if t <= s <= t + RUN:
            return s
        p += V_JIA * RUN
        t += RUN + REST                           # 休息时乙在走，差距只会变大

s = catch_time()
h = 7 + s
hh, mm = int(h), (h - int(h)) * 60
print('追上时刻 %d:%02d' % (hh, mm))
hits = [k for k, v in OPTS.items() if v == (hh, mm)]
assert len(hits) == 1, hits
print(hits[0])
