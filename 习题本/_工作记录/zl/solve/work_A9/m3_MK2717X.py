# MK2717X-M1 洗护用品分渠道市场规模（亿元）
yrs = [2017, 2018, 2019, 2020, 2021]
on = dict(zip(yrs, [605, 722, 874, 1096, 1249]))
off = dict(zip(yrs, [1286, 1300, 1349, 1355, 1430]))
tot = {y: on[y] + off[y] for y in yrs}
print("totals", tot)
print("== Q1 合计 ==", sum(tot.values()))

print("== Q2 同比增速 ==")
for y in yrs[1:]:
    print(y, (tot[y] / tot[y - 1] - 1) * 100)

print("== Q3 保持2021年增长量 ==")
don, doff = on[2021] - on[2020], off[2021] - off[2020]
print("增长量", don, doff)
a, b = on[2021], off[2021]
for y in range(2022, 2027):
    a += don; b += doff
    print(y, a, b, b / (a + b) * 100)

print("== Q4 线下占比-线上占比 (百分点) ==")
for y in yrs:
    print(y, (off[y] - on[y]) / tot[y] * 100)

print("== Q5 ==")
for y in [2018, 2019, 2020]:
    print("A", y, "线上", (on[y] / on[y - 1] - 1) * 100, "线下", (off[y] / off[y - 1] - 1) * 100)
print("B 线上占比 2019", on[2019] / tot[2019] * 100, "2020", on[2020] / tot[2020] * 100)
print("C 增量 2021", on[2021] - on[2020], "2018", on[2018] - on[2017], "倍数", (on[2021] - on[2020]) / (on[2018] - on[2017]))
print("D 线上合计", sum(on.values()))
