# D01-math-h-v15 同一批沙袋：2辆大货车+4辆小货车运5趟恰好运完；1辆大货车+7辆小货车运4趟也恰好运完。
# 现派大、小货车共14辆，运2趟恰好运完（每车每趟满载、同型号载重相同），求派出的大货车辆数。
# 独立求解：枚举大、小货车每趟载重（整数单位，覆盖所有可能的载重比），保留两方案总量相等的情形；
# 对每种情形枚举大货车辆数 x（0～14），找出"2趟恰好运完"的 x，确认处处唯一且相同；再复核干扰项的错误路径。
from fractions import Fraction as Fr

OPTS = {'A': 6, 'B': 8, 'C': 1, 'D': 2}
PLAN1 = (2, 4, 5)      # 大车数, 小车数, 趟数
PLAN2 = (1, 7, 4)
N_TRUCKS, TRIPS = 14, 2

answers, ratios = set(), set()
for big in range(1, 301):
    for small in range(1, 301):
        w1 = PLAN1[2] * (PLAN1[0] * big + PLAN1[1] * small)
        w2 = PLAN2[2] * (PLAN2[0] * big + PLAN2[1] * small)
        if w1 != w2:
            continue
        ratios.add(Fr(big, small))
        xs = [x for x in range(N_TRUCKS + 1)
              if TRIPS * (x * big + (N_TRUCKS - x) * small) == w1]
        assert len(xs) == 1, (big, small, xs)
        answers.add(xs[0])
assert len(ratios) == 1 and len(answers) == 1, (ratios, answers)
r = ratios.pop()
ans = answers.pop()
assert r == Fr(4, 3)                                   # 大∶小＝4∶3

# 按份数复核：大车4份、小车3份
B, S = r.numerator, r.denominator
W = PLAN1[2] * (PLAN1[0] * B + PLAN1[1] * S)           # 100 份
per_trip = Fr(W, TRIPS)                                # 每趟 50 份
assert W == 100 and per_trip == 50 and (per_trip - N_TRUCKS * S) / (B - S) == ans


def big_count(b, s):
    w = PLAN1[2] * (PLAN1[0] * b + PLAN1[1] * s)
    return (Fr(w, TRIPS) - N_TRUCKS * s) / (b - s)


# 干扰项的错误路径
assert big_count(S, B) == OPTS['C']                    # 载重比写反（大∶小＝3∶4）
assert (per_trip - N_TRUCKS * S) / B == OPTS['D']      # 补差时除以大车载重4，而不是每车差1份
assert N_TRUCKS - ans == OPTS['A']                     # 求成小货车辆数

hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, hits
print('big:small =', r, 'total parts =', W, 'big trucks =', ans)
print(hits[0])
