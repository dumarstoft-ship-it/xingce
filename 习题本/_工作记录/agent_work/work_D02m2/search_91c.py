# v04 rework search: 甲乙原计划N天; 合作a天后甲抽调; 乙单独b天时恰完成p; 丙加入(丙单独T丙天);
# x天后甲返回, 三队干到完工, 最终比原计划【推迟】d天。问甲队共离开多少天(b+x)。
from fractions import Fraction as F

out = []
for N in range(12, 37):
    if N in (30, 25):          # 避开种子30天、旧版25天
        continue
    for a in range(2, 10):
        for b in range(2, 14):
            for p in [F(2, 5), F(1, 3), F(3, 10), F(1, 4), F(3, 5), F(2, 3)]:
                den = a + b - p * N
                if den == 0:
                    continue
                r = (p * N - a) / den            # 乙/甲
                if r <= 0 or r.denominator > 3 or r.numerator > 5:
                    continue
                s = r.denominator
                e1, e2 = s, int(r * s)
                if (e1, e2) in [(1, 2), (1, 3)]:   # 避开种子(乙=2甲)和旧版(乙=3甲)
                    continue
                W = N * (e1 + e2)
                for d in range(1, 5):
                    rem = N + d - a - b
                    if rem < 4:
                        continue
                    for c in range(1, 13):
                        if W % c:
                            continue
                        x = F((e1 + e2 + c) * rem - (1 - p) * W, e1)
                        if x.denominator != 1 or x < 2 or rem - x < 2:
                            continue
                        x = int(x)
                        absent = b + x
                        trio = rem - x
                        jia_work_days = a + trio
                        # 推迟/提前看反：用 N-d 算
                        rem2 = N - d - a - b
                        x2 = F((e1 + e2 + c) * rem2 - (1 - p) * W, e1)
                        out.append(dict(N=N, a=a, b=b, p=str(p), jia=e1, yi=e2, c=c, Tc=W // c, W=W, d=d,
                                        x=x, absent=absent, trio=trio, jia_days=jia_work_days, x_if_early=str(x2)))
print(len(out))
for o in out:
    if o['Tc'] <= 60 and o['p'] in ('2/5', '1/3', '3/5', '1/4') and o['c'] < o['jia'] + o['yi']:
        print(o)
