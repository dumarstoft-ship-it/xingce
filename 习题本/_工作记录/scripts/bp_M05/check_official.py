"""M05 真题官方答案复核：逐题从题面独立求解，与官方答案比对（只做核查，不改题库）。"""
import math, itertools, json
from fractions import Fraction as F

S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
official = {q['id']: q['answer_official'] for q in json.load(open(S + '/tasks_in/M05.json'))['real']}
res = {}

def pick(opts, val, tol=1e-9):
    hits = [k for k, v in opts.items() if (abs(v - val) < tol if not callable(v) else v(val))]
    return hits[0] if len(hits) == 1 else ('AMBIG' + ''.join(hits) if hits else 'NONE')

# 2020HB-65
rev = 10 * (100 * 4 + 80 * 2 + 90 * 1); cost = 5 * 100 * 7
res['2020HB-65'] = pick({'A': 2950, 'B': 3000, 'C': 3250, 'D': 3500}, rev - cost)
# 2020JSA-52  团购量至少
base = (99 - 39) * 800; need = math.ceil((base - (99 - 39) * 400) / (59 - 39))
res['2020JSA-52'] = pick({'A': 800, 'B': 1000, 'C': 1200, 'D': 1500}, need)
# 2020JSA-63  降价 x 元利润最大（整数枚举）
best = max(range(0, 21), key=lambda x: (20 - x) * (120 + 20 * x))
res['2020JSA-63'] = pick({'A': 5, 'B': 6, 'C': 7, 'D': 8}, best)
# 2020SC1206-43 高价优先
items = sorted([(300, 300), (500, 300), (400, 400)], key=lambda t: -t[0])  # (单价, 件数)
left = 500; total = 0
for p, n in items:
    k = min(n, left); total += p * k + p * (n - k) * 0.5; left -= k
res['2020SC1206-43'] = pick({'A': 28.5, 'B': 30, 'C': 31.5, 'D': 33}, total / 10000)
# 2020SD-38
x = F(5000 - 400 * F(3, 2), 1000)       # 量贩店单件利润
res['2020SD-38'] = pick({'A': 7.2, 'B': 7.6, 'C': 8.0, 'D': 8.4}, float(12 - x))
# 2021ZJA-64
p = F(10) / (F(124, 100) - F(80, 100) * F(130, 100))   # 花生油进价
res['2021ZJA-64'] = pick({'A': 10, 'B': 15, 'C': 24, 'D': 25}, float(p * F(20, 100)))
# 2022GD-38
res['2022GD-38'] = pick({'A': 75, 'B': 85, 'C': 95, 'D': 105}, (48.5 + 25) / 0.7)
# 2022GK-67
xx = 660 / (1.65 * 6 - 1.5 * 5)
res['2022GK-67'] = pick({'A': 2200, 'B': 1980, 'C': 1650, 'D': 1375}, 6 * xx)
# 2022SD-43
for x in range(7, 200):
    if 25 * (x + 8) == 60 * (x - 6):
        fund = 25 * (x + 8); price_b = fund / x
res['2022SD-43'] = pick({'A': 600, 'B': 660, 'C': 700, 'D': 840}, (price_b - 5) * 40 - fund)
# 2022ZJA-61 提价销售
best = max(range(0, 31), key=lambda x: (4 + x) * (300 - 10 * x))
res['2022ZJA-61'] = pick({'A': 51, 'B': 52, 'C': 54, 'D': 57}, 44 + best)
# 2023HB-71
res['2023HB-71'] = pick({'A': .4, 'B': .3, 'C': .6, 'D': .5}, (120 - 80) / 80)
# 2023HB-74 停车费
def park(minutes):
    if minutes <= 15: return 0
    if minutes <= 60: return 5
    return 5 + 4 * math.ceil((minutes - 60) / 30)
res['2023HB-74'] = pick({'A': 120, 'B': 135, 'C': 165, 'D': 180}, 17, tol=0) if False else \
    [k for k, mnt in {'A': 120, 'B': 135, 'C': 165, 'D': 180}.items() if park(mnt) == 17]
res['2023HB-74'] = res['2023HB-74'][0] if len(res['2023HB-74']) == 1 else 'AMBIG'
# 2023SD-41 等额本金第二个月
pr = 600000 / 240; pay2 = pr + (600000 - pr) * 0.041 / 12
res['2023SD-41'] = pick({'A': 4550.0, 'B': 4541.5, 'C': 5137.0, 'D': 5290.5}, round(pay2, 1))
# 2023ZJA-58
q = (4 * 1.8) / (14 - 8)
res['2023ZJA-58'] = pick({'A': 1.3, 'B': 1.25, 'C': 1.2, 'D': 1.15}, q)
# 2024GD-37
res['2024GD-37'] = pick({'A': 400, 'B': 600, 'C': 800, 'D': 1000}, 4000 / 0.8 - 4000)
# 2025GD-41（表格见截图）
tab = {'A': (2000, .7, .15), 'B': (1500, .9, .20), 'C': (3000, .6, .15), 'D': (1800, .8, .20)}
sub = {k: p * d * r for k, (p, d, r) in tab.items()}
res['2025GD-41'] = max(sub, key=sub.get)
# 2025HB-73
res['2025HB-73'] = pick({'A': 0, 'B': 20, 'C': -20, 'D': -25}, 300 - (150 / 1.25 + 150 / 0.75))
# 2020HB-66 出租车最远里程（不足1公里按1公里）
def taxi(km):
    k = math.ceil(km)
    fee = 8
    for i in range(3, k + 1):
        fee += 2 if i <= 5 else (3 if i <= 8 else 4)
    return fee
mx = max(k for k in range(1, 30) if taxi(k) <= 20)
res['2020HB-66'] = pick({'A': 7, 'B': 8, 'C': 9, 'D': 10}, mx)
# 2020JSA-57
# R-E=1000, 1.15R-1.10E=1600
E = (1600 - 1.15 * 1000) / (1.15 - 1.10)
res['2020JSA-57'] = pick({'A': 9000, 'B': 9900, 'C': 10800, 'D': 11500}, 1.1 * E)
# 2020SC0725-51
sol = [(x, y) for x in range(0, 700) for y in range(0, 300) if 1.5 * x + 4 * y == 1000 and 1.5 * x + 2 * y == 800]
res['2020SC0725-51'] = pick({'A': 4, 'B': 3, 'C': 2, 'D': 1.5}, sol[0][0] / sol[0][1])
# 2020ZJB-15 包装合买（DP：花费 c 元最多能买多少盒）
packs = [(1, 10), (5, 40), (10, 70), (20, 120)]
def max_boxes(budget):
    best = [0] * (budget + 1)
    for c in range(1, budget + 1):
        best[c] = best[c - 1]
        for n, p in packs:
            if p <= c: best[c] = max(best[c], best[c - p] + n)
    return best
mb = max_boxes(1400)
budA = [c for c in range(1400) if mb[c] == 92]
budB = [c for c in range(1400) if mb[c] == 103]
exact = mb[min(budA) + min(budB)] - 92 - 103
loose = max(mb[a + b] for a in budA for b in budB) - 92 - 103
res['2020ZJB-15'] = pick({'A': 3, 'B': 5, 'C': 8, 'D': 10}, exact)
print('2020ZJB-15 预算区间: 甲', min(budA), '~', max(budA), ' 乙', min(budB), '~', max(budB),
      ' 预算恰为最低花费时多', exact, '盒；预算取区间上限时最多可多', loose, '盒')
# 2021JSA-59
before = 5 * 1 * 10 + 2 * 5 * 10; after = 5 * 2 * 2 + 2 * 10 * 5
res['2021JSA-59'] = pick({'A': .5, 'B': .6, 'C': .7, 'D': .8}, after / before)
# 2021JSA-62 买赠
def bag_cost(n):  # 买2送1，单价18
    g, r = divmod(n, 3); return g * 36 + r * 18
def db_cost(n):   # 买3送1，单价12
    g, r = divmod(n, 4); return g * 36 + r * 12
hits = [k for k, v in {'A': 24, 'B': 25, 'C': 26, 'D': 27}.items() if bag_cost(56 - v) + db_cost(v) == 606]
res['2021JSA-62'] = hits[0] if len(hits) == 1 else 'AMBIG' + str(hits)
# 2021ZJA-70
c = F(10) / F(65, 100)        # 原每亩成本（产量4、单价5赋值）
newp = 2 * (20 - c); ratio = newp / 30
res['2021ZJA-70'] = pick({'A': lambda r: r < .25, 'B': lambda r: .25 <= r <= .35, 'C': lambda r: .35 < r <= .45, 'D': lambda r: r > .45}, float(ratio))
# 2022GK-63
for x in range(1, 100):
    if abs(480 / x * 0.75 - 495 / (x + 3)) < 1e-9: dom = 495 / (x + 3)
res['2022GK-63'] = pick({'A': lambda v: v < 30, 'B': lambda v: 30 <= v <= 40, 'C': lambda v: 40 < v <= 50, 'D': lambda v: v > 50}, dom)
# 2022GK-72
# 赋值改造前日产10、能耗2；其他成本 o、单件利润 y：y = 3y-2-o ； 9(3y-1-o) = 1.1*10*y
from fractions import Fraction
# 由第一式 o = 2y-2，代入第二式
y = None
for num in range(1, 2000):
    yy = Fraction(num, 10); o = 2 * yy - 2
    if 9 * (3 * yy - 1 - o) == Fraction(11, 10) * 10 * yy: y = yy; oo = o
r = 2 / oo
res['2022GK-72'] = pick({'A': lambda v: v < .25, 'B': lambda v: .25 <= v <= 1 / 3, 'C': lambda v: 1 / 3 < v <= .5, 'D': lambda v: v > .5}, float(r))
# 2022GK-75
for x in range(1, 2000):   # 成本 x，定价 1.5x
    if abs(5 * ((1.5 * x - 30) * 0.8 - x) - (1.5 * x - x) - 130) < 1e-9: cost = x
price = 1.5 * cost; n0 = 15000 / price; target = 15000 / (n0 + 4)
o = {'A': (price - 50) * 0.8, 'B': price * 0.9 - 50, 'C': price - 150, 'D': price * 0.85}
res['2022GK-75'] = pick(o, target)
# 2022SD-40
def order(total_list):
    s = sum(total_list)
    disc = .10 if s > 1000 else .05 if s > 500 else .02 if s > 100 else 0
    return s * (1 - disc) + 6
cands = {}
for k, single in {'A': 123.6, 'B': 153, 'C': 183.6, 'D': 202}.items():
    # 单次买1本：定价 p，开销 order([p])；反解 p
    for p100 in range(1, 30000):
        p = p100 / 100
        if abs(order([p]) - single) < 1e-6:
            cands[k] = abs(10 * single - order([p] * 10) - 174) < 1e-6
res['2022SD-40'] = [k for k, v in cands.items() if v][0]
# 2023GK-61
for x in range(1, 2000):
    y = 0.6 * x
    if abs((x - y) - 3 * (x - 120 - y)) < 1e-9: res['2023GK-61'] = pick({'A': 360, 'B': 450, 'C': 540, 'D': 720}, x)
# 2023SC-52
# 2x+3y=130, 3x+2y=110
xp = (130 * 2 - 3 * 110) / (2 * 2 - 3 * 3); yp = (130 - 2 * xp) / 3
cnt = sum(1 for a in range(0, 6) if a * xp + (5 - a) * yp <= 120)
res['2023SC-52'] = pick({'A': 1, 'B': 2, 'C': 3, 'D': 4}, cnt)
# 2023SD-44
for xx in [k / 100 for k in range(1, 10000)]:
    if abs((1.5 * xx * 2) - (0.9 * xx * 2) - 3.6) < 1e-9: xn = xx
save_per_day = (4 * xn - (1.5 * xn + 0.9 * xn)) * 2
res['2023SD-44'] = pick({'A': 480, 'B': 300, 'C': 360, 'D': 540}, 3456 / save_per_day)
# 2024JSA-53
tot_cost = 7410 / 0.19; n = tot_cost / 100
xs = [x for x in range(0, int(n) + 1) if 30 * (n - x) - 9 * x == 7410]
res['2024JSA-53'] = pick({'A': 90, 'B': 100, 'C': 105, 'D': 110}, xs[0])
# 2024SC-47
def pay(orig):
    return orig * (.6 if orig >= 988 else .7 if orig >= 688 else .8 if orig >= 488 else 1)
def origs(paid):
    out = []
    for d in (1, .8, .7, .6):
        o_ = paid / d
        if abs(pay(o_) - paid) < 1e-6: out.append(o_)
    return out
save = max(400 + 630 - pay(a + b) for a in origs(400) for b in origs(630))
res['2024SC-47'] = pick({'A': 100, 'B': 190, 'C': 250, 'D': 412}, save)
# 2024SD-58
ok = [p for p in [x / 10 for x in range(80, 300)] if (p - 8) * (100 - 10 * (p - 10)) >= 350 - 1e-9]
lo, hi = min(ok), max(ok)
res['2024SD-58'] = 'B' if (13 <= lo and hi <= 15) else '?'
# 2024ZJA-59
def best(p):
    if p <= 50: return p
    return min((p - 20) * .9, p * .8 - 10)
cost2 = min(best(a) + best(b) for a, b in itertools.combinations([45, 75, 85], 2))
res['2024ZJA-59'] = pick({'A': lambda v: v < 90, 'B': lambda v: 90 <= v < 93, 'C': lambda v: 93 <= v < 96, 'D': lambda v: v >= 96}, cost2)
# 2025GK-76
s15 = sum(40 + 10 * d for d in range(1, 16))
# (0.8P - C)*s15 = (P - C)*800, P=1
C = (0.8 * s15 - 800) / (s15 - 800)
res['2025GK-76'] = pick({'A': .6, 'B': .64, 'C': .7, 'D': .75}, C)
# 2025SD-56
c = 288 / 120; pr = c * 1.5; exp_profit = 120 * (pr - c)
xprice = (0.85 * exp_profit - 90 * (pr - c)) / 30 + c
res['2025SD-56'] = pick({'A': .7, 'B': .75, 'C': .8, 'D': .85}, round(xprice / pr, 6))
# 2020SC0725-50 包装最优：x 支的最低价 = 1.7x - 2.3 的最大 x
def minprice(x):
    best = [0.0] + [1e9] * x
    for i in range(1, x + 1):
        best[i] = best[i - 1] + 1.7
        if i >= 3: best[i] = min(best[i], best[i - 3] + 5)
        if i >= 10: best[i] = min(best[i], best[i - 10] + 15)
    return best[x]
xs = [x for x in range(1, 200) if abs(minprice(x) - (1.7 * x - 2.3)) < 1e-6]
res['2020SC0725-50'] = pick({'A': 19, 'B': 21, 'C': 29, 'D': 31}, max(xs))
# 2024SZ-57 骑手分段计酬（a 为整数；30 单 247.5 元、40 单 315 元、仅第二日超健康临界）
sols = []
for a in range(1, 30):
    for k in range(0, 30):          # 基础接单量 k < 30
        for h in range(30, 40):     # 健康临界 30 <= h < 40（第一日未超、第二日超）
            if h < k: continue
            d1 = 30 * a + 1.5 * (30 - k)
            d2 = 40 * a + 1.5 * (h - k) - 1 * (40 - h)
            if abs(d1 - 247.5) < 1e-9 and abs(d2 - 315) < 1e-9: sols.append((a, k, h))
res['2024SZ-57'] = pick({'A': 5, 'B': 6, 'C': 7, 'D': 8}, sols[0][0] - 1) if len({s[0] for s in sols}) == 1 else 'AMBIG'
# 2025SD-58
nA_yi = 800; pA_yi = 70 * .6; pB_yi = 70 * .8
nB_yi = nA_yi * pA_yi / 2 / pB_yi
nA_jia = (123600 - nA_yi * pA_yi) / (50 * .6); nB_jia = (123600 - nB_yi * pB_yi) / (50 * .8)
ratio = (nA_jia + nB_jia) / (nA_yi + nB_yi)
res['2025SD-58'] = pick({'A': lambda v: v < 3, 'B': lambda v: 3 <= v <= 4, 'C': lambda v: 4 < v <= 5, 'D': lambda v: v > 5}, ratio)

bad = 0
for k in sorted(res):
    flag = 'OK ' if res[k] == official[k] else 'XX '
    if flag == 'XX ': bad += 1
    print(flag, k, 'computed', res[k], 'official', official[k])
print('checked', len(res), 'mismatch', bad)
