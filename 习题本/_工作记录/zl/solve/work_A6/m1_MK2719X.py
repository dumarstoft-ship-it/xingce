# MK2719X-M3 calculations
# Q1: 2022 primary / 2022 graduate - 1
p23, dp = 518.49, -4.61
g23, dg = 12.36, 0.63
p22 = p23 - dp
g22 = g23 - dg
print("Q1 p22=%.2f g22=%.2f ratio=%.4f 多倍=%.4f" % (p22, g22, p22/g22, p22/g22-1))

# Q2: growth rates of in-school students
groups = [
 ("普通小学", 518.49, -4.61),
 ("普通初中", 270.78, 7.04),
 ("普通高中", 147.30, 5.07),
 ("中职", 70.37, -4.26),
 ("研究生", 12.36, 0.63),
 ("本专科", 177.80, 9.29),
 ("特教在校", 5.17, -0.19),
 ("幼儿园", 183.70, -32.3),
 ("特教招收(非在校)", 0.80, 0.06),
]
for name, cur, inc in groups:
    print("Q2 %s growth=%.4f%%" % (name, inc/(cur-inc)*100))
comb_cur = 12.36+177.80; comb_inc = 0.63+9.29
print("Q2 高校合计 growth=%.4f%%" % (comb_inc/(comb_cur-comb_inc)*100))

# Q3: average books per secondary vocational school growth
books_g = 0.182
n23, dn = 497, 2
n22 = n23 - dn
avg_g = (1+books_g)/(n23/n22) - 1
print("Q3 avg growth=%.4f%%" % (avg_g*100))
print("Q3 check: avg23=%.4f avg22=%.4f" % (1762.28/497, 1762.28/1.182/495))

# Q4: 2022 average kindergarten room area
area23 = 1669.7  # 万平方米
area22 = area23/(1-0.007)
k22 = 15327 + 671
print("Q4 area22=%.4f 万m2, k22=%d, avg=%.4f m2" % (area22, k22, area22*1e4/k22))
print("Q4 wrong-unit avg=%.4f" % (area22/k22*1e4/1e4))

# Q5
inc1 = 1762.28*0.182/1.182
print("Q5-1 增量=%.4f 万册" % inc1)
k2028 = 15327 - 5*671
print("Q5-2 2028 kindergartens=%d" % k2028)
tot = 518.49+270.78+147.30+70.37+12.36+177.80+5.17+183.70
print("Q5-3 total=%.2f" % tot)
