# MK2732X-M2
ex_inc = 2185.18*0.031/1.031; im_inc = 3267.43*(-0.078)/(1-0.078)
gap = 3267.43-2185.18
print("Q1 东盟出口增量 =", ex_inc, " 进口增量 =", im_inc, " 2023逆差 =", gap, " 每年缩小 =", ex_inc-im_inc, " 年数 =", gap/(ex_inc-im_inc))
e, i = 2185.18, 3267.43
for y in range(2024, 2030):
    e += ex_inc; i += im_inc
    print("   ", y, "出口", round(e,2), "进口", round(i,2), "差(出-进)", round(e-i,2))
cur = 17377.94/42121.61
print("Q2 现期比重 =", cur*100, " 基期比重 =", cur*1.007/1.016*100)
print("   用数值: ", (17377.94/1.016)/(42121.61/1.007)*100, " 另法(出口/(出口+进口)):", (17377.94/1.016)/((17377.94/1.016)+(24743.67/1.001))*100)
s23 = 63193.1-43383.5; s22 = (63193.1-2605.3)-(43383.5-258.7)
print("Q3 顺差2023 =", s23, " 2022 =", s22, " 增速 =", (s23/s22-1)*100)
names = ["欧盟","美国","东盟","日本","中国香港","中国台湾","韩国","俄罗斯"]
ex = [3101.72,2774.90,2185.18,1432.19,1501.09,803.05,774.90,340.22]
exg = [-1.0,-11.8,3.1,6.5,15.6,-8.8,16.5,52.2]
imv = [5343.96,2020.70,3267.43,2481.48,139.99,1570.84,1240.97,585.45]
img = [5.0,-2.5,-7.8,-4.2,43.3,-16.2,-18.5,50.7]
# 对上海出口 = 上海进口
mx = max(range(8), key=lambda k: abs(img[k])); mn = min(range(8), key=lambda k: abs(img[k]))
print("Q4 (正确视角) 上海进口增速|max| =", names[mx], img[mx], " |min| =", names[mn], img[mn], " 其对上海进口=上海出口之和 =", ex[mx]+ex[mn])
mx2 = max(range(8), key=lambda k: abs(exg[k])); mn2 = min(range(8), key=lambda k: abs(exg[k]))
print("   (陷阱视角) 上海出口增速|max| =", names[mx2], " |min| =", names[mn2], " 上海进口之和 =", imv[mx2]+imv[mn2])
print("   B候选: 美国+俄罗斯 上海进口 =", imv[1]+imv[7], "  A候选: 俄罗斯+韩国 上海出口 =", ex[7]+ex[6])
tot = 42121.61
sh = {n: (ex[k]+imv[k])/tot*100 for k,n in enumerate(names)}
print("Q5 shares of total:", {k: round(v,2) for k,v in sh.items() if k in ("欧盟","美国","东盟")}, " 其他 =", round(100-sh["欧盟"]-sh["美国"]-sh["东盟"],2))
s8 = sum(ex)+sum(imv)
print("   trap (8地区合计为分母):", {n: round((ex[k]+imv[k])/s8*100,2) for k,n in enumerate(names) if n in ("欧盟","美国","东盟")}, " 8地区合计 =", s8)
