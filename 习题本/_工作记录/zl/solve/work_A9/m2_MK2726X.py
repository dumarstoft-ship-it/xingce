# MK2726X-M1 插混新能源汽车活跃量 2024年9月
SUV, CAR, MPV = 307.08, 245.54, 32.81
rS, rC, rM = 5.6, 6.9, 6.4
print("== Q1 比亚迪SUV - 比亚迪轿车 ==")
a, b = SUV * 0.588, CAR * 0.687
print(a, b, a - b)

print("== Q2 2024年8月 SUV - MPV ==")
s8, m8 = SUV / (1 + rS / 100), MPV / (1 + rM / 100)
print(s8, m8, s8 - m8)
# trap: current diff / or no base
print(" 现期差", SUV - MPV)

print("== Q3 环比增量 ==")
d = {"驱逐舰05": (26.94, 7.7), "汉DM": (31.73, 3.6), "唐DM": (43.44, 2.6), "宋Pro-DM": (46.02, 3.1)}
for k, (v, r) in d.items():
    print(k, v * r / (100 + r))

print("== Q4 2024年8月 秦PLUS-DM / 轿车 ==")
q, rq = 72.98, 3.2
cur = q / CAR
base = cur * (1 + rC / 100) / (1 + rq / 100)
print("现期", cur * 100, "基期", base * 100)

print("== Q5 ==")
print("A 岚图-别克 万辆", MPV * (0.140 - 0.040), "辆", MPV * (0.140 - 0.040) * 1e4)
print("B 上汽集团/五菱", 4.6 / 2.3)
print("C 无同比数据; 2024年8月 D9", 16.70 / 1.037, " 5系", 9.98 / (1 - 0.002))
print("D 2024年8月 秦L-DM", 12.62 / 1.459)
