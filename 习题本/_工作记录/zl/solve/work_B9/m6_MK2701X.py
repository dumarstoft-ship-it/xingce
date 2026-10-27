# MK2701X-M1
sales = [12.1,14.9,16.3,16.5,19.4,23.3,23.9,24.9,27.7,31.0,32.3,36.4]
g = [42.5,98.0,84.3,144.5,94.4,93.0,77.0,72.8,64.4,80.2,89.5,92.6]
print("sum months", sum(sales))
# Q1
nev22 = 949.5/1.379
g22 = 37.9+55.5
nev21 = nev22/(1+g22/100)
print("Q1 nev2022", nev22, "g2022", g22, "nev2021", nev21)
# Q2
ph22 = 280.7/1.847
s23 = 280.7/949.5; s22 = ph22/nev22
print("Q2 share23", s23*100, "share22", s22*100, "diff", (s23-s22)*100)
print("  formula", s23*(0.847-0.379)/1.847*100)
# Q3/Q4
q = [sum(sales[i*3:i*3+3]) for i in range(4)]
print("quarters", q)
print("Q3 Q4 qoq", (q[3]/q[2]-1)*100)
print("Q4 max/min -1", max(q)/min(q)-1, "ratio", max(q)/min(q))
# Q5
print("Q5A 2022 PHEV growth", 84.7+66.9)
mar22 = sales[2]/(1+g[2]/100); apr22 = sales[3]/(1+g[3]/100)
print("Q5B Mar22", mar22, "Apr22", apr22, "mom", (apr22/mar22-1)*100)
print("Q5C H1 avg", sum(sales[:6])/6)
imax = g.index(max(g)); imin = g.index(min(g))
print("Q5D fastest month", imax+1, sales[imax], "slowest", imin+1, sales[imin])
