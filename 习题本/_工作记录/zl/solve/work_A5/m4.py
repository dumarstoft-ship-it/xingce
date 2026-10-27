# MK2728X-M1 通用机械 2024
asset=13178.62; asset_g=6.46; debt_g=6.21; ratio=53.56
rev=10739.39; rev_g=3.49; profit=843.79; profit_g=-0.36
exp_deliv=1722.70; exp_deliv_g=14.34
k_exp=102.90; k_exp_g=24.26
trade=499.25; trade_g=6.59; ex=355.24; ex_g=10.57
reg = {'东盟':(52.42,19.19),'美国':(52.39,3.92),'欧盟':(51.65,11.12),'俄罗斯':(22.25,6.39),'中亚':(8.92,28.70)}
debt24 = asset*ratio/100
print("Q1 2024 debt", debt24, " 2023 debt", debt24/(1+debt_g/100))
inc = k_exp*k_exp_g/(100+k_exp_g); base = exp_deliv/(1+exp_deliv_g/100)
print("Q2 200家出口交货值增量", inc, " 全国2023", base, " 拉动 %.4f pp" % (inc/base*100))
t23 = trade/(1+trade_g/100); e23 = ex/(1+ex_g/100)
print("Q3 2023 trade", t23, " exports", e23, " imports", t23-e23)
print("Q4 2023 exports by region:")
for k,(v,g) in sorted(reg.items(), key=lambda kv: kv[1][0]/(1+kv[1][1]/100)):
    print("   ", k, round(v/(1+g/100),3), " share %.3f%%" % (v/(1+g/100)/e23*100))
print("Q5 A: 全国工业利润增速", profit_g-2.94, " 机械工业利润增速", profit_g-7.64, " diff", (profit_g-2.94)-(profit_g-7.64))
print("   C: 2023进出口", t23)
m24 = profit/rev; m23 = (profit/(1+profit_g/100))/(rev/(1+rev_g/100))
print("   D: margin 2024 %.4f%%  2023 %.4f%%  diff %.4f pp" % (m24*100, m23*100, (m24-m23)*100))
print("      formula", m24*(profit_g-rev_g)/(100+profit_g)*100)
