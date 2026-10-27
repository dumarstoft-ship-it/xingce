# MK2711X-M3: 2023年2月福建部分地区外贸
d = {
 "厦门": {"合计":(696.4,23.5,1482.3,None),"出口":(268.4,-2.1,675.6,-6.9),"进口":(428.0,47.8,806.7,27.8)},
 "泉州": {"合计":(130.6,-16.5,385.2,-13.7),"出口":(84.5,-22.2,294.1,-14.3),"进口":(46.1,-3.6,91.1,-12.0)},
 "漳州": {"合计":(77.6,2.8,171.6,-7.0),"出口":(51.0,26.5,111.6,-4.9),"进口":(26.6,-24.5,60.0,-10.7)},
 "龙岩": {"合计":(35.4,-3.0,71.2,-26.4),"出口":(21.3,-7.6,40.7,-23.7),"进口":(14.1,4.9,30.5,-29.8)},
}
# Q1 import MoM change in Feb
for c in d:
    feb, _, cum, _ = d[c]["进口"]
    jan = cum - feb
    print("Q1 %s jan=%.1f feb=%.1f change=%.1f" % (c, jan, feb, feb-jan))
# Q2 Jan total > 1-2 monthly average
for c in d:
    feb, _, cum, _ = d[c]["合计"]
    jan = cum - feb
    print("Q2 %s jan=%.1f avg=%.2f jan>avg=%s" % (c, jan, cum/2, jan > cum/2))
# Q3 Xiamen 1-2 total growth
ex, exg = 675.6, -0.069
im, img = 806.7, 0.278
base = ex/(1+exg) + im/(1+img)
print("Q3 base=%.3f growth=%.4f%% (sum check %.1f)" % (base, (1482.3/base-1)*100, ex+im))
# Q4 Quanzhou Jan 2022 exports
cum22 = 294.1/(1-0.143); feb22 = 84.5/(1-0.222)
print("Q4 cum22=%.3f feb22=%.3f jan22=%.3f; jan23=%.1f" % (cum22, feb22, cum22-feb22, 294.1-84.5))
# Q5
jan_ex = 294.1-84.5; jan_tot = 385.2-130.6
print("Q5A share=%.4f%%" % (jan_ex/jan_tot*100))
jan_ly = 71.2-35.4
print("Q5B 龙岩 yoy=-3.0%%, mom=%.4f%%" % ((35.4/jan_ly-1)*100))
for c in d:
    print("Q5C %s ex=%.1f im=%.1f surplus=%.1f" % (c, d[c]["出口"][2], d[c]["进口"][2], d[c]["出口"][2]-d[c]["进口"][2]))
for c in d:
    feb, fg, cum, cg = d[c]["出口"]
    jan = cum-feb
    s_now = jan/cum
    s_last = (cum/(1+cg/100) - feb/(1+fg/100)) / (cum/(1+cg/100))
    print("Q5D %s jan share now=%.4f last=%.4f up=%s" % (c, s_now, s_last, s_now > s_last))
