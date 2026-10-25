# Independent blind solver for D02 math (engineering problems). Written BEFORE opening the key.
# Each function derives the answer from stem data (simulation / brute force where possible)
# and returns the set of option letters that are correct.
import json, sys, datetime
from fractions import Fraction as F

QFILE = sys.argv[1]
qs = {q['vid']: q for q in json.load(open(QFILE, encoding='utf-8'))}

def opts(vid):
    return qs[vid]['options']

def match_num(vid, val):
    """Return option letters whose numeric content equals val."""
    out = []
    for k, v in opts(vid).items():
        try:
            if F(v) == F(val):
                out.append(k)
        except Exception:
            pass
    return out

res = {}

# ---- 1-v01: 820 boxes, A 6 days, B 5 days, A total - B total = 20. B daily?
def q1():
    sols = []
    for a in range(1, 1000):
        for b in range(1, 1000):
            if 6*a + 5*b == 820 and 6*a - 5*b == 20:
                sols.append((a, b))
    assert len(sols) == 1, sols
    return match_num('D02-math-1-v01', sols[0][1]), sols
res['D02-math-1-v01'] = q1()

# ---- 1-v02: 3L+2S=240, 2L+5S=270; have 4L+3S; need 1500 in 3 days; min extra S
def q2():
    sols = [(L, S) for L in range(1, 200) for S in range(1, 200) if 3*L+2*S == 240 and 2*L+5*S == 270]
    assert len(sols) == 1
    L, S = sols[0]
    n = 0
    while 3*(4*L + (3+n)*S) < 1500:
        n += 1
    return match_num('D02-math-1-v02', n), (L, S, n)
res['D02-math-1-v02'] = q2()

# ---- 1-v03: 6000 households, +20% per day -> 4 days earlier. original per day?
def q3():
    good = []
    for k, v in opts('D02-math-1-v03').items():
        r = F(v)
        if F(6000)/r - F(6000)/(r*F(6, 5)) == 4:
            good.append(k)
    return good, None
res['D02-math-1-v03'] = q3()

# ---- 1-v04: 甲 27 d, 甲+乙 18 d; start 11-20, 甲 alone 4 d, both x d, 乙 alone rest, finish on 12-19.
def q4():
    start = datetime.date(2025, 11, 20)
    end = datetime.date(2025, 12, 19)
    ndays = (end - start).days + 1  # inclusive
    jia = F(1, 27); yi = F(1, 18) - F(1, 27)
    good = []
    detail = {}
    for k, v in opts('D02-math-1-v04').items():
        x = int(v)
        done = 4*jia + x*(jia+yi)
        if done > 1:
            continue
        rest_days = (1 - done) / yi
        total = 4 + x + rest_days   # continuous time in days
        # finishes on calendar day ceil(total)
        import math
        day_idx = math.ceil(total)
        finish = start + datetime.timedelta(days=day_idx-1)
        detail[k] = (x, float(total), finish.isoformat())
        if finish == end:
            good.append(k)
    return good, (ndays, detail)
res['D02-math-1-v04'] = q4()

# ---- 1-v05: 甲乙 10, 乙丙 12, 甲丙 15; all three 4 days, then 乙丙 finish -> days?
def q5():
    ab, bc, ac = F(1, 10), F(1, 12), F(1, 15)
    s = (ab+bc+ac)/2
    rem = 1 - 4*s
    d = rem / bc
    return match_num('D02-math-1-v05', d), d
res['D02-math-1-v05'] = q5()

# ---- 1-v06: 甲 18 d, 乙 36 d; 甲 rests Sun, 乙 rests Sat+Sun; start Monday -> finish weekday
def q6():
    names = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    jia, yi = F(1, 18), F(1, 36)
    done = F(0); day = 0
    while True:
        wd = day % 7  # 0 = Monday
        r = 0
        if wd != 6: r += jia
        if wd not in (5, 6): r += yi
        done += r
        if done >= 1:
            break
        day += 1
    nm = names[day % 7]
    return [k for k, v in opts('D02-math-1-v06').items() if v == nm], (day+1, nm)
res['D02-math-1-v06'] = q6()

# ---- 1-v07: 12z+10w = 8(z+w)+12w = 1 -> 老周 alone days
def q7():
    # solve 12z+10w=1, 20w+8z=1
    # brute via fractions: Cramer's rule
    a1, b1, c1 = 12, 10, 1
    a2, b2, c2 = 8, 20, 1
    det = a1*b2 - a2*b1
    z = F(c1*b2 - c2*b1, det); w = F(a1*c2 - a2*c1, det)
    return match_num('D02-math-1-v07', 1/z), (z, w, 1/z, 1/w)
res['D02-math-1-v07'] = q7()

# ---- 1-v08: A = 3B workload; 甲 = 2*乙; 甲->A, 乙->B; 乙 then helps 2 h; A done. 甲 alone on A hours?
def q8():
    # unknown B workload b (in 乙-hours), rates 乙 = 1, 甲 = 2
    for b2 in range(1, 2000):
        b = F(b2, 10)
        A = 3*b
        t1 = b / 1           # 乙 finishes B
        remA = A - 2*t1
        if remA > 0 and remA == 3*2:   # 2 hours at combined 3
            return match_num('D02-math-1-v08', A/2), (b, A, A/2)
    return [], None
res['D02-math-1-v08'] = q8()

# ---- 1-v09: equal N; when 甲 done 乙 left 18, 丙 left 30; when 乙 done 丙 left 15
def q9():
    sols = []
    for N in range(31, 5000):
        # ratio 乙:丙 = (N-18):(N-30) must equal N:(N-15)
        if F(N-18, N-30) == F(N, N-15):
            sols.append(N)
    return match_num('D02-math-1-v09', sols[0]) if len(sols) == 1 else [], sols
res['D02-math-1-v09'] = q9()

# ---- 1-v10: 1200 m; A at half, B at 40%; then A +20%, B +50%; B remaining when A done
def q10():
    L = F(1200)
    vA = F(1); t = (L/2)/vA
    vB = (L*F(2, 5))/t
    vA2, vB2 = vA*F(6, 5), vB*F(3, 2)
    t2 = (L/2)/vA2
    left = L - L*F(2, 5) - vB2*t2
    return match_num('D02-math-1-v10', left), left
res['D02-math-1-v10'] = q10()

# ---- 1-v11: fuel 16 machines x 7 days (24h); after h hours 4 stop; remaining feeds 12 machines 9 days
def q11():
    total = 16*7*24
    sols = [h for h in range(0, 7*24+1) if total - 16*h == 12*9*24]
    return match_num('D02-math-1-v11', sols[0]) if sols else [], sols
res['D02-math-1-v11'] = q11()

# ---- 1-v12: rations N people 18 days; after 6 days +30 people; finishes 3 days early
def q12():
    sols = [N for N in range(1, 2000) if 18*N - 6*N == (18-3-6)*(N+30)]
    return match_num('D02-math-1-v12', sols[0]) if len(sols) == 1 else [], sols
res['D02-math-1-v12'] = q12()

# ---- 1-v13: big = 2 small; 8 big+4 small 6 days; after 2 days: 4 big, 8 small. remaining days?
def q13():
    s = F(1); b = 2*s
    total = (8*b + 4*s)*6
    rem = total - (8*b + 4*s)*2
    d = rem / (4*b + 8*s)
    return match_num('D02-math-1-v13', d), d
res['D02-math-1-v13'] = q13()

# ---- 1-v14: 27 cows 6 days; 23 cows 9 days; max cows balance
def q14():
    g = F(23*9 - 27*6, 9 - 6)
    init = 27*6 - g*6
    # max integer cows with non-decreasing grass: cows <= g
    import math
    n = math.floor(g)
    return match_num('D02-math-1-v14', n), (g, init)
res['D02-math-1-v14'] = q14()

# ---- 1-v15: 5 pumps 6h; 8 pumps 3h; within 4h min pumps
def q15():
    inflow = F(5*6 - 8*3, 6 - 3)
    init = 5*6 - inflow*6
    n = 1
    while n*4 < init + inflow*4:
        n += 1
    return match_num('D02-math-1-v15', n), (inflow, init, n)
res['D02-math-1-v15'] = q15()

# ---- 1-v16: per-acre a, growth g per acre per day; 10 acres 12 workers 10 days; 15 acres 20 workers 6 days
def q16():
    # 10a + 10*10 g = 120 ; 15a + 15*6 g = 120
    a1, b1, c1 = 10, 100, 120
    a2, b2, c2 = 15, 90, 120
    det = a1*b2 - a2*b1
    a = F(c1*b2 - c2*b1, det); g = F(a1*c2 - a2*c1, det)
    need = (24*a + 24*12*g) / 12
    return match_num('D02-math-1-v16', need), (a, g, need)
res['D02-math-1-v16'] = q16()

# ---- 2-v01: inlet 6h fill, outlet 8h empty; inlet alone 2h, then both. hours from opening outlet?
def q17():
    vin, vout = F(1, 6), F(1, 8)
    level = 2*vin
    t = (1 - level) / (vin - vout)
    return match_num('D02-math-2-v01', t), t
res['D02-math-2-v01'] = q17()

# ---- 2-v02: S甲 = 2 S乙; depths 9, 3; 甲 drops 0.25 m/h; time equal
def q18():
    S_yi = F(1); S_jia = 2*S_yi
    # step simulation in exact fractions per minute
    hj, hy = F(9), F(3)
    rate_j = F(1, 4)
    rate_y = rate_j*S_jia/S_yi
    t = (hj - hy)/(rate_j + rate_y)
    start = datetime.datetime(2025, 1, 1, 7, 30)
    tt = start + datetime.timedelta(hours=float(t))
    s = tt.strftime('%H:%M')
    return [k for k, v in opts('D02-math-2-v02').items() if v == s], (t, s)
res['D02-math-2-v02'] = q18()

# ---- 2-v03: drain at half height; inlet 4h fills (drain blocked); full->drain 6h to half; fill with drain open
def q19():
    vin = F(1, 4)
    vout = F(1, 2)/6
    # numeric simulation with small steps to double-check piecewise reasoning
    lvl = F(0); t = F(0); dt = F(1, 600)
    while lvl < 1:
        rate = vin - (vout if lvl > F(1, 2) else 0)
        lvl += rate*dt; t += dt
    return match_num('D02-math-2-v03', t), t
res['D02-math-2-v03'] = q19()

# ---- 2-v04: 甲+乙 plan 25 d; both 7 d, 乙 alone 4 d => 40%; 丙 (50 d) joins with 乙 x d; then all three; total 22 d
def q20():
    s = F(1, 25)
    yi = (F(2, 5) - 7*s)/4
    jia = s - yi
    bing = F(1, 50)
    good = []
    for k, v in opts('D02-math-2-v04').items():
        x = int(v)
        rem = 1 - F(2, 5) - x*(yi+bing)
        tail = rem/(jia+yi+bing)
        if 7 + 4 + x + tail == 22:
            good.append(k)
    return good, (jia, yi, bing)
res['D02-math-2-v04'] = q20()

# ---- 2-v05: plan both 15 d; both 3 d, 甲 alone y d, both 9 d; total 20 d. 甲 alone days?
def q21():
    y = 20 - 3 - 9
    # 12(j+i) + y j = 1, 15(j+i) = 1
    s = F(1, 15)
    j = (1 - 12*s)/y
    return match_num('D02-math-2-v05', 1/j), (j, s-j, 1/j)
res['D02-math-2-v05'] = q21()

# ---- 2-v06: 甲20 乙30 丙15; 甲乙 4 d; 乙 alone x d; 乙丙 4 d; 75 wan by work; 乙 share
def q22():
    j, y, b = F(1, 20), F(1, 30), F(1, 15)
    x = (1 - 4*(j+y) - 4*(y+b))/y
    yi_work = (4 + x + 4)*y
    return match_num('D02-math-2-v06', 75*yi_work), (x, yi_work, 75*yi_work)
res['D02-math-2-v06'] = q22()

# ---- 2-v07: 甲 24h, 乙 48h; both 6h; 乙 repair y h (甲 alone); then 甲 + 0.5乙 to finish; 3h late
def q23():
    j, y = F(1, 24), F(1, 48)
    plan = 1/(j+y)
    good = []
    for k, v in opts('D02-math-2-v07').items():
        r = int(v)
        done = 6*(j+y) + r*j
        if done >= 1:
            continue
        t = (1 - done)/(j + y/2)
        if 6 + r + t == plan + 3:
            good.append(k)
    return good, plan
res['D02-math-2-v07'] = q23()

# ---- 2-v08: +20% from start -> 5 days early; switch after x days -> 3 days early
def q24():
    # plan T days at rate 1: T - T/1.2 = 5
    T = None
    for t2 in range(1, 1000):
        t = F(t2)
        if t - t/F(6, 5) == 5:
            T = t; break
    good = []
    for k, v in opts('D02-math-2-v08').items():
        x = int(v)
        total = x + (T - x)/F(6, 5)
        if total == T - 3:
            good.append(k)
    return good, T
res['D02-math-2-v08'] = q24()

# ---- 2-v09: 张 9h, 李 12h; alternate 1 h; difference in minutes
def finish_alt(rates, durs, start_idx=0):
    done = F(0); t = F(0); i = start_idx
    while True:
        r, d = rates[i], durs[i]
        if done + r*d >= 1:
            t += (1 - done)/r
            return t
        done += r*d; t += d
        i = (i + 1) % len(rates)

def q25():
    tz = finish_alt([F(1, 9), F(1, 12)], [1, 1], 0)
    tl = finish_alt([F(1, 9), F(1, 12)], [1, 1], 1)
    diff = (tl - tz)*60
    return match_num('D02-math-2-v09', diff), (tz, tl, diff)
res['D02-math-2-v09'] = q25()

# ---- 2-v10: 甲 12h, 乙 18h; 甲 2h, 乙 1h alternate, 甲 first
def q26():
    t = finish_alt([F(1, 12), F(1, 18)], [2, 1], 0)
    h = int(t); m = (t - h)*60
    s = f"{h}小时" + (f"{int(m)}分" if m else "")
    return [k for k, v in opts('D02-math-2-v10').items() if v == s], (t, s)
res['D02-math-2-v10'] = q26()

# ---- 2-v11: warehouse; in 6 days fill, out 9 days empty; alternate in/out starting in; first full day
def q27():
    cap = F(1); vin, vout = F(1, 6), F(1, 9)
    lvl = F(0); day = 0
    while True:
        day += 1
        if day % 2 == 1:
            lvl = min(cap, lvl + vin)
        else:
            lvl = max(F(0), lvl - vout)
        if lvl >= cap:
            break
    return match_num('D02-math-2-v11', day), day
res['D02-math-2-v11'] = q27()

for vid, (good, info) in res.items():
    flag = 'OK ' if len(good) == 1 else '!! '
    print(flag, vid, good, info)
