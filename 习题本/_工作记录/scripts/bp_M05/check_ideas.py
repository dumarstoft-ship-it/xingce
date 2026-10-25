"""校验蓝图里给出的"建议数据"：答案是否干净、唯一，典型错误路径会落到哪个数（供出题人设计干扰项）。
注意：这只是规划阶段的数据检查，出题人仍需为每道改编题写独立验算脚本。"""
import math, itertools
from fractions import Fraction as F

def show(tag, **kw):
    print(f'[{tag}]', ', '.join(f'{k}={v}' for k, v in kw.items()))

# ======================= Day 4 =======================
# G1-V1 同价一盈一亏 20%，共亏 25 元，求售价
P = [p for p in range(1, 2000) if abs(2 * p - (p / 1.2 + p / 0.8) + 25) < 1e-9]
show('D4-G1-V1', P=P, err_2Pr2=25 / (2 * 0.04), costs=(P[0] / 1.2, P[0] / 0.8))
# G1-V2 利润率口径：成本120，甲按成本加价25%，乙利润占售价25%
a = 120 * 1.25; b = 120 / (1 - .25)
show('D4-G1-V2', jia=a, yi=b, diff=b - a, err_same=0, err_mix=120 + .25 * 150 - 150)
# G1-V3 转手链：甲盈20%卖给乙，乙亏10%卖给丙，丙付540
yi_cost = 540 / 0.9; jia_cost = yi_cost / 1.2
show('D4-G1-V3', jia_cost=jia_cost, jia_profit=yi_cost - jia_cost, yi_loss=540 - yi_cost,
     total=(yi_cost - jia_cost) + (540 - yi_cost), err_10pct=0.1 * jia_cost, err_loss_on_price=(yi_cost - jia_cost) - 0.1 * 540)
# G2-V1 会员价低于市场价20%，新客再优惠10%，支付3600
m = 3600 / (0.8 * 0.9)
show('D4-G2-V1', market=m, saved=m - 3600, err_30pct_of_paid=3600 * .3, err_add=m * .3, err_70=3600 / .7 - 3600)
# G2-V2 封顶补贴比较
def sub(final, rate, cap): return min(final * rate, cap)
A = 12500 * .88; B = 13000 * .8
payA = A - sub(A, .2, 2000); payB = B - sub(B, .15, 1500)
show('D4-G2-V2', A_final=A, B_final=B, payA=payA, payB=payB, diff=payA - payB,
     nocap=(A * .8, B * .85), capA_only=(payA, B * .85))
# G2-V3 先折后减 vs 先减后折 临界标价
crit = [p for p in range(1, 1000) if 0.8 * p - 30 < 0.9 * (p - 50)]
show('D4-G2-V3', threshold_min_p=min(crit), err_forget_09=[p for p in range(1, 1000) if .8 * p - 30 < .9 * p - 50][0])
# G2-V4 数码补贴：售价<=6000补15%最高500，超6000不补；实付<=5600的最高售价
def pay_phone(p): return p - (min(.15 * p, 500) if p <= 6000 else 0)
mx = max(p for p in range(1, 10000) if pay_phone(p) <= 5600)
show('D4-G2-V4', max_price=mx, pay_at=pay_phone(mx), naive=5600 + 500, naive2=round(5600 / .85, 1), pay6000_vs_6100=(pay_phone(6000), pay_phone(6100)))
# G3-V1 防暑药包：A比B贵4元，B是A的80%；全买A x份，全买B x+15份；各买相同份数最多几份
a = 4 / (1 - .8); b = .8 * a
xs = [x for x in range(1, 1000) if a * x == b * (x + 15)]
budget = a * xs[0]
show('D4-G3-V1', A=a, B=b, x=xs, budget=budget, each=math.floor(budget / (a + b)), raw=budget / (a + b))
# G4-V1 利润率26%->40%，售价不变，进价降幅
c = 126 / 1.4
show('D4-G4-V1', new_cost=c, drop=1 - c / 100, err_pp=.14, err_base=(1.4 - 1.26) / 1.26)
# G4-V2 售价是进价1.5倍，进价涨20%，利润不低于上月90%，销量至少
show('D4-G4-V2', q=0.9 * 5 / (15 - 12), err_no90=5 / 3)
# G4-V3 进价降8%，售价不变，利润率提高10个百分点
for r in [F(k, 1000) for k in range(1, 1000)]:
    P = 100 * (1 + r)
    if (P - 92) / 92 == r + F(1, 10): show('D4-G4-V3', r=float(r))
# G4-V4 富硒稻：亩产-10%，单价+50%，成本+20%；原利润=成本50%
old_rev, old_cost = 150, 100
new_rev = old_rev * .9 * 1.5; new_cost = old_cost * 1.2
show('D4-G4-V4', inc=(new_rev - new_cost) / (old_rev - old_cost) - 1, rev_growth=new_rev / old_rev - 1,
     no_cost=(new_rev - old_cost) / 50 - 1, no_yield=(old_rev * 1.5 - new_cost) / 50 - 1)
# G5-V1 收入+20% 支出+12% 利润+50%，去年利润800
for R in range(801, 20000):
    E = R - 800
    if abs(1.2 * R - 1.12 * E - 1200) < 1e-9: show('D4-G5-V1', R=R, E=E, R_now=1.2 * R, E_now=1.12 * E)
# G5-V2 原材料60% +20%，加工40% -25%，出厂价不变，单件利润降10%
newc = 60 * 1.2 + 40 * .75
profit = (newc - 100) / .1
show('D4-G5-V2', new_cost=newc, profit=profit, rate=profit / 100)
# G6-V1 150盆，360元，50%利润定价，剩余打八折，总利润为期望的88%
c = 360 / 150; pr = c * 1.5
k = [n for n in range(0, 151) if abs(n * (pr - c) + (150 - n) * (pr * .8 - c) - .88 * 150 * (pr - c)) < 1e-9]
show('D4-G6-V1', full_price_sold=k, share=[x / 150 for x in k])
# G6-V2 团购价至少（零售量降1/3，团购量=零售量2倍）
base = (50 - 30) * 600; retail = 400
g = [x for x in range(30, 60) if retail * 20 + 2 * retail * (x - 30) >= base][0]
show('D4-G6-V2', group_price_min=g)
# G6-V3 进价6 定价10，60%按定价，剩余打折，总利润率不低于30%
d = [x / 100 for x in range(0, 101) if 0.6 * 10 + 0.4 * 10 * x / 100 >= 1.3 * 6 - 1e-9][0]
show('D4-G6-V3', min_discount=d, err_ignore_first=7.8 / 10)
# G7-V1 进价40 定价50 日销300，每涨1元少10个：最大日利润
best = max(range(0, 31), key=lambda x: (10 + x) * (300 - 10 * x))
show('D4-G7-V1', x=best, price=50 + best, maxprofit=(10 + best) * (300 - 10 * best), now=10 * 300)
# G7-V2 进价60 售价100 日销80，每降2元多卖15件，降价须为2元整数倍
vals = {n: (40 - 2 * n) * (80 + 15 * n) for n in range(0, 21)}
nb = max(vals, key=vals.get)
show('D4-G7-V2', n=nb, price=100 - 2 * nb, profit=vals[nb], neighbors=(vals[nb - 1], vals[nb + 1]), vertex_cut=(40 - 32 / 3) / 2 * 1)
# G7-V3 民宿：40间 200元满房，每涨20元少2间，入住房每间成本40
vals = {x: (200 + 20 * x - 40) * (40 - 2 * x) for x in range(0, 21)}
xb = max(vals, key=vals.get)
vals2 = {x: (200 + 20 * x) * (40 - 2 * x) for x in range(0, 21)}
show('D4-G7-V3', price=200 + 20 * xb, profit=vals[xb], trap_no_cost=200 + 20 * max(vals2, key=vals2.get))
# G8-V1 停车：首15分钟免费，15~60分钟6元，超1小时后每30分钟3元（不足按30）
def park(mn):
    if mn <= 15: return 0
    if mn <= 60: return 6
    return 6 + 3 * math.ceil((mn - 60) / 30)
feeA = park(160)
cands = [mn for mn in range(0, 600) if park(mn) == feeA + 6]
show('D4-G8-V1', feeA=feeA, B_pay=feeA + 6, B_range=(min(cands), max(cands)), opt_check={t: park(t) for t in (210, 220, 240, 250)})
# G8-V2 阶梯电价：<=200 0.6；200~400 0.65；>400 0.9；7月u，8月u+120，合计453
def elec(u):
    if u <= 200: return .6 * u
    if u <= 400: return 120 + .65 * (u - 200)
    return 250 + .9 * (u - 400)
us = [u for u in range(0, 1000) if abs(elec(u) + elec(u + 120) - 453) < 1e-9]
show('D4-G8-V2', july=us, aug=[u + 120 for u in us], fees=[(elec(u), elec(u + 120)) for u in us])
# G8-V3 网约车：起步10含3km，2元/km，0.5元/分钟；高速30km@60km/h+10元路费；市区24km@36km/h
def ride(km, v, toll=0): return 10 + 2 * max(0, km - 3) + 0.5 * km / v * 60 + toll
hs, cs = ride(30, 60, 10), ride(24, 36)
show('D4-G8-V3', highway=hs, city=cs, diff=hs - cs, no_time=(10 + 54 + 10) - (10 + 42), no_toll=hs - 10 - cs)
# G9-V1 会员年费120，9.5折
show('D4-G9-V1', breakeven=120 / .05, err_after=120 / .05 * .95, err_div=120 / .05 / .95)
# G9-V2 固定6万 变动30 售价50 目标利润4万；售价降为46
q1 = (60000 + 40000) / 20; q2 = math.ceil((60000 + 40000) / 16)
show('D4-G9-V2', q1=q1, q2=q2, inc=q2 / q1 - 1)
# G10-V1 菜商：进100斤，进价5 售价10，剩余2元处理；10天6天卖完，4天每天剩r，共赚4520
r = [x for x in range(0, 101) if 6 * 500 + 4 * ((100 - x) * 10 + 2 * x - 500) == 4520]
r2 = [x for x in range(0, 101) if 6 * 500 + 4 * ((100 - x) * 10 - 500) == 4520]
show('D4-G10-V1', r=r, trap_no_salvage=r2)
# G10-V2 荔枝：200斤 进价12 损耗10% 利润率35%
show('D4-G10-V2', price=12 * 200 * 1.35 / 180, e1=12 * 1.35, e2=12 * 1.35 * 1.1, e3=12 * 1.45)

# ======================= Day 18 =======================
# G1-V1 两店：甲 >60 立减15再九折；乙 >60 八五折再减5；三件55/120/200
def j(p): return (p - 15) * .9 if p > 60 else p
def y(p): return p * .85 - 5 if p > 60 else p
items = [55, 120, 200]
best = sum(min(j(p), y(p)) for p in items)
show('D18-G1-V1', best=best, all_jia=sum(j(p) for p in items), all_yi=sum(y(p) for p in items),
     crit=[p for p in range(61, 1000) if y(p) < j(p)][0])
# G1-V2 两件封顶补贴分类讨论（只核对两种情形都成立的现象）
sols = []
for A10 in range(1000, 15000, 50):
    W = 15000 - A10
    if abs(min(.2 * A10, 2000) + min(.15 * W, 2000) - 2600) < 1e-9: sols.append((A10, W))
show('D18-G1-V2', solutions_total15000_sub2600=sols)
# G1-V3 地铁月累计：前15次原价，第16次起6折；每月40次每次6元
tot = 15 * 6 + 25 * 6 * .6
show('D18-G1-V3', total=tot, rate=tot / 240)
# G2-V1 预算300万：A x辆剩20；B单价为A的80%，x+2辆剩12
s = [(a, x) for x in range(1, 50) for a in [F(280, x)] if F(8, 10) * a * (x + 2) == 288]
show('D18-G2-V1', A_x=[(float(a), x) for a, x in s], B=[float(F(8, 10) * a) for a, x in s])
# G2-V2 全买A 60件或B 90件，先买30件A，剩余最多买几件B
show('D18-G2-V2', B=(180 - 30 * 3) / 2)
# G3-V1 工作日3折、周末6折；客流工作日×3、周末×1.5；周末日均=4×工作日
before = 5 * 1 * 10 + 2 * 4 * 10; after = 5 * 3 * 3 + 2 * 6 * 6
show('D18-G3-V1', ratio=after / before)
# G3-V2 产量+25% 售价+20% 利润翻倍，原利润占收入25%，成本增幅
show('D18-G3-V2', cost_inc=(150 - 50) / 75 - 1)
# G3-V3 连续调价
show('D18-G3-V3', profit_ratio=(1.2 * .9 - .6) * 1.05 / .4, revenue_ratio=1.2 * .9 * 1.05)
# G4-V1 日产-20% 原材料-25% 日利润+20% 出厂价=4×单件利润
for pi in [F(k, 10) for k in range(1, 200)]:
    for m_ in [F(k, 10) for k in range(1, 400)]:
        o_ = 3 * pi - m_
        if o_ > 0 and F(8, 10) * (pi + F(1, 4) * m_) == F(12, 10) * pi:
            show('D18-G4-V1', ratio_m_over_o=float(m_ / o_)); break
    else: continue
    break
# G4-V2 十字交叉：A利润率25% B10% 合计16%，A成本比B少600
for cb in range(601, 10000):
    ca = cb - 600
    if abs((.25 * ca + .10 * cb) / (ca + cb) - .16) < 1e-12: show('D18-G4-V2', ca=ca, cb=cb, profit=.25 * ca + .1 * cb)
# G4-V3 能耗8元降40%，日产2000->2500，改造72万
show('D18-G4-V3', days=720000 / (8 * .4 * 2500))
# G5-V1 九折卖3件=定价卖2件；降45元卖4件=定价卖1件
for x in range(1, 2000):
    yv = .7 * x
    if abs(4 * (x - 45 - yv) - (x - yv)) < 1e-9: show('D18-G5-V1', price=x, cost=yv)
# G5-V2 三段 5:3:2，进价80，定价120，八折96，清仓56
show('D18-G5-V2', rate=(5 * 40 + 3 * 16 + 2 * (56 - 80)) / 800)
# G6-V1 进价20 售价30 日销200 每涨1元少10，利润不低于2160，售价最高
ok = [p for p in range(20, 51) if (p - 20) * (200 - 10 * (p - 30)) >= 2160]
show('D18-G6-V1', range=(min(ok), max(ok)))
# G6-V2 每降1元多卖10件，且每多卖10件进价降0.5
v = {x: (10 - .5 * x) * (100 + 10 * x) for x in range(0, 21)}
xb = max(v, key=v.get); v2 = {x: (10 - x) * (100 + 10 * x) for x in range(0, 11)}
show('D18-G6-V2', cut=xb, price=30 - xb, profit=v[xb], trap_no_cost_change=max(v2, key=v2.get))
# G6-V3 门票80 日客2000，每降5元增200人，人均二次消费利润20
v = {x: (80 - 5 * x + 20) * (2000 + 200 * x) for x in range(0, 17)}
v2 = {x: (80 - 5 * x) * (2000 + 200 * x) for x in range(0, 17)}
show('D18-G6-V3', price=80 - 5 * max(v, key=v.get), trap=80 - 5 * max(v2, key=v2.get))
# G7-V1 出租车（2020HB-66规则）11.5公里车费
def taxi(km):
    k = math.ceil(km); fee = 8
    for i in range(3, k + 1): fee += 2 if i <= 5 else (3 if i <= 8 else 4)
    return fee
show('D18-G7-V1', fare=taxi(11.5), no_round=8 + 6 + 9 + 4 * 3.5)
# G7-V2 个税 3%/10%/20%，缴税1590
def tax(x):
    t = 0
    for lo, hi, r in [(0, 3000, .03), (3000, 12000, .10), (12000, 25000, .20), (25000, 35000, .25)]:
        if x > lo: t += (min(x, hi) - lo) * r
    return t
inc = [x for x in range(0, 40000) if abs(tax(x) - 1590) < 1e-9]
show('D18-G7-V2', income=inc, e1=1590 / .2, e2=1590 / .1)
# G7-V3 快递首重1kg12元，续重每0.5kg3元
def exp(w): return 12 + 3 * max(0, math.ceil(round((w - 1) / .5, 9)))
ws = [.8, 1.3, 2.2]
show('D18-G7-V3', separate=sum(exp(w) for w in ws), merged=exp(sum(ws)))
# G8-V1 满额折扣反推：寻找两笔实付各有2个整数原价候选的数据（300/9折，500/8折，800/7折）
def payf(o): return o * (.7 if o >= 800 else .8 if o >= 500 else .9 if o >= 300 else 1)
def origs(p):
    out = []
    for d in (1, .9, .8, .7):
        o = p / d
        if abs(o - round(o)) < 1e-9 and abs(payf(round(o)) - p) < 1e-9: out.append(round(o))
    return out
found = []
for p1 in range(250, 300):
    for p2 in range(400, 560, 2):
        o1, o2 = origs(p1), origs(p2)
        if len(o1) == 2 and len(o2) == 2:
            saves = sorted({p1 + p2 - payf(a + b) for a in o1 for b in o2})
            if all(abs(s - round(s)) < 1e-9 for s in saves) and len(saves) >= 3:
                found.append((p1, p2, o1, o2, saves))
show('D18-G8-V1', examples=found[:6], count=len(found))
# G8-V2 每满100减20可叠加，满减前满199包邮，运费8；85+66+47，可加购5元小商品
def order(total):
    return total - 20 * (total // 100) + (0 if total >= 199 else 8)
show('D18-G8-V2', no_add=order(198), add5=order(203), save=order(198) - order(203))
# G10-V1 等额本金：48万，120期，月利率0.25%
show('D18-G10-V1', m61=4000 + (480000 - 60 * 4000) * .0025, total_interest=sum((480000 - k * 4000) * .0025 for k in range(120)))
# G10-V2 寻找干净数据：定价10，成本c，打九折；打折前日销s0共D天；打折后第i天销 s0+k*i；n天总利润=打折前D天
cands = []
for c in [6, 7, 7.5, 8]:
    for s0 in (40, 50, 60, 80, 100):
        for k in (5, 10, 20):
            for Dd in (10, 15, 20, 30):
                lhs_unit = 9 - c; rhs = (10 - c) * s0 * Dd
                if lhs_unit <= 0: continue
                for n in range(2, 40):
                    tot = sum(s0 + k * i for i in range(1, n + 1))
                    if abs(lhs_unit * tot - rhs) < 1e-9: cands.append((c, s0, k, Dd, n))
show('D18-G10-V2', clean=cands[:10])
# G11-V1 三套餐：A 0.2/分；B 月租30含200分超0.15；C 月租60含500分超0.1
def A_(t): return .2 * t
def B_(t): return 30 + .15 * max(0, t - 200)
def C_(t): return 60 + .1 * max(0, t - 500)
bbest = [t for t in range(0, 1000) if B_(t) < A_(t) - 1e-9 and B_(t) < C_(t) - 1e-9]
show('D18-G11-V1', B_best_range=(min(bbest), max(bbest)))
# G11-V2 新能源比燃油贵3万，每公里0.1 vs 0.6，维护每年少500，年行1.5万公里
show('D18-G11-V2', years=30000 / (.5 * 15000 + 500))
# G12-V1 报童：成本4 售价10 处理价2；需求 100×4天 120×8天 140×6天 160×2天
dem = [100] * 4 + [120] * 8 + [140] * 6 + [160] * 2
def tot(q): return sum(10 * min(q, d) + 2 * max(0, q - d) - 4 * q for d in dem)
show('D18-G12-V1', **{f'q{q}': tot(q) for q in (100, 120, 140, 160)})

# ======================= Day 32 =======================
# G1-V1 海外 -m, +m, +3m；国内不变；2025总利润比2024多40%
for Dm in [F(k, 10) for k in range(0, 500)]:
    if Dm + 3 == F(14, 10) * (Dm + 1): show('D32-G1-V1', D=float(Dm), r2023_over_2025=(Dm - 1) / (Dm + 3))
# G1-V2 国补15%最高2000；市补=国补后价格10%最高800；实付6120
def pay2(P):
    a = P - min(.15 * P, 2000); return a - min(.1 * a, 800)
Ps = [P for P in range(1000, 30000) if abs(pay2(P) - 6120) < 1e-9]
show('D32-G1-V2', P=Ps, e_add=6120 / .75, e1=6120 / .85, e2=6120 / .9)
# G3-V1 进价降10% 售价降5% 利润率提高6个百分点
for P in [F(k, 10) for k in range(1000, 3000)]:
    if F(95, 100) * P / 90 - 1 == P / 100 - 1 + F(6, 100): show('D32-G3-V1', r=float(P / 100 - 1))
# G3-V2 门票100->60 客流+80% 人均二次消费利润20
show('D32-G3-V2', ratio=1.8 * (60 + 20) / (100 + 20), trap=1.8 * 60 / 100)
# G4-V2 2023SD-44 结构 + 每天维护1.6万
show('D32-G4-V2', days=3456 / (9.6 - 1.6))
# G4-V3 成本56 物流12 佣金=售价15% 利润率25%（以成本+物流为基数）
show('D32-G4-V3', price=(68 * 1.25) / .85, e1=68 * 1.25, e2=68 * 1.25 * 1.15)
# G6-V1 第n天降价n元、销量100+10n，原价50成本30
v = {n: (20 - n) * (100 + 10 * n) for n in range(1, 20)}
show('D32-G6-V1', best_day=max(v, key=v.get), profit=max(v.values()))
# G6-V2 EOQ：年需求3600，每次订货费200，每件年存储费4（平均库存x/2）
v = {x: 200 * 3600 / x + 4 * x / 2 for x in range(1, 3601) if 3600 % x == 0}
show('D32-G6-V2', best_x=min(v, key=v.get), cost=min(v.values()))
# G6-V3 充电服务费p，日电量4000-2000p，运维0.2/度，补贴0.4/度
v = {p / 100: (p / 100 + .4 - .2) * (4000 - 2000 * p / 100) for p in range(0, 201)}
v2 = {p / 100: (p / 100 - .2) * (4000 - 2000 * p / 100) for p in range(0, 201)}
show('D32-G6-V3', p=max(v, key=v.get), p_nosub=max(v2, key=v2.get))
# G7-V2 水价：甲20吨76元，乙28吨116元，第一档3元
for a_ in range(1, 20):
    p_ = F(76 - 3 * a_, 20 - a_)
    if 3 * a_ + p_ * (28 - a_) == 116: show('D32-G7-V2', a=a_, p=float(p_), bing=[x for x in range(0, 60) if 3 * min(x, a_) + p_ * max(0, x - a_) == 51])
# G8-V2 五件商品分单 + 两张券（满200减40、满300减70，每单限一张，每种各一张）
items = [150, 120, 90, 80, 60]
best = None
for assign in itertools.product(range(3), repeat=5):   # 最多分3单
    orders = [sum(it for it, g in zip(items, assign) if g == k) for k in range(3)]
    orders = [o for o in orders if o > 0]
    # 券分配：每张券最多用一次，每单最多一张
    bestoff = 0
    for perm in itertools.permutations(range(len(orders)), min(2, len(orders))):
        off = 0
        coupons = [(300, 70), (200, 40)]
        for (th, dv), oi in zip(coupons, perm):
            if orders[oi] >= th: off += dv
        bestoff = max(bestoff, off)
    pay = sum(orders) - bestoff
    if best is None or pay < best[0]: best = (pay, sorted(orders))
show('D32-G8-V2', best=best, single=500 - 70)
# G8-V3 消费券满100减30（政府20、商户10），核销1200张，标价15万
show('D32-G8-V3', share=(150000 - 36000 + 24000) / 150000)
# G10-V1 2022SC1-48 结构：年均利润最大
avg = {n: (9100 * n - 16200 - sum(1100 + 400 * (k - 1) for k in range(1, n + 1))) / n for n in range(1, 30)}
show('D32-G10-V1', best_year=max(avg, key=avg.get), avg=round(max(avg.values()), 2))
# G10-V3 120万 年利率4% 5年 等额本金(年) vs 先息后本
show('D32-G10-V3', ep=sum((120 - 24 * k) * .04 for k in range(5)), interest_only=120 * .04 * 5)
# G11-V1 两平台收益相同时播放量（万次）
show('D32-G11-V1', x=100000 / (0.01 - 0.006) / 10000)
# G11-V3 家充3000元，0.6 vs 1.5元/度，每百公里15度，月行1500公里
show('D32-G11-V3', months=3000 / (1500 / 100 * 15 * .9))
# G12-V1 荔枝两天每天损耗10%，进价8.1，利润率20%
show('D32-G12-V1', price=8.1 * 1.2 / .81)
# G13-V1 工程+利润
show('D32-G13-V1', days=1 / (1 / 10 + 1 / 15), profit=50 - 6 * (2 + 1.5))
# G13-V2 抽奖期望返现
show('D32-G13-V2', ret=100 * .05 + 40 * .2 + 10 * .5, zhe=1 - (100 * .05 + 40 * .2 + 10 * .5) / 200)

# ======================= 追加检查 =======================
# D18-G9-V1 三种商品库存200/300/500，单价60/40/50；先按原价卖总量40%，其余八折；最高与最低之差
stock = {'A': (60, 200), 'B': (40, 300), 'C': (50, 500)}
def sales(order):
    left = 400; tot = 0
    for k in order:
        p, n = stock[k]; t = min(n, left); tot += p * t + p * .8 * (n - t); left -= t
    return tot
vals = {o: sales(o) for o in itertools.permutations('ABC')}
show('D18-G9-V1', max=max(vals.values()), min=min(vals.values()), diff=max(vals.values()) - min(vals.values()))
# D18-G9-V2 A单价10买3送2；B单价15买2送1；需要A 9件、B 7件，最少花费（允许多拿）
def mincost(need, price, buy, free):
    best = None
    for g in range(0, need + 1):
        for s in range(0, need + 1):
            got = g * (buy + free) + s
            if got >= need:
                c = g * buy * price + s * price
                best = c if best is None else min(best, c)
    return best
show('D18-G9-V2', A=mincost(9, 10, 3, 2), B=mincost(7, 15, 2, 1), total=mincost(9, 10, 3, 2) + mincost(7, 15, 2, 1),
     A_no_extra=30 + 40)
# D32-G9-V1 单支1.7，3支装5元，10支装15元；最低总价=1.7x-4.1 的 x
def minprice(x):
    best = [0.0] + [1e9] * x
    for i in range(1, x + 1):
        best[i] = best[i - 1] + 1.7
        if i >= 3: best[i] = min(best[i], best[i - 3] + 5)
        if i >= 10: best[i] = min(best[i], best[i - 10] + 15)
    return best[x]
xs = [x for x in range(1, 300) if abs(minprice(x) - (1.7 * x - 4.1)) < 1e-6]
show('D32-G9-V1', xs=xs)
# D32-G9-V2 单价10；满30件9折、满60件8折、满100件7折；三社区需要25/28/45（允许多买凑档）
def best_buy(need):
    def c(q): return q * 10 * (.7 if q >= 100 else .8 if q >= 60 else .9 if q >= 30 else 1)
    return min(c(q) for q in range(need, 200))
sep = sum(best_buy(n) for n in (25, 28, 45)); comb = best_buy(98)
show('D32-G9-V2', sep=sep, comb=comb, save=sep - comb, comb_exact=98 * 10 * .8, sep_exact=250 + 280 * .9 * 0 + 280 + 45 * 10 * .9)
# D32-G11-V2 固定20万，前5000件变动30，超过部分26，售价50，月利润至少14万
def prof(q): return 50 * q - 200000 - (30 * min(q, 5000) + 26 * max(0, q - 5000))
qmin = next(q for q in range(0, 100000) if prof(q) >= 140000)
show('D32-G11-V2', qmin=qmin, trap20=(200000 + 140000) / 20, trap24=(200000 + 140000) / 24)
# D32-G7-V3 年度汇算：应纳税所得额=收入-6万-专项附加3.6万；3%(<=3.6万)/10%(3.6~14.4万)/20%(14.4~30万)；税8280
def tax_y(T):
    t = 0
    for lo, hi, r in [(0, 36000, .03), (36000, 144000, .10), (144000, 300000, .20)]:
        if T > lo: t += (min(T, hi) - lo) * r
    return t
Ts = [T for T in range(0, 300001, 100) if abs(tax_y(T) - 8280) < 1e-6]
show('D32-G7-V3', taxable=Ts, income=[T + 60000 + 36000 for T in Ts])
# D32-G8-V1 满30减5、满80减20两种券，核销12万张，商户获补贴=减免额60%，共108万
for y_ in range(0, 121):
    x_ = 120 - y_
    if 5 * x_ + 20 * y_ == 1800: show('D32-G8-V1', x_wan=x_ / 10, y_wan=y_ / 10, min_pay_wan=(x_ * 25 + y_ * 60) / 10)
# D18-G5-V3 套餐：A售价30、B售价10；1A+1B九折获利11；2A+3B八折获利17
a_, b_ = None, None
for a in range(1, 30):
    for b in range(1, 10):
        if (30 + 10) * .9 - (a + b) == 11 and (60 + 30) * .8 - (2 * a + 3 * b) == 17: a_, b_ = a, b
show('D18-G5-V3', a=a_, b=b_, rateA=(30 - a_) / a_, rateB=(10 - b_) / b_)
# D18-G10-V2 选用数据：定价10 成本7.5 九折；打折前日销60，共15天；打折后每天比前一天多10件
n_ = [n for n in range(1, 40) if 1.5 * sum(60 + 10 * i for i in range(1, n + 1)) == 2.5 * 60 * 15]
show('D18-G10-V2-pick', n=n_)

# ======================= 追加检查 2 =======================
# D4-G4-V3 误把"提高10个百分点"当"提高10%"
for r in [F(k, 10000) for k in range(1, 10000)]:
    if (100 * (1 + r) - 92) / 92 == r * F(11, 10): show('D4-G4-V3-err', r=float(r))
# D18-G1-V3 追问：平均折扣低于8折的最少次数
show('D18-G1-V3b', n=next(n for n in range(16, 200) if (15 + .6 * (n - 15)) / n < .8))
# D32-G3-V1 甲35 乙25 预算149；共5台，甲至少1台
x_, y_ = 35, 25
show('D32-G3-V1', over=3 * x_ + 2 * y_ - 149, left=149 - (2 * x_ + 3 * y_),
     schemes=[a for a in range(0, 6) if a * x_ + (5 - a) * y_ <= 149], with_min1=[a for a in range(1, 6) if a * x_ + (5 - a) * y_ <= 149])
# D32-G6-V2 进价80，加价25%，剩余七折，总利润率15%
for xs_ in [F(k, 1000) for k in range(0, 1001)]:
    if 20 * (1 - xs_) + (70 - 80) * xs_ == F(15, 100) * 80: show('D32-G6-V2', share=xs_)
# D32-G11-V1 5天，每天降原价10%，销量翻倍，第5天销量同第2天，成本为原价50%
pr_ = [1, .9, .8, .7, .6]; q_ = [1, 2, 4, 8, 2]
rev_ = sum(p * q for p, q in zip(pr_, q_)); cst_ = .5 * sum(q_)
show('D32-G11-V1', rev=rev_, cost=cst_, rate=(rev_ - cst_) / cst_)
# D32-G11-V2 购入12800，首年维护1000每年+400，年收益8000：年均利润最大
avg = {n: (8000 * n - 12800 - sum(1000 + 400 * (k - 1) for k in range(1, n + 1))) / n for n in range(1, 30)}
cum = {n: avg[n] * n for n in avg}
show('D32-G11-V2', best=max(avg, key=avg.get), avg=avg[max(avg, key=avg.get)], first_cum_over_20000=next(n for n in cum if cum[n] > 20000))
# D32-G8-V1 骑手：搜索干净数据（基础a整数；超过k单每单a+1.5；超过h单每单a-1；第一天未超h，第二天超h）
found = []
for a in range(4, 12):
    for k in range(5, 30):
        for h in range(k + 1, 45):
            for n1 in range(k + 1, h + 1):
                for n2 in range(h + 1, 50):
                    d1 = n1 * a + 1.5 * (n1 - k)
                    d2 = n2 * a + 1.5 * (h - k) - (n2 - h)
                    # 要求：由(n1,d1,n2,d2)反推(a,k,h)唯一
                    found.append((n1, d1, n2, d2, a, k, h))
from collections import defaultdict
idx = defaultdict(set)
for n1, d1, n2, d2, a, k, h in found: idx[(n1, d1, n2, d2)].add((a, k, h))
uniq = [(key, list(v)[0]) for key, v in idx.items() if len(v) == 1 and key[0] in (25, 28, 32) and key[2] in (36, 40, 42)
        and float(key[1]).is_integer() is False and (key[1] * 2).is_integer()]
show('D32-G8-V1', sample=uniq[:8], count=len(uniq))
