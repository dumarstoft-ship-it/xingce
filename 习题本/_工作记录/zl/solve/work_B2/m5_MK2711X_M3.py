# MK2711X-M3 Fujian trade table
# city: {item: (feb, feb_g, cum, cum_g)}
T = {
 '厦门': {'tot':(696.4,23.5,1482.3,None),'exp':(268.4,-2.1,675.6,-6.9),'imp':(428.0,47.8,806.7,27.8)},
 '泉州': {'tot':(130.6,-16.5,385.2,-13.7),'exp':(84.5,-22.2,294.1,-14.3),'imp':(46.1,-3.6,91.1,-12.0)},
 '漳州': {'tot':(77.6,2.8,171.6,-7.0),'exp':(51.0,26.5,111.6,-4.9),'imp':(26.6,-24.5,60.0,-10.7)},
 '龙岩': {'tot':(35.4,-3.0,71.2,-26.4),'exp':(21.3,-7.6,40.7,-23.7),'imp':(14.1,4.9,30.5,-29.8)},
}
print("Q1 Feb mom decrease")
for c,d in T.items():
    feb,_,cum,_ = d['tot']; jan = cum-feb
    print(c, "Jan", round(jan,1), "Feb", feb, "decrease", round(jan-feb,1), "mom%", round((feb/jan-1)*100,2))
print("Q2 Jan > 1-2 avg")
for c,d in T.items():
    feb,_,cum,_ = d['tot']; jan=cum-feb
    print(c, round(jan,1), cum/2, jan>cum/2)
print("Q3 Xiamen 1-2 total growth")
e22 = 675.6/(1-0.069); i22 = 806.7/(1+0.278)
print(e22, i22, e22+i22, (1482.3/(e22+i22)-1)*100, "export weight", e22/(e22+i22))
print("Q4 Quanzhou 2022 Jan export")
c22 = 294.1/(1-0.143); f22 = 84.5/(1-0.222)
print(c22, f22, c22-f22)
print("Q5")
print("A Quanzhou Jan export share", (294.1-84.5)/(385.2-130.6)*100)
jan_ly = 71.2-35.4
print("B Longyan Feb yoy -3.0 vs mom", (35.4/jan_ly-1)*100)
print("C trade balance 1-2")
for c,d in T.items():
    print(c, d['exp'][2], d['imp'][2], round(d['exp'][2]-d['imp'][2],1))
print("D Jan export share of 1-2, 2023 vs 2022")
cnt=0
for c,d in T.items():
    feb,fg,cum,cg = d['exp']
    s23 = (cum-feb)/cum
    cum22 = cum/(1+cg/100); feb22 = feb/(1+fg/100)
    s22 = (cum22-feb22)/cum22
    print(c, round(s23*100,2), round(s22*100,2), s23>s22, "jan growth", round(((cum-feb)/(cum22-feb22)-1)*100,2))
    cnt += s23>s22
print("count", cnt)
