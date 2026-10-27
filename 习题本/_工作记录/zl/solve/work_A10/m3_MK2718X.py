# MK2718X-M2 NEV import/export Dec 2023
names = ["纯电动乘用车", "插电式混动乘用车", "非插电式混动乘用车", "纯电动客车", "混合动力客车"]
dec = [23.1, 6.5, 3.9, 1.6, 0.4]
dec_g = [27.4, 192.1, 804.5, 23.1, 277.7]
cum = [341.3, 43.2, 16.3, 16.8, 0.5]
cum_share = [81.6, 10.3, 3.9, 4.0, 0.1]
cum_g = [69.9, 70.9, 462.0, 51.2, -52.2]

# Q1
phev22 = 43.2/(1+0.709); bus22 = 16.8/(1+0.512)
print("Q1 2022 PHEV", phev22, "BEV bus", bus22, "ratio", phev22/bus22, "多倍", phev22/bus22-1)

# Q2
exp_1_11 = 177.3 - 15.1; imp_1_11 = 15.0 - 1.8
print("Q2 1-11 export", exp_1_11, "import", imp_1_11, "net", exp_1_11 - imp_1_11)

# Q3
cnt = 0
for n, d, dg, c, cg in zip(names, dec, dec_g, cum, cum_g):
    s23 = d/c
    s22 = (d/(1+dg/100))/(c/(1+cg/100))
    up = s23 > s22
    cnt += up
    print("Q3", n, "share23", round(s23, 4), "share22", round(s22, 4), "higher", up)
print("Q3 count", cnt)

# Q4
for n, d, c in zip(names, dec, cum):
    m = (c-d)/11
    print("Q4", n, "1-11 monthly avg", round(m, 4), "Dec", d, "avg>Dec", m > d)

# Q5
tot = sum(dec)
print("Q5 Dec total", tot)
for n, d in zip(names, dec):
    print("Q5", n, "share", round(d/tot*100, 2), "% angle", round(d/tot*360, 1))
print("Q5 cum-based shares", cum_share)
