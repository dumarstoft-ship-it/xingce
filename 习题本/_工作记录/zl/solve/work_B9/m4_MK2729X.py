# MK2729X-M1
life = [177,54,77,63,62,92,62,51,52,37,53,64]
tot12 = 139.56
# Q1
print("Q1", (1.22/1.0966-1)*100)
# Q2
life_share = 64/tot12
acc = 1-life_share-0.2916-0.2271
print("Q2 life share", life_share*100, "accident", acc*100, "diff", (life_share-acc)*100)
# Q3
for m in range(6,12):
    inc = life[m]-life[m-1]
    print(f"Q3 month {m+1} inc {inc} rate {inc/life[m-1]*100:.2f}")
# Q4
h1 = sum(life[:6]); h2 = sum(life[6:])
print("Q4 H1", h1, h1/6, "H2", h2, h2/6, "diff", h1/6-h2/6)
# Q5
print("Q5A persons 万人", tot12*1e8/790.18/1e4)
print("Q5B Q2 sum", sum(life[3:6]), "Q1 sum", sum(life[0:3]))
print("Q5D 2022-12", tot12/1.0966)
