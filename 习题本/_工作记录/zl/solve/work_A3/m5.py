# MK2732X-M2 Shanghai trade 2023
tbl = {
 '欧盟':(3101.72,-1.0,5343.96,5.0),
 '美国':(2774.90,-11.8,2020.70,-2.5),
 '东盟':(2185.18,3.1,3267.43,-7.8),
 '日本':(1432.19,6.5,2481.48,-4.2),
 '中国香港':(1501.09,15.6,139.99,43.3),
 '中国台湾':(803.05,-8.8,1570.84,-16.2),
 '韩国':(774.90,16.5,1240.97,-18.5),
 '俄罗斯':(340.22,52.2,585.45,50.7),
}
# Q1
ex, eg, im, ig = tbl['东盟']
dex = ex*eg/(100+eg); dim = im*ig/(100+ig)
gap = im-ex
print("Q1: export inc =", dex, " import inc =", dim, " deficit2023 =", gap, " closing/yr =", dex-dim)
for n in range(1,6):
    print("   ", 2023+n, " exp-imp =", (ex+n*dex)-(im+n*dim))
# Q2
e22 = 17377.94/1.016; t22 = 42121.61/1.007; i22 = 24743.67/1.001
print("Q2: 2022 exp =", e22, " tot =", t22, " share =", e22/t22, " (check exp+imp=", e22+i22, "share2=", e22/(e22+i22), ") 2023 share =", 17377.94/42121.61)
# Q3
s23 = 63193.1-43383.5
s22 = (63193.1-2605.3)-(43383.5-258.7)
print("Q3: surplus23 =", s23, " surplus22 =", s22, " growth =", s23/s22-1, " (check total 2022:", (63193.1-2605.3)+(43383.5-258.7), "vs", 106576.6/1.028, ")")
# Q4
imp_g = {k:v[3] for k,v in tbl.items()}
exp_g = {k:v[1] for k,v in tbl.items()}
def pick(gd, absval):
    key = (lambda k: abs(gd[k])) if absval else (lambda k: gd[k])
    return max(gd, key=key), min(gd, key=key)
for label, gd, other in [('partner-view(Shanghai imports growth)', imp_g, 0), ('Shanghai-view(Shanghai exports growth)', exp_g, 2)]:
    for absval in (True, False):
        mx, mn = pick(gd, absval)
        val = tbl[mx][other] + tbl[mn][other]
        print("Q4:", label, "abs" if absval else "alg", mx, mn, "sum of", "SH exports" if other==0 else "SH imports", "=", round(val,2))
# Q5
T = 42121.61
tot = {k:v[0]+v[2] for k,v in tbl.items()}
s = {k: tot[k]/T for k in ['欧盟','美国','东盟']}
print("Q5:", {k: round(v*100,2) for k,v in s.items()}, " other =", round((1-sum(s.values()))*100,2))
print("    degrees:", {k: round(v*360,1) for k,v in s.items()})
