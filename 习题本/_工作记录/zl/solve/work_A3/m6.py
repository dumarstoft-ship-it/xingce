# MK2718X-M1 cosmetics trade
ex_inc = 37.4*0.326/1.326
im_inc = 144.3*(-0.198)/(1-0.198)
print("Q1: export inc =", ex_inc, " import inc =", im_inc, " diff =", ex_inc-im_inc, " (abs trap:", abs(im_inc)-ex_inc, ")")
sh22 = 0.205*1.167/1.079
us23 = 65.1*0.205; us22 = us23/1.079; tot22 = 65.1/1.167
print("Q2: 2022 US share =", sh22, " check:", us22/tot22, " us22 =", us22)
imp22 = 179.4/(1-0.194); exp22 = 65.1/1.167
print("Q3: imp22 =", imp22, " exp22 =", exp22, " total =", imp22+exp22)
b20 = 25.0/1.15
print("Q4: beauty export 2020 =", b20, " 2023-2020 =", 37.4-b20, " (trap 2023-2021 =", 37.4-25.0, ")")
# Q5
pi22 = 25.3/(1-0.194); pe22 = 21.7/1.131
print("Q5-1: personal care total 2022 =", pi22+pe22, " 2023 =", 25.3+21.7, " growth =", (25.3+21.7)/(pi22+pe22)-1)
e21 = 65.1/1.159**2
print("Q5-2: export 2021 =", e21, " ; implied 2022 growth =", 1.159**2/1.167-1)
print("Q5-3: beauty inc 2021 =", 25.0*0.15/1.15, " ; cosmetics export 2020 not given -> cannot compute")
