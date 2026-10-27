# MK2709X-M2 通信业
print("== Q1 接入网 - (本地网中继+长途) ==")
tot = 7377
d = 59.9 - (38.5 + 1.6)
print("pct diff", d, " value", tot * d / 100)

print("== Q2 2024年6月末光缆总长度 ==")
print(7377 / 1.099)

print("== Q3 增长量最大地区及占比 ==")
reg = {"东": (780.4, 15.7), "中": (441.8, 16.7), "西": (534.3, 15.4), "东北": (110.3, 25.8)}
for k, (v, r) in reg.items():
    print(k, "增量", v * r / (100 + r))
S = sum(v for v, r in reg.values())
print("total", S)
for k, (v, r) in reg.items():
    print(k, "占比", v / S * 100)

print("== Q4 2024年末渗透率 ==")
pen = {"东": (61.5, 4.8), "中": (62.6, 5.4), "西": (61.5, 5.1), "东北": (61.9, 5.7)}
base = {k: round(a - b, 1) for k, (a, b) in pen.items()}
print(base, sorted(base, key=base.get))

print("== Q5 ==")
print("A 10G PON增长率", 201.9 / (3022 - 201.9) * 100)
print("B 5G月均净增", 29.8 / 6)
print("C 移动基站总数", 454.9 / 0.357)
print("D 非光纤净增", 3244 - 3264)
print("   check 光纤占比", 11.93 / 12.34 * 100)
