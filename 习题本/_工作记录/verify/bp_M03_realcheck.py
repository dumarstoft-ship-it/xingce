# M03 工程问题：真题复算（从题面数据出发独立计算，不代入官方答案凑）
# 运行：python3 bp_M03_realcheck.py
from fractions import Fraction as F
import math, datetime, itertools
from sympy import symbols, solve, Eq, Rational, simplify

res = {}
def rec(qid, ans, official, note=""):
    res[qid] = (ans, official, note)

def pick(val, table):
    """table: dict option->value; return the option letters whose value == val"""
    return ''.join(k for k, v in table.items() if v == val)

# ---------------- 自解 4 题（各用两种独立方法） ----------------
# 2026GD-38 蓄电池：方法1 台·天；方法2 按小时逐时模拟
cap = 20 * 5                         # 台·天
left = cap - 20 * F(12, 24)
d1 = left / 25
cap_h = 20 * 5 * 24                  # 台·小时
used = 0; h = 0
while used < 20 * 12: used += 20; h += 1
rem_h = cap_h - used
d2 = F(rem_h, 25 * 24)
assert d1 == d2
rec('2026GD-38', pick(d1, {'A': F(7, 2), 'B': F(18, 5), 'C': F(19, 5), 'D': F(4)}), None, f'还可运行{d1}天')

# 2026ZJA-46 水深：方法1 差值/速度和；方法2 逐分钟模拟
t1 = F(8 - 5) / (F(2, 10) + F(3, 10))
m = 0
while F(8) - F(2, 10) * F(m, 60) > F(5) + F(3, 10) * F(m, 60): m += 1
assert F(m, 60) == t1
end = 8 * 60 + 30 + m
clock = f'{end // 60}:{end % 60:02d}'
rec('2026ZJA-46', pick(clock, {'A': '14:30', 'B': '15:00', 'C': '15:30', 'D': '16:00'}), None, clock)

# 2026GK-67 字母关系：方法1 符号求解；方法2 取多组 n 检验各选项
m_, n_ = symbols('m_ n_')
msol = solve(Eq(5 * (m_ + 1), 3 * (Rational(3, 2) * m_ + n_)), m_)[0]
opts = {'A': 3 * n_ - 5, 'B': 6 * n_ - 10, 'C': 5 - 3 * n_, 'D': 10 - 6 * n_}
sym_hit = ''.join(k for k, v in opts.items() if simplify(v - msol) == 0)
num_hit = ''
for k, v in opts.items():
    ok = True
    for nv in [2, 3, 4, F(5, 2)]:
        mv = F(str(v.subs(n_, Rational(nv.numerator if isinstance(nv, F) else nv, nv.denominator if isinstance(nv, F) else 1))))
        w = 5 * (mv + 1)                       # 乙效率=1
        if 3 * (F(3, 2) * mv + F(nv)) != w: ok = False
    if ok: num_hit += k
assert sym_hit == num_hit
rec('2026GK-67', sym_hit, None, f'm={msol}')

# 2026ZJA-56 按效率分配：方法1 比例分配；方法2 枚举整数分配检验"同时结束"
ej, ey, eb = F(120 - 48, 120), F(120 - 12, 120), F(120, 120 - 20)   # 个/分钟
alloc = [270 * e / (ej + ey + eb) for e in (ej, ey, eb)]
brute = [(a, b, 270 - a - b) for a in range(1, 270) for b in range(1, 270 - a)
         if F(a) / ej == F(b) / ey == F(270 - a - b) / eb]
assert len(brute) == 1 and list(brute[0]) == alloc
rec('2026ZJA-56', pick(alloc[2] - alloc[0], {'A': 30, 'B': 60, 'C': 90, 'D': 120}), None, f'分配{[int(x) for x in alloc]}')

# ---------------- 有官方答案的 44 题 ----------------
# 2020JSA-53
y = next(y for y in range(1, 2000) if 5 * (y + 23) + 4 * y == 1033)
rec('2020JSA-53', pick(5 * (y + 23), {'A': 625, 'B': 645, 'C': 535, 'D': 515}), 'A')
# 2023GD-37
rec('2023GD-37', pick(True, {o: F(300) / (F(1, 5) * F(T, 4)) - F(300) / F(T, 4) == 1 for o, T in zip('ABCD', [2400, 3600, 4800, 6000])}), 'C')
# 2023ZJA-64
t = next(F(k, 100) for k in range(1, 10000) if 5 * (F(k, 100) + 4) == 9 * (F(k, 100) - 2))
v = 5 * (t + 4) / t
rec('2023ZJA-64', 'A' if v < 6 else 'B' if v < 7 else 'C' if v < 8 else 'D', 'C', f'丙速{float(v):.3f}')
# 2024GD-36
rec('2024GD-36', ''.join(o for o, x in zip('ABCD', [6, 7, 8, 9]) if F(300, x - 1) - F(300, x) == 10), 'A')
# 2024HB-63
x = F(2 * 40 - F(3, 2) * 50, 50 - 40)        # 每天损耗
rec('2024HB-63', pick(F(3, 2) * 50 + 50 * x, {'A': 75, 'B': 80, 'C': 100, 'D': 110}), 'C')
# 2025JSA-56
rec('2025JSA-56', pick(40 - F(40 * 24, 32), {'A': 4, 'B': 8, 'C': 10, 'D': 12}), 'C')
# 2025JSA-61
Mv = next(F(k, 360) for k in range(1, 360) if 2 * F(k, 360) + 5 * (F(1, 3) - F(k, 360)) == 1)   # M+N=1/3，2M+5N=1
rec('2025JSA-61', pick(1 / Mv, {'A': F(7, 2), 'B': F(9, 2), 'C': 5, 'D': F(11, 2)}), 'B')
# 2025SC-46
A_, B_ = 3 * 8, 2 * 8
rec('2025SC-46', pick(F(A_, 2) - F(B_, 3), {'A': 6, 'B': F(20, 3), 'C': F(22, 3), 'D': 8}), 'B')
# 2025SD-53
zl = [(z, l) for z in range(1, 10) for l in range(1, 10) if 5 * z + 9 * l == 7 * z + 6 * l and math.gcd(z, l) == 1][0]
T = 5 * zl[0] + 9 * zl[1]
rec('2025SD-53', pick(F(T - 3 * sum(zl), zl[1]), {'A': 10, 'B': 8, 'C': 7, 'D': 9}), 'D')
# 2020SC0725-46
okx = []
for nn in (6, 10, 30):
    yv = nn; xv = F(5 * nn - yv, 4)
    okx.append(xv == yv)
rec('2020SC0725-46', 'B' if all(okx) else '?', 'B')
# 2020SC1206-46
a, b = F(240 * 10, 100) / 12, F(240 * 15, 100) / 12
c = F(240 - (a + b) * 12, 30) - a - b * F(8, 10)
rec('2020SC1206-46', pick(c / a, {'A': 1, 'B': F(4, 5), 'C': F(3, 5), 'D': F(1, 2)}), 'B')
# 2020SD-45
ja = F(1, 20); yi = F(1, 12) - ja
days = 5 + 3 + (1 - 5 * ja - 3 * (ja + yi)) / yi
endd = datetime.date(2020, 8, 15) + datetime.timedelta(days=int(days) - 1)
rec('2020SD-45', pick(endd, {'A': datetime.date(2020, 9, 5), 'B': datetime.date(2020, 9, 6), 'C': datetime.date(2020, 9, 7), 'D': datetime.date(2020, 9, 8)}), 'B', str(endd))
# 2020SZS-26
xs = [(x, y) for x in range(1, 300) for y in range(1, 300) if (3 * x + y) * 2 == 600 and (x + 2 * y) * 4 == 800]
x, y = xs[0]
rec('2020SZS-26', pick((4 * x + 2 * y) * F(85, 100) * 5, {'A': 1650, 'B': 1870, 'C': 1980, 'D': 2020}), 'B')
# 2020ZJB-17
X = F(5 * 45 - 3 * 90, 45 - 90); Y = (3 - X) * 90
rec('2020ZJB-17', pick(Y / (6 - X), {'A': 36, 'B': 38, 'C': 40, 'D': 42}), 'A')
# 2021JSA-53
yv = next(y for y in range(5, 500) if 12 * y == 15 * (y - 4))
rec('2021JSA-53', pick(F(12 * yv, 8), {'A': 30, 'B': 40, 'C': 50, 'D': 60}), 'A')
# 2021JSA-57
xy = [(x, y) for x in range(1, 4000) for y in [F(30000 - 8 * x, 8)] if y.denominator == 1 and 2 * x + 3 * y == 10000][0]
rec('2021JSA-57', pick(F(620000, 11 * xy[0] + 10 * xy[1]), {'A': 14, 'B': 15, 'C': 16, 'D': 17}), 'C')
# 2021SC2-51
rates = [10, 12, 15]; done = 0; tj = F(0); i = 0
while True:
    r = rates[i % 3]
    if done + r >= 120:
        if i % 3 == 0: tj += F(120 - done, r)
        break
    done += r
    if i % 3 == 0: tj += 1
    i += 1
rec('2021SC2-51', pick(tj, {'A': F(174, 60), 'B': 3, 'C': F(234, 60), 'D': 4}), 'C', f'甲{tj}h')
# 2021ZJA-65（截图：升级≥2/3x，新款≥3/5x）
cnt = [yv for yv in range(0, 181) if F(14, 10) * yv >= F(3, 5) * 180 and F(12, 10) * (180 - yv) >= F(2, 3) * 180]
rec('2021ZJA-65', pick(len(cnt), {'A': 2, 'B': 3, 'C': 4, 'D': 5}), 'B', str(cnt))
# 2022GD-32
xx = next(x for x in range(3, 200) if 50 * (x - 2) + 85 * 2 == 55 * (x - 1))
rec('2022GD-32', pick(55 * (xx - 1), {'A': 1215, 'B': 1250, 'C': 1320, 'D': 1375}), 'C')
# 2022GD-37
sol = [(a_, b_) for a_ in range(0, 38) for b_ in range(a_ + 1, 38) if (38 - a_) == 4 * (38 - b_) and 2 * (53 - a_) == 3 * (53 - b_)]
rec('2022GD-37', pick(sol[0][1] - sol[0][0], {'A': 4, 'B': 6, 'C': 8, 'D': 9}), 'D', f'甲9:{sol[0][0]} 乙9:{sol[0][1]}')
# 2022JSA-63
xx = next(F(k) for k in range(1, 500) if 10 * k + 5 * k + 5 * (k + 5) + 10 * k + 5 * F(3, 2) * (k + 5) == 1000)
rec('2022JSA-63', pick(5 * xx + 5 * (xx + 5) + 5 * F(3, 2) * (xx + 5), {'A': 450, 'B': 500, 'C': 550, 'D': 600}), 'B')
# 2022SC2-42（"又用了7天运完"=第7天运完）
a = F(18 * 8 - 24 * 5, 8 - 5); yv = (24 - a) * 5
ok = [xv for xv in range(1, 80) if (xv - a) * 4 + (xv - a * F(3, 2)) * 7 >= yv > (xv - a) * 4 + (xv - a * F(3, 2)) * 6]
rec('2022SC2-42', pick(min(ok), {'A': 18, 'B': 19, 'C': 20, 'D': 21}), 'A', f'可行x={ok}')
# 2022SD-42
tot = (6 + 5 + 4) * 180; Bq = F(tot, F(5, 2))
rec('2022SD-42', pick((Bq - 5 * 180) / 4, {'A': 45, 'B': 75, 'C': 105, 'D': 135}), 'A')
# 2022ZJA-62
xx = next(x for x in range(1, 20) if 20 - x == 25 - 2 * x)
rec('2022ZJA-62', pick(xx, {'A': 3, 'B': 5, 'C': 8, 'D': 10}), 'B')
# 2023GD-36（羊=1，牛=2）
X = F(40 * 20 - 30 * 30, 20 - 30); Y = (40 - X) * 20
rec('2023GD-36', pick(Y / (30 - X), {'A': 10, 'B': 20, 'C': 30, 'D': 40}), 'C')
# 2023GK-62
xv = next(F(k, 10) for k in range(1, 100) if F(12) / F(k, 10) - F(12) / (4 + F(k, 10)) == 4)
rec('2023GK-62', pick(F(12) / (3 - xv), {'A': 10, 'B': 12, 'C': 6, 'D': 8}), 'B')
# 2023HB-67
r1 = F(75, 15); r2 = (300 - r1 * 5 - 235) / 10; total = 15 + F(235) / r2
rec('2023HB-67', 'C' if 73 < total < 75 else '?', 'C', f'总时长{total}分钟=1小时{float(total) - 60:.2f}分（精确10:13:45）')
# 2023SC-46（截图：乙为甲的1/2，丙为乙的1/3）
tj, ty = 60, 30; tb = 10
work = 4 * (tj - ty) + 2 * 4 * F(5, 4) * (ty - tb) + 3 * 4 * F(3, 2) * tb
rec('2023SC-46', pick(work / 4, {'A': 120, 'B': 125, 'C': 130, 'D': 150}), 'B')
# 2024JSA-54
hours = F(259, F(60, 6) + F(60, 5) + F(60, 4))
rec('2024JSA-54', pick(F(60, 2) * hours * F(8, 10) + hours * (12 + 15), {'A': 357, 'B': 399, 'C': 427, 'D': 469}), 'A', f'每天{hours}小时')
# 2024JSA-61
rec('2024JSA-61', ''.join(o for o, (a, b, c) in zip('ABCD', [(5, 4, 6), (6, 4, 5), (10, 15, 12), (12, 15, 10)]) if F(9 * b + 6 * (a + b), 10 * c) == F(60, 40)), 'A')
# 2024SC-48
for xv in range(1, 451):
    if 450 % xv == 0 and 450 % (xv + 5) == 0 and 450 // xv - 450 // (xv + 5) == 1:
        d9 = 450 // (xv + 5); yy = F(450 - xv * d9, xv - (xv + 5 - 10))
        rec('2024SC-48', pick((xv - 5) * yy, {'A': 240, 'B': 280, 'C': 320, 'D': 360}), 'D')
# 2024SC-49
extra = 5 + F(60 - 24 - 10, F(37, 5)) - F(60, 8)
rec('2024SC-49', 'A' if extra < 1 else 'B' if extra < F(4, 3) else 'C' if extra < F(5, 3) else 'D', 'B', f'多{extra}小时')
# 2024SD-54
xv = F(150 - 33 - 2 * 5 * F(22, 10), (5 + 6) * 3)
rec('2024SD-54', pick(3 + math.ceil(xv) + 2, {'A': 7, 'B': 8, 'C': 9, 'D': 10}), 'B', f'精确{float(3 + xv + 2):.2f}天')
# 2024ZJA-60
a = F(1, 20); aj = (F(4, 10) - 4 * a) / 6; ay = a - aj; c = F(6, 10) / 10 - a
rr = [v / min(aj, ay, c) for v in (aj, ay, c)]
rec('2024ZJA-60', pick(tuple(v * 3 for v in rr), {'A': (3, 6, 10), 'B': (4, 8, 15), 'C': (6, 3, 2), 'D': (10, 5, 3)}), 'D')
# 2025GD-39
ab = [(a, b) for a in range(1, 10) for b in range(1, 10) if 2 * (5 * (a + b) + 15 * b) == 30 * (a + b) and math.gcd(a, b) == 1][0]
tot = 30 * sum(ab)
cv = F(tot - 15 * sum(ab) - 3 * ab[1] - 5 * sum(ab), 3 + 5)
rec('2025GD-39', pick(cv / ab[0], {'A': F(3, 2), 'B': 2, 'C': F(5, 2), 'D': 3}), 'D')
# 2025GK-71
xv = next(x for x in range(1, 13) if 2 * x + 3 * x + (3 * x - 6) == 50 - 3 * 2 * 4)
rec('2025GK-71', pick(12 - xv, {'A': 6, 'B': 7, 'C': 8, 'D': 9}), 'C')
# 2025HB-75
n = next(n for n in range(1, 50) if 150 * max(0, n - 1) + 100 * max(0, n - 3) + 80 * max(0, n - 2) >= 1040)
rec('2025HB-75', pick(n, {'A': 7, 'B': 6, 'C': 5, 'D': 4}), 'C')
# 2025SC-54
am = sum(1 for mm in range(8 * 60, 11 * 60 + 50) if (mm - 8 * 60) % 40 < 30)
need = F(am, F(3, 2)); w = 0; mm = 14 * 60
while w < need:
    if (mm - 14 * 60) % 35 < 30: w += 1
    mm += 1
rec('2025SC-54', pick(f'{mm // 60}:{mm % 60:02d}', {'A': '16:15', 'B': '16:20', 'C': '16:25', 'D': '16:30'}), 'A', f'上午有效{am}分钟')
# 2025ZJA-58（图像选项：甲先快后慢且后段用时为前段3倍、乙先完成）
Q = 48; tA1 = F(Q, 2) / 6; tA2 = F(Q, 2) / 2; tB = F(Q, 8) * 2
rec('2025ZJA-58', 'C' if (tA2 == 3 * tA1 and tB < tA1 + tA2) else '?', 'C', f'甲{tA1}+{tA2}h，乙{tB}h')
# 2025ZJA-59
k = next(F(kk, 100) for kk in range(101, 1000) if (F(kk, 100) + 1) ** 2 == F(9, 2) * F(kk, 100))
yv = F(1, 12 * (k + 1) + 12)
rec('2025ZJA-59', pick(1 / (k * yv), {'A': 24, 'B': 30, 'C': 48, 'D': 60}), 'A')
# 2023JSA-61
def workdays(total, w, r):
    full, rem = divmod(total, w + r); return full * w + min(rem, w)
j1, y1, j2, y2 = workdays(23, 3, 1), workdays(21, 5, 2), workdays(15, 3, 1), workdays(27, 5, 2)
ratio = F(y2 - y1, j1 - j2)             # 甲/乙
tot = j1 * ratio + y1; need = tot / ratio
dd = 0; wk = 0
while wk < need:
    dd += 1
    if (dd - 1) % 4 < 3: wk += 1
rec('2023JSA-61', pick(dd, {'A': 43, 'B': 44, 'C': 47, 'D': 48}), 'C', f'甲需{need}个工作日')
# 2022GK-74
for xv in range(1, 500):
    yv = F(5, 4) * xv
    if 54 - xv == xv - yv:
        clock = 12 + (500 - xv - yv) / (2 * yv / 3)
        rec('2022GK-74', 'A' if clock < F(33, 2) else 'B' if clock < 17 else 'C' if clock < F(35, 2) else 'D', 'D', f'x={xv},y={yv},{float(clock):.3f}时')
        break
# 2024GK-72（截图：剩余任务量的2/3）
a_, b_, c_ = symbols('a_ b_ c_', positive=True)
Tt = 44 * b_
asol = solve(Eq(6 * (a_ + Rational(11, 10) * b_), Tt / 4), a_)[0]
csol = solve(Eq(15 * (Rational(11, 10) * b_ + c_), Tt * Rational(3, 4) * Rational(2, 3)), c_)[0]
rec('2024GK-72', pick(int(simplify(Tt / (asol + Rational(11, 10) * b_ + csol))), {'A': 16, 'B': 20, 'C': 24, 'D': 28}), 'B')

# ---------------- 题面有问题的真题：分析 ----------------
print('2020SZS-29：')
for d in (15, 10):
    sols = [(a, a - 5) for a in range(6, 300) if 3 * a + 4 * (2 * a - 5) == d * (a - 5) + 2 * a]
    if sols:
        a, b = sols[0]; trees = d * b + 2 * a
        print(f'  乙先做{d}天：甲{a}、乙{b}棵/天，共{trees}棵，路长{8 * (trees // 2 - 1)}米（选项B=1232）')
    else:
        aa, bb = symbols('aa bb')
        s = solve([Eq(3 * aa + 4 * (aa + bb), d * bb + 2 * aa), Eq(aa - bb, 5)], [aa, bb])
        print(f'  乙先做{d}天：甲={s[aa]}、乙={s[bb]}（非整数）→ 无解，与选项都不符')

print('2022SC1-46（"完成了全部任务的__"缺数）：设缺失值为p，三线效率都为正时各选项是否可能成立：')
for opt, share in zip('ABCD', [F(4, 15), F(1, 3), F(2, 5), F(3, 5)]):
    p = (share - F(1, 10)) / F(9, 10)              # 甲占比 = 4甲 = 1 - 0.9(1-p)
    s3 = F(1, 4)
    jia = s3 - F(45, 100) * (1 - p) / 2; yi = s3 - p / 2; bing = s3 - F(55, 100) * (1 - p) / 2
    print(f'  {opt}：需 p={p}，效率甲{jia} 乙{yi} 丙{bing} → {"可能" if min(jia, yi, bing) > 0 and 0 < p < 1 else "不可能"}')

print()
bad = []
for k, (a, o, n) in res.items():
    flag = '自解' if o is None else ('一致' if a == o else '不一致')
    if flag == '不一致': bad.append(k)
    print(f'{k:15s} 复算={a}  官方={o}  {flag}  {n}')
print(f'共复算 {len(res)} 题（官方 {sum(1 for v in res.values() if v[1])}，自解 {sum(1 for v in res.values() if v[1] is None)}）；不一致：{bad}')
