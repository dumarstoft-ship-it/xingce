# T103 2025国考地市级：65人中至少一项认证占80%；没有甲认证=有乙认证；仅丙3人；三项都有6人；求仅甲乙
TOTAL = 65
NONE = TOTAL * 20 // 100
ONLY_C, ALL3 = 3, 6
OPTS = {'A': 10, 'B': 13, 'C': 16, 'D': 19}
assert NONE * 100 == TOTAL * 20

rest = TOTAL - NONE - ONLY_C - ALL3      # 只甲、只乙、甲乙、甲丙、乙丙 之和
vals = set()
for oa in range(rest + 1):
    for ob in range(rest + 1 - oa):
        for ab in range(rest + 1 - oa - ob):
            for ac in range(rest + 1 - oa - ob - ab):
                bc = rest - oa - ob - ab - ac
                no_a = NONE + ob + ONLY_C + bc
                has_b = ob + ab + bc + ALL3
                if no_a == has_b:
                    vals.add(ab)
assert len(vals) == 1, vals
ab = vals.pop()
assert ab + ALL3 == OPTS['C']            # 干扰项：把三项都有的也算进来
print('only A&B =', ab)
print([k for k, v in OPTS.items() if v == ab][0])
