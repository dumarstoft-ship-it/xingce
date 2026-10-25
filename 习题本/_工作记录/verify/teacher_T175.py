# teacher T175 甲乙交替（甲先整数天完成，乙先多1/4天），甲单独8天后两人合作4天完成，求甲单独完成天数
from fractions import Fraction as F

OPTS = {'A': 14, 'B': 15, 'C': 16, 'D': 18}

def finish(cycle, total=F(1)):
    done, t = F(0), 0
    while True:
        r = cycle[t % 2]
        if done + r >= total:
            return t + (total - done) / r
        done += r
        t += 1

ok = []
for key, T in OPTS.items():
    a = F(1, T)
    b = (1 - 12 * a) / 4                           # 8a + 4(a+b) = 1
    if b <= 0:
        continue
    t1, t2 = finish((a, b)), finish((b, a))
    print(key, '甲单独', T, '天 | 乙效率', b, '| 甲先', t1, '| 乙先', t2)
    if t1.denominator == 1 and t2 - t1 == F(1, 4):
        ok.append(key)
assert len(ok) == 1, ok
print(ok[0])
