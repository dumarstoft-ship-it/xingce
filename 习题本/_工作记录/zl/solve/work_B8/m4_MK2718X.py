# MK2718X-M2 新能源汽车进出口
# 表2: name: (Dec val, Dec g%, annual val, share%, annual g%)
T2 = {'纯电动乘用车':(23.1,27.4,341.3,81.6,69.9),'插混乘用车':(6.5,192.1,43.2,10.3,70.9),
      '非插混乘用车':(3.9,804.5,16.3,3.9,462.0),'纯电动客车':(1.6,23.1,16.8,4.0,51.2),'混动客车':(0.4,277.7,0.5,0.1,-52.2)}
# Q1 2022: PHEV / BEV bus
p22 = 43.2/1.709; b22 = 16.8/1.512
print("Q1 2022 PHEV", p22, "BEV bus", b22, "ratio", p22/b22, "多几倍", p22/b22-1)
print("   2023 ratio", 43.2/16.8, "多", 43.2/16.8-1)
# Q2 1-11 net export volume
exp111 = 177.3-15.1; imp111 = 15.0-1.8
print("Q2 1-11 export", exp111, "import", imp111, "net", exp111-imp111, "| annual net", 177.3-15.0, "| 177.3-1.8", 177.3-1.8)
# Q3 Dec share of annual vs last year
cnt = 0
for k,(m,gm,a,s,ga) in T2.items():
    cur = m/a; prev = (m/(1+gm/100))/(a/(1+ga/100))
    print("Q3", k, "cur", round(cur,4), "prev", round(prev,4), "higher" if cur>prev else "lower")
    cnt += cur>prev
print("Q3 count", cnt)
# Q4 1-11 monthly avg vs Dec
for k,(m,gm,a,s,ga) in T2.items():
    avg = (a-m)/11
    print("Q4", k, "1-11 avg", round(avg,3), "Dec", m, "avg>Dec" if avg>m else "no", "| a vs 12m", a, 12*m)
# Q5 Dec shares
tot = sum(v[0] for v in T2.values())
print("Q5 Dec total", tot)
for k,v in T2.items():
    print("Q5", k, round(v[0]/tot*100,2), "% ->", round(v[0]/tot*360,1), "deg")
