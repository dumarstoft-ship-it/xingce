# MK2724X-M1  2023年末全国水上运输船舶构成
tot = dict(dwt=30052.07, dwt_g=0.9, pax=81.25, pax_g=-5.7, teu=304.24, teu_g=1.8, n_g=-2.9)
nh  = dict(n=10.66e4, n_g=-2.6, dwt=15433.11, dwt_g=1.2, pax=55.76, pax_g=-2.6, teu=62.40, teu_g=13.1)
yh  = dict(n=10672, n_g=-3.0, dwt=9792.75, dwt_g=4.5, pax=24.22, pax_g=-9.8, teu=68.83, teu_g=14.9)
yy  = dict(n=972, n_g=-29.9, dwt=4826.20, dwt_g=-6.4, pax=1.27, pax_g=-38.4, teu=173.01, teu_g=-5.8)

print("Q1")
cur = nh['pax']/tot['pax']
base = (nh['pax']/(1+nh['pax_g']/100))/(tot['pax']/(1+tot['pax_g']/100))
print(" cur share %.4f%%  base share %.4f%%  diff %.4f pp" % (cur*100, base*100, (cur-base)*100))
print(" formula A/B*(a-b)/(1+a):", cur*(nh['pax_g']-tot['pax_g'])/(100+nh['pax_g'])*100)

print("Q2")
for name,d in [('内河',nh),('沿海',yh),('远洋',yy)]:
    inc = d['teu']*d['teu_g']/(100+d['teu_g'])
    print(" ", name, "TEU change %.4f" % inc)

print("Q3")
print(" avg dwt growth inland: %.4f%%" % (((1+nh['dwt_g']/100)/(1+nh['n_g']/100)-1)*100))

print("Q4")
a_yy = yy['pax']*1e4/yy['n']; a_yh = yh['pax']*1e4/yh['n']
print(" 远洋 avg %.4f  沿海 avg %.4f  ratio %.4f" % (a_yy, a_yh, a_yy/a_yh), " 3/5=0.6 4/5=0.8")

print("Q5")
inc_yh = yh['teu']*yh['teu_g']/(100+yh['teu_g'])
base_tot = tot['teu']/(1+tot['teu_g']/100)
print(" A: 沿海TEU增量 %.4f  全国上年末 %.4f  拉动 %.4f%%" % (inc_yh, base_tot, inc_yh/base_tot*100))
for name,d in [('内河',nh),('沿海',yh),('远洋',yy)]:
    print(" B:", name, "avg pax growth %.4f%%" % (((1+d['pax_g']/100)/(1+d['n_g']/100)-1)*100))
print(" C: total ships =", nh['n']+yh['n']+yy['n'], " trap 10.66+10672+972 =", 10.66+10672+972)
print(" D: 远洋 dwt share %.4f%%" % (yy['dwt']/tot['dwt']*100))
print(" check sum dwt", nh['dwt']+yh['dwt']+yy['dwt'], "pax", nh['pax']+yh['pax']+yy['pax'], "teu", nh['teu']+yh['teu']+yy['teu'])
