# MK2729X-M1 S city insurance premiums
life = [177, 54, 77, 63, 62, 92, 62, 51, 52, 37, 53, 64]  # 1-12月 寿险 (亿元)
tot12 = 139.56; g = 0.0966
# Q1
print("Q1 2022 Dec growth", 1.22/(1+g) - 1)
# Q2
s_life = life[11]/tot12*100
s_acc = 100 - s_life - 29.16 - 22.71
print("Q2 life share", s_life, "accident share", s_acc, "diff pp", s_life - s_acc)
for lv in (63.5, 64.5):
    sl = lv/tot12*100; sa = 100 - sl - 29.16 - 22.71
    print("   sensitivity life=", lv, "diff", sl - sa)
# Q3
for m in range(7, 13):
    inc = life[m-1] - life[m-2]
    print("Q3 month", m, "mom incr", inc, "rate", inc/life[m-2])
# Q4
h1 = sum(life[:6]); h2 = sum(life[6:])
print("Q4 H1 sum", h1, "avg", h1/6, "H2 sum", h2, "avg", h2/6, "diff", h1/6 - h2/6)
# Q5
print("Q5A population implied (万人)", tot12*1e8/790.18/1e4)
print("Q5B Q2 life", sum(life[3:6]), "Q1 life", sum(life[0:3]))
print("Q5D 2022 Dec total", tot12/(1+g))
