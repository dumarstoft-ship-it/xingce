# D02-math-1-v01  820箱订单：A线先6天、B线再5天恰好完成；A线总产量比B线多20箱；求B线每天产量
# 从题面数据出发：穷举两线的日产量（正整数），找出同时满足两个条件的解。
TOTAL, DA, DB, DIFF = 820, 6, 5, 20
OPTS = {'A': 70, 'B': 74, 'C': 80, 'D': 84}

sols = [(a, b) for a in range(1, TOTAL + 1) for b in range(1, TOTAL + 1)
        if DA * a + DB * b == TOTAL and DA * a - DB * b == DIFF]
assert len(sols) == 1, sols
a, b = sols[0]
hits = [k for k, v in OPTS.items() if v == b]
assert len(hits) == 1, hits

# 干扰项来源核对
assert OPTS['A'] == a                                    # 求成A线的日产量
assert (TOTAL + DIFF) // 2 / DB == OPTS['D']            # 把多出的20箱算到B线头上
passes = [v for v in OPTS.values() if (TOTAL - DB * v) % DA == 0 and TOTAL - DB * v > 0]
assert sorted(passes) == [74, 80]                        # 只做整除筛选会剩74和80
assert DA * ((TOTAL - DB * 74) // DA) - DB * 74 != DIFF  # 74不满足“多20箱”
print('A daily', a, 'B daily', b)
print(hits[0])
