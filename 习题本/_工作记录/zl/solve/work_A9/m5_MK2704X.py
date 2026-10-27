# MK2704X-M3 社会组织、基金会
yrs = [2018, 2019, 2020, 2021, 2022]
non = dict(zip(yrs, [5109, 5670, 6296, 6688, 7105]))   # 不具有公开募捐资格
pub = dict(zip(yrs, [1925, 1915, 2136, 2189, 2214]))   # 具有公开募捐资格
gr = dict(zip(yrs, [11.5, 7.8, 11.2, 5.3, 5.0]))
tot = {y: non[y] + pub[y] for y in yrs}
print("totals", tot)
for y in yrs[1:]:
    print(" check growth", y, (tot[y] / tot[y - 1] - 1) * 100, "label", gr[y])

print("== Q1 具有公开募捐资格占比 ==")
for y in yrs:
    s = pub[y] / tot[y] * 100
    print(y, s, "具有增速", (pub[y] / pub[y - 1] - 1) * 100 if y > 2018 else None)

print("== Q2 2022年社会组织数增速 ==")
print((1.008 / 1.02 - 1) * 100)

print("== Q3 不具有资格增速 ==")
for y in yrs[1:]:
    print(y, non[y] - non[y - 1], (non[y] / non[y - 1] - 1) * 100)
print(" cross", 561 * 5670, 626 * 5109)

print("== Q4 2019年基金会/社会组织 ==")
so19 = 89.1 - 2.5
print("社会组织2019(万)", so19, "比重%", tot[2019] / (so19 * 1e4) * 100)

print("== Q5 ==")
print("A 2022人均吸纳", 1108.3 / 89.1)
print("B 2022基金会比重%", tot[2022] / 891000 * 100)
print("C 2017基金会", tot[2018] / 1.115)
print("D 不具有增量 2020", non[2020] - non[2019], "2019", non[2019] - non[2018])
