# MK26ZX-M3 工业机器人
# text
sales23 = 31.6        # 万台, 2023 市场销量, +4.29%
prod24 = 55.64        # 万台, 2024 规上产量, +14.2%
g_prod24 = 0.142
sales24_est = 30.0    # 万台 预计
exp23 = 21268         # 台 全年出口量
coop23 = 6058         # 协作机器人出口量
exp24q3 = 17906       # 2024前三季度出口量 +14.95%
g_exp24q3 = 0.1495
coop24q3 = 2000       # 约0.2万台, +42.32%
g_coop24q3 = 0.4232

events = {2020: 115, 2021: 162, 2022: 153, 2023: 130, 2024: 125}
amount = {2020: 633.24, 2021: 268.08, 2022: 256.81, 2023: 162.17, 2024: 508.09}

print("Q1")
prod23 = prod24 / (1 + g_prod24)
print(" prod23 =", prod23, " diff =", prod23 - sales23)

print("Q2")
exp23q3 = exp24q3 / (1 + g_exp24q3)
q4 = exp23 - exp23q3
print(" 2023Q1-3 =", exp23q3, " Q4 =", q4, " share =", q4 / exp23)
# shortcut: 17906/1.15
print(" approx 17906/1.15 =", 17906 / 1.15)

print("Q3")
avg = {y: amount[y] / events[y] for y in events}
for y in avg:
    print(" ", y, avg[y])
r = avg[2024] / avg[2023]
print(" ratio =", r, " increase times =", r - 1)

print("Q4")
print(" 2021 %.4f 2022 %.4f 2023 %.4f" % (avg[2021], avg[2022], avg[2023]))

print("Q5")
print(" A: 30/31.6-1 =", sales24_est / sales23 - 1)
print(" B: 6058/21268 =", coop23 / exp23)
inc = coop24q3 * g_coop24q3 / (1 + g_coop24q3)
print(" C: increase =", inc, " monthly =", inc / 9)
# what base would be needed for >90 per month
need = 90 * 9 * (1 + g_coop24q3) / g_coop24q3
print("    needed 2024 Q1-3 coop for >90/month:", need)
s = sum(events.values())
print(" D: total =", s, " avg =", s / 5)
