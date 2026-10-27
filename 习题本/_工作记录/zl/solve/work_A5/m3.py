# MK2736F-M1 中关村 2025年1-2月
zgc=13922.8; zgc_g=7.1; tech=3735.9
gx=5280.0; gx_g=5.8
ei_g=11.4; ei_pull=5.1
rd_people=55.4; rd_people_g=-1.9; rd_fee=611.9; rd_fee_g=2.5
inc = [8.9,7.2,7.0,7.3,4.9,4.9,4.4,4.0,3.7,3.6,7.1]
rd  = [3.7,4.3,2.8,3.4,3.0,3.0,2.6,2.2,1.9,2.0,2.5]
labels = ['24/1-2','1-3','1-4','1-5','1-6','1-7','1-8','1-9','1-10','1-11','25/1-2']
cur = gx/zgc; base = (gx/(1+gx_g/100))/(zgc/(1+zgc_g/100))
print("Q1 cur %.4f%% base %.4f%% diff %.4f pp" % (cur*100, base*100, (cur-base)*100))
print("   formula:", cur*(gx_g-zgc_g)/(100+gx_g)*100)
print("Q2 2024 EI share = pull/rate =", ei_pull/ei_g*100)
print("Q3 per-capita R&D fee growth =", ((1+rd_fee_g/100)/(1+rd_people_g/100)-1)*100)
print("Q4 cumulative R&D growth changes (Mar..Nov):")
cnt=0
for i in range(1,10):
    d = rd[i]-rd[i-1]
    flag = d>0
    cnt += flag
    print("   ", labels[i], rd[i-1], '->', rd[i], 'month>cum' if d>0 else ('equal' if d==0 else 'month<cum'))
print("   count =", cnt)
print("Q5 ③ 2023年1-2月 总收入 =", zgc/(1+zgc_g/100)/(1+inc[0]/100), " 2024年1-2月=", zgc/(1+zgc_g/100))
print("   tech share check", tech/zgc*100)
print("   2024 1-2 R&D fee", rd_fee/(1+rd_fee_g/100))
