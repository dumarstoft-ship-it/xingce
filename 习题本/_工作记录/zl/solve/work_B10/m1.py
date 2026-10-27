# MK2713X-M1 上海金融市场
tot = {2018:1645.78, 2019:1934.31, 2020:2274.83, 2021:2511.07, 2022:2932.98}
print("check 2022 growth", tot[2022]/tot[2021]-1)
# Q1 上市证券数量同比增长
now, inc = 30110, 3121
base = now-inc
print("Q1 base", base, "growth", inc/base)
# Q2 2019-2022 年均
s = sum(tot[y] for y in range(2019,2023))
print("Q2 sum", s, "avg", s/4)
# Q3 原保险保费收入增速
p, rp = 663.05, 0.049
l, rl = 1431.96, 0.070
print("Q3 parts sum", p+l, "vs total 2095.01")
bp, bl = p/(1+rp), l/(1+rl)
print("Q3 base", bp, bl, bp+bl, "growth", 2095.01/(bp+bl)-1)
# 混合增速范围: 应在4.9%~7.0%之间，偏向人身险(权重大)
print("Q3 weight life(base)", bl/(bp+bl))
# Q4 保持2022年增量不变, 2021-2025累计
d = tot[2022]-tot[2021]
vals = [tot[2021], tot[2022]] + [tot[2022]+d*k for k in (1,2,3)]
print("Q4 inc", d, "vals", vals, "sum", sum(vals), "5*mid", 5*vals[2])
# Q5
incs = {y: tot[y]-tot[y-1] for y in range(2019,2023)}
print("Q5A incs", incs)
print("Q5B payout", 654.55, "1/3 premium", 2095.01/3, 654.55/2095.01)
g = tot[2022]/tot[2021]-1
y23 = tot[2022]*(1+0.168)
print("Q5C 2023 (16.8%)", y23, "2x2018", 2*tot[2018], "ratio", y23/tot[2018], " with exact g", tot[2022]*(1+g)/tot[2018])
st, rs = 96.26, 0.156
print("Q5D decrease", st/(1-rs)*rs, " trap *r/(1+r)", st*rs/(1+rs), " trap *r", st*rs)
