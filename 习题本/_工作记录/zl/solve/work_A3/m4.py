# MK2729X-M2 2022 passenger/tourism/retail
r = (1-0.346)/(1-0.327)-1
print("Q1: per-trip distance growth =", r, " check:", 12921/56, "vs 2021", (12921/0.654)/(56/0.673))
base = 1987/0.358
print("Q2: 2021 rural spend =", base, " 2022 =", base-1987)
dom21 = 25.3/(1-0.221); urb21 = 19.3/(1-0.177)
rur22 = 25.3-19.3; rur21 = dom21-urb21
print("Q3: dom21 =", dom21, " urb21 =", urb21, " rur21 =", rur21, " rur22 =", rur22, " growth =", rur22/rur21-1)
inc_goods = 395792*0.005/1.005
inc_food = 43941*(-0.063)/(1-0.063)
print("Q4: goods inc =", inc_goods, " catering inc =", inc_food, " diff =", inc_goods-inc_food, " (trap sum-of-abs? ", inc_goods+inc_food, ")")
# Q5
t21 = 439733/0.998; u21 = 380448/0.997; ru21 = t21-u21
print("Q5-1: rural 2021 =", ru21, " growth =", 59285/ru21-1, " share22 =", 59285/439733, " share21 =", ru21/t21)
print("Q5-2: 2023 =", 20444*1.3, " 2024 =", 20444*1.3**2, " 2025 =", 20444*1.3**3)
print("Q5-3: urban share =", 19.3/25.3)
