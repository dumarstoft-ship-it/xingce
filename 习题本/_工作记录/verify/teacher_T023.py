# teacher_T023  55人都参加了培训班：书法35、美术28、舞蹈31，三种都参加6人。只参加一种的人数
OPTS = {'A': 45, 'B': 33, 'C': 29, 'D': 22}
TOTAL, SH, MS, WD, ALL3 = 55, 35, 28, 31, 6
only_one = set()
for ab in range(0, 40):            # 只参加书法+美术
    for ac in range(0, 40):        # 只参加书法+舞蹈
        for bc in range(0, 40):    # 只参加美术+舞蹈
            a = SH - ab - ac - ALL3
            b = MS - ab - bc - ALL3
            c = WD - ac - bc - ALL3
            if min(a, b, c) < 0:
                continue
            if a + b + c + ab + ac + bc + ALL3 == TOTAL:
                only_one.add(a + b + c)
assert len(only_one) == 1, only_one
ans = only_one.pop()
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
assert OPTS['A'] == SH + MS + WD + ALL3 - TOTAL    # 标准型公式里的"两两交集之和"
assert OPTS['B'] == TOTAL - ans                    # 参加两种及以上的人数
print('只参加一种 =', ans)
print(hits[0])
