# L01 翻译推理 —— 蓝图里每道改编设计的独立验算
# 做法：把 idea 里写定的题干条件翻译成命题/集合/可能世界模型，逐项判断选项，
# 从题面条件出发计算（不是把预期答案代回去），并确认四个选项恰好一个满足设问。
# 编号 d-g-v = 第 d 天第 g 组第 v 道改编（与 blueprints/L01.md、L01.json 一致；一拖二记作 v.1 / v.2）。
import itertools

def imp(a, b): return (not a) or b
def xor(a, b): return a != b
def iff(a, b): return a == b

# ---------------- 命题逻辑 ----------------
def models(names, prem):
    for vals in itertools.product([False, True], repeat=len(names)):
        m = dict(zip(names, vals))
        if all(p(m) for p in prem):
            yield m

def ent(names, prem, f):
    ms = list(models(names, prem))
    assert ms, "题干条件不相容"
    return all(f(m) for m in ms)

def cons(names, prem):
    return next(models(names, prem), None) is not None

REPORT = []
def check(code, status, expect, note=""):
    hits = sorted(k for k, v in status.items() if v)
    want = [expect] if isinstance(expect, str) else sorted(expect)
    REPORT.append((code, "/".join(hits) if hits else "无", "/".join(want), hits == want, note))

def entail(code, n, P, O, e): check(code, {k: ent(n, P, f) for k, f in O.items()}, e)
def notentail(code, n, P, O, e): check(code, {k: not ent(n, P, f) for k, f in O.items()}, e)
def impossible(code, n, P, O, e): check(code, {k: not cons(n, P + [f]) for k, f in O.items()}, e)
def possible(code, n, P, O, e): check(code, {k: cons(n, P + [f]) for k, f in O.items()}, e)
def bridge(code, n, P, O, T, e):
    check(code, {k: cons(n, P + [f]) and ent(n, P + [f], T) for k, f in O.items()}, e)
def bridge_fail(code, n, P, O, T, e):   # 选非：补充后不能得出结论
    check(code, {k: not (cons(n, P + [f]) and ent(n, P + [f], T)) for k, f in O.items()}, e)
def combo(code, n, P, S, C, e, kind="entail"):
    if kind == "entail":
        got = {i for i, f in S.items() if ent(n, P, f)}
    elif kind == "bridge":   # S 中每项为 (补充条件, 目标)
        got = {i for i, (f, t) in S.items() if cons(n, P + [f]) and ent(n, P + [f], t)}
    check(code, {k: got == set(v) for k, v in C.items()}, e, "成立项=" + str(sorted(got)))
def count(code, n, P, S, C, e):
    c = sum(1 for f in S.values() if ent(n, P, f))
    check(code, {k: c == v for k, v in C.items()}, e, "成立项数=%d" % c)
def equiv(code, n, stem, O, e):
    allv = [dict(zip(n, v)) for v in itertools.product([False, True], repeat=len(n))]
    check(code, {k: all(stem(m) == f(m) for m in allv) for k, f in O.items()}, e)
def violation(code, n, rule, cases, C, e):
    vio = {i for i, c in cases.items() if ent(n, [c], lambda m: not rule(m))}
    check(code, {k: vio == set(v) for k, v in C.items()}, e, "违反=" + str(sorted(vio)))
def minmax(code, n, P, which, C, e, over=None):
    ms = list(models(n, P)); assert ms
    over = over or n
    sizes = [sum(m[x] for x in over) for m in ms]
    val = min(sizes) if which == "min" else max(sizes)
    check(code, {k: val == v for k, v in C.items()}, e, "%s=%d" % (which, val))

# ---------------- 直言命题：类型模型 ----------------
# 一个"模型"= 若干非空类型（谓词真假组合）的集合；全称句限制允许出现的类型，特称句要求有见证类型。
def ctypes(preds): return [dict(zip(preds, v)) for v in itertools.product([False, True], repeat=len(preds))]
def callowed(preds, U): return [t for t in ctypes(preds) if all(u(t) for u in U)]
def cok(preds, U, E):
    a = callowed(preds, U); return all(any(e(t) for t in a) for e in E)
def c_univ(preds, U, E, f):          # "所有……"是否必然为真
    assert cok(preds, U, E), "直言前提不相容"
    return all(f(t) for t in callowed(preds, U))
def c_exist(preds, U, E, g):         # "有的……"是否必然为真
    assert cok(preds, U, E), "直言前提不相容"
    rest = [t for t in callowed(preds, U) if not g(t)]
    return not all(any(e(t) for t in rest) for e in E)
def c_poss_exist(preds, U, E, g):    # "有的……"是否可能为真
    return cok(preds, U, E) and any(g(t) for t in callowed(preds, U))
def c_poss_univ(preds, U, E, f):     # "所有……"是否可能为真
    a = [t for t in callowed(preds, U) if f(t)]
    return all(any(e(t) for t in a) for e in E)
# 选项写成 ("U", f) 全称 / ("E", g) 特称
def c_true(preds, U, E, o):
    return c_univ(preds, U, E, o[1]) if o[0] == "U" else c_exist(preds, U, E, o[1])
def c_poss(preds, U, E, o):
    return c_poss_univ(preds, U, E, o[1]) if o[0] == "U" else c_poss_exist(preds, U, E, o[1])
def c_entail(code, preds, U, E, O, e): check(code, {k: c_true(preds, U, E, o) for k, o in O.items()}, e)
def c_notentail(code, preds, U, E, O, e): check(code, {k: not c_true(preds, U, E, o) for k, o in O.items()}, e)
def c_impossible(code, preds, U, E, O, e): check(code, {k: not c_poss(preds, U, E, o) for k, o in O.items()}, e)
def c_possible(code, preds, U, E, O, e): check(code, {k: c_poss(preds, U, E, o) for k, o in O.items()}, e)
def c_unknown(code, preds, U, E, O, e):   # 真假不能确定
    def unk(o):
        t = c_true(preds, U, E, o)
        neg = ("E", lambda x, f=o[1]: not f(x)) if o[0] == "U" else ("U", lambda x, g=o[1]: not g(x))
        return (not t) and c_poss(preds, U, E, o) and c_poss(preds, U, E, neg)
    check(code, {k: unk(o) for k, o in O.items()}, e)
def c_bridge(code, preds, U, E, O, concl, e):
    """补充 O[k]（("U",f) 或 ("E",g)）后，结论 concl（同样格式）必然成立且补充后相容"""
    st = {}
    for k, o in O.items():
        U2 = U + ([o[1]] if o[0] == "U" else []); E2 = E + ([o[1]] if o[0] == "E" else [])
        st[k] = cok(preds, U2, E2) and c_true(preds, U2, E2, concl)
    check(code, st, e)

# ---------------- 可能世界（模态） ----------------
# 世界 = 若干"随世界变化"的原子命题的赋值；模型 = (非空世界集 W, 现实世界 w0∈W, 全局事实 g)
def kmodels(wvars, gvars=(), wcon=lambda w: True):
    worlds = [dict(zip(wvars, v)) for v in itertools.product([False, True], repeat=len(wvars))]
    worlds = [w for w in worlds if wcon(w)]
    gs = [dict(zip(gvars, v)) for v in itertools.product([False, True], repeat=len(gvars))]
    for r in range(1, len(worlds) + 1):
        for W in itertools.combinations(range(len(worlds)), r):
            Ws = [worlds[i] for i in W]
            for w0 in Ws:
                for g in gs:
                    yield {"W": Ws, "w0": w0, "g": g}
def BOX(M, f): return all(f(w) for w in M["W"])
def DIA(M, f): return any(f(w) for w in M["W"])
def k_ent(wv, gv, P, f, wcon=lambda w: True):
    ms = [M for M in kmodels(wv, gv, wcon) if all(p(M) for p in P)]; assert ms
    return all(f(M) for M in ms)
def k_cons(wv, gv, P, wcon=lambda w: True):
    return any(all(p(M) for p in P) for M in kmodels(wv, gv, wcon))
def k_entail(code, wv, gv, P, O, e, wcon=lambda w: True):
    check(code, {k: k_ent(wv, gv, P, f, wcon) for k, f in O.items()}, e)
def k_contra(code, wv, gv, P, O, e, wcon=lambda w: True):
    check(code, {k: not k_cons(wv, gv, P + [f], wcon) for k, f in O.items()}, e)
def pair_profile(wv, gv, f1, f2, wcon=lambda w: True):
    return {(f1(M), f2(M)) for M in kmodels(wv, gv, wcon)}

def run_and_report(title):
    w = max(len(r[0]) for r in REPORT)
    bad = 0
    for code, got, want, ok, note in REPORT:
        if not ok: bad += 1
        print(f"{code:<{w}}  程序={got:<10} 设计={want:<6} {'OK' if ok else '**FAIL**'}  {note}")
    print(f"{title}: 共 {len(REPORT)} 项，失败 {bad} 项")
    return bad

# =====================================================================
# 第 1 天
# =====================================================================
# 1-1 考法一
n = ["T", "P", "Q", "R"]   # T推行一窗通办 P排队缩短 Q一人通办多项 R完成综合培训
notentail("1-1-1", n, [lambda m: imp(m["T"], m["P"]), lambda m: imp(m["Q"], m["R"])], {
    "A": lambda m: imp(not m["P"], not m["T"]), "B": lambda m: imp(not m["R"], not m["Q"]),
    "C": lambda m: imp(m["Q"], m["R"]), "D": lambda m: imp(m["P"], m["T"])}, "D")
n = ["S", "C", "T", "W", "F", "X", "A"]  # 申报示范村 充电点 通道 拆违 及时发现 巡查 安置
entail("1-1-2", n, [lambda m: imp(m["S"], m["C"]), lambda m: imp(m["T"], m["W"]),
                    lambda m: imp(m["F"], m["X"]), lambda m: imp(m["W"], m["A"])], {
    "A": lambda m: imp(m["C"], m["S"]), "B": lambda m: imp(not m["W"], not m["A"]),
    "C": lambda m: imp(m["T"], m["A"]), "D": lambda m: imp(m["X"], m["F"])}, "C")
n = ["D", "J", "W", "Y", "C", "G", "H"]  # 下沉 就近解决 有温度 议事会 参与决策 事事有人管 好坏大家判
entail("1-1-3", n, [lambda m: imp(not m["D"], not m["J"]), lambda m: imp(not m["J"], not m["W"]),
                    lambda m: imp(m["C"], m["Y"])], {
    "A": lambda m: imp(m["W"], m["D"]), "B": lambda m: imp(m["Y"], m["C"]),
    "C": lambda m: imp(m["H"], m["G"]), "D": lambda m: imp(m["J"], m["W"])}, "A")
n = ["B", "P"]   # B纳入白名单 P通过评审；除非P否则不B：B->P
count("1-1-4", n, [lambda m: imp(m["B"], m["P"])], {
    1: lambda m: imp(m["B"], m["P"]), 2: lambda m: xor(m["P"], not m["B"]),
    3: lambda m: m["P"] or not m["B"], 4: lambda m: imp(not m["B"], not m["P"])},
    {"A": 1, "B": 2, "C": 3, "D": 4}, "B")
n = ["Q", "Y", "W", "S"]  # 谋全局 足谋一域 谋万世 足谋一时
entail("1-1-5", n, [lambda m: imp(not m["Q"], not m["Y"]), lambda m: imp(not m["W"], not m["S"])], {
    "A": lambda m: imp(m["Q"], m["Y"]), "B": lambda m: imp(m["S"], m["W"]),
    "C": lambda m: imp(not m["Y"], not m["Q"]), "D": lambda m: imp(m["W"], m["S"])}, "B")

# 1-2 考法二
n = ["U", "F", "T", "X"]  # 用好抓手 做强特色产业 推进工程 协调发展取得进展
impossible("1-2-1", n, [lambda m: imp(m["U"], m["F"])], {
    "A": lambda m: m["U"] and not m["F"], "B": lambda m: m["F"] and not m["U"],
    "C": lambda m: (not m["T"]) and m["X"], "D": lambda m: m["T"] and not m["X"]}, "A")
n = ["Z", "R", "L", "G"]  # 乡村振兴 人才振兴 年轻人愿留 就业岗位
entail("1-2-2", n, [lambda m: imp(m["Z"], m["R"]), lambda m: imp(m["R"], m["L"]), lambda m: imp(m["L"], m["G"])], {
    "A": lambda m: imp(m["G"], m["L"]), "B": lambda m: imp(not m["G"], not m["Z"]),
    "C": lambda m: imp(m["R"], m["Z"]), "D": lambda m: imp(not m["L"], not m["G"])}, "B")
n = ["Y", "J", "L", "H", "S", "G"]  # 一流湾区 规则衔接 要素流动 硬联通 软联通 产业格局
entail("1-2-3", n, [lambda m: imp(m["Y"], m["J"]), lambda m: imp(m["L"], m["H"] and m["S"]),
                    lambda m: imp(m["G"], m["L"])], {
    "A": lambda m: imp(m["S"], m["L"]), "B": lambda m: imp(not m["H"], not m["G"]),
    "C": lambda m: imp(m["J"], m["Y"]), "D": lambda m: imp(m["L"], m["G"])}, "B")
n = ["X", "C", "L", "G", "D"]  # 新型电力系统 新型储能 绿色转型(重要支撑,无条件) 规模化 降成本
entail("1-2-4", n, [lambda m: imp(m["X"], m["C"]), lambda m: imp(m["G"], m["D"])], {
    "A": lambda m: imp(not m["C"], not m["L"]), "B": lambda m: imp(m["D"], m["G"]),
    "C": lambda m: imp(m["C"], m["X"]), "D": lambda m: imp(not m["D"], not m["G"])}, "D")
n = ["W", "S", "M", "R", "B"]  # 一网通办 数据共享 满意 线上线下融合 帮办代办(描述)
entail("1-2-5", n, [lambda m: imp(m["W"], m["S"]), lambda m: imp(m["M"], m["R"])], {
    "A": lambda m: imp(m["S"], m["W"]), "B": lambda m: imp(not m["R"], not m["M"]),
    "C": lambda m: imp(m["M"], m["B"]), "D": lambda m: imp(m["R"], m["M"])}, "B")

# 1-3 考法四
n = ["P", "N", "S", "C"]  # 特色产业 留住年轻人 保住生源 撤并
entail("1-3-1", n, [lambda m: imp(not m["P"], not m["N"]), lambda m: imp(m["S"], m["N"]),
                    lambda m: imp(not m["S"], m["C"])], {
    "A": lambda m: imp(m["P"], not m["C"]), "B": lambda m: imp(not m["C"], m["P"]),
    "C": lambda m: imp(m["C"], not m["P"]), "D": lambda m: imp(m["N"], m["S"])}, "B")
n = ["J", "Y", "B", "D"]  # 甲乙丙丁
possible("1-3-2", n, [lambda m: imp(not m["J"], m["Y"]), lambda m: imp(m["Y"], m["B"]),
                      lambda m: not (m["B"] and m["D"])], {
    "A": lambda m: not m["J"] and not m["Y"], "B": lambda m: m["D"] and not m["J"],
    "C": lambda m: m["Y"] and m["D"], "D": lambda m: m["J"] and m["D"] and not m["Y"]}, "D")
n = ["B", "C", "E", "Y"]  # 北方市场 冷链 错峰 预冷
entail("1-3-3", n, [lambda m: imp(m["B"], m["C"]), lambda m: imp(m["E"], m["C"]), lambda m: imp(m["C"], m["Y"])], {
    "A": lambda m: imp(not m["E"], not m["B"]), "B": lambda m: imp(m["B"], m["Y"]),
    "C": lambda m: imp(m["Y"], m["E"]), "D": lambda m: imp(m["C"], m["B"])}, "B")
n = ["J", "Y", "B", "D", "W"]  # 甲乙丙丁戊；附加"甲参加"
entail("1-3-4", n, [lambda m: imp(m["J"], m["Y"]), lambda m: imp(m["Y"], not m["B"]),
                    lambda m: imp(m["D"], m["B"]), lambda m: m["D"] or m["W"], lambda m: m["J"]], {
    "A": lambda m: m["B"] and m["D"], "B": lambda m: m["Y"] and not m["D"] and m["W"],
    "C": lambda m: not m["Y"] and not m["B"], "D": lambda m: not m["W"]}, "B")
n = ["Bi", "Bu", "Dl"]  # 创新标杆 研发补贴 瞪羚计划；事实：没入选瞪羚
entail("1-3-5", n, [lambda m: imp(m["Bi"], m["Bu"]), lambda m: imp(m["Dl"], m["Bi"]),
                    lambda m: imp(m["Bu"], m["Dl"]), lambda m: not m["Dl"]], {
    "A": lambda m: m["Bi"] and not m["Bu"], "B": lambda m: not m["Bi"] and not m["Bu"],
    "C": lambda m: m["Bu"], "D": lambda m: m["Bi"]}, "B")

# 1-4 考法五
n = ["Z", "C", "L", "W"]  # 老周 小陈 小林 小吴
entail("1-4-1", n, [lambda m: imp(m["Z"], m["C"] and m["L"]), lambda m: imp(m["L"], m["W"]), lambda m: not m["W"]], {
    "A": lambda m: not m["Z"] and not m["C"], "B": lambda m: not m["Z"],
    "C": lambda m: m["C"], "D": lambda m: m["Z"] and not m["C"]}, "B")
n = ["D", "C", "P", "Z", "J"]  # 研发达标 初审 专家评审 知识产权证明 检测报告
entail("1-4-2", n, [lambda m: imp(not m["D"], not m["C"]), lambda m: imp(m["P"], m["C"]),
                    lambda m: imp(m["P"], m["Z"] or m["J"]), lambda m: m["P"]], {
    "A": lambda m: m["D"] and (m["Z"] or m["J"]), "B": lambda m: m["D"] and m["Z"] and m["J"],
    "C": lambda m: m["J"], "D": lambda m: m["D"] and not m["Z"]}, "A")
n = ["S", "Q", "F", "T", "J"]  # 按期上线 查询空位 无感支付 调整流程 数据接入
entail("1-4-3", n, [lambda m: imp(m["S"], m["Q"] and m["F"]), lambda m: imp(m["Q"], m["J"]),
                    lambda m: imp(m["F"], m["T"]), lambda m: not m["J"]], {
    "A": lambda m: not m["S"], "B": lambda m: not m["T"], "C": lambda m: not m["F"],
    "D": lambda m: m["S"] and not m["Q"]}, "A")
n = ["M", "Z", "Q"]  # 糖水卖完 喝早茶 放晴
entail("1-4-4", n, [lambda m: imp(m["M"], m["Z"]), lambda m: imp(m["M"], m["Q"]), lambda m: not m["Z"]], {
    "A": lambda m: not m["Q"], "B": lambda m: not m["M"],
    "C": lambda m: m["Q"] and not m["M"], "D": lambda m: m["M"] and not m["Q"]}, "B")

# 1-5 考法三
n = ["M", "S", "T"]  # 获评最美 社区志愿者 参加培训
impossible("1-5-1", n, [lambda m: imp(m["M"] and m["S"], m["T"])], {
    "A": lambda m: m["S"] and m["T"] and not m["M"], "B": lambda m: m["M"] and not m["T"] and not m["S"],
    "C": lambda m: m["S"] and m["M"] and not m["T"], "D": lambda m: not m["T"] and not m["S"] and m["M"]}, "C")
n = ["B", "Z", "J"]  # 报名 中级职称 5年经历
combo("1-5-2", n, [lambda m: imp(m["B"], m["Z"] or m["J"])], {
    1: lambda m: imp(m["B"], m["Z"]), 2: lambda m: imp(not m["Z"] and not m["J"], not m["B"]),
    3: lambda m: imp(m["J"], m["B"]), 4: lambda m: imp(m["B"] and not m["Z"], m["J"])},
    {"A": {1, 2}, "B": {2, 4}, "C": {2, 3}, "D": {3, 4}}, "B")
n = ["K", "Y", "D", "S"]  # 控制客流 分时预约 拥堵 安全事故
entail("1-5-3", n, [lambda m: imp(not m["K"] and not m["Y"], m["D"] or m["S"])], {
    "A": lambda m: imp(not m["D"] and not m["S"], m["K"]),
    "B": lambda m: imp(not m["D"] and not m["S"], m["K"] or m["Y"]),
    "C": lambda m: imp(m["Y"], not m["D"]), "D": lambda m: imp(m["D"], not m["K"] and not m["Y"])}, "B")
n = ["Z", "X", "D", "Y", "S"]  # 省重点 专项债 督导 月报 审计
notentail("1-5-4", n, [lambda m: imp(m["Z"] or m["X"], m["D"]), lambda m: imp(m["D"], m["Y"] and m["S"])], {
    "A": lambda m: imp(m["X"], m["Y"]), "B": lambda m: imp(not m["S"], not m["Z"]),
    "C": lambda m: imp(not m["Y"], not m["Z"] and not m["X"]), "D": lambda m: imp(m["D"], xor(m["Z"], m["X"]))}, "D")
n = ["J", "Y", "B", "D"]  # 甲乙丙丁社区
entail("1-5-5", n, [lambda m: not (m["J"] and m["Y"]), lambda m: m["Y"] + m["B"] + m["D"] >= 2,
                    lambda m: imp(m["D"], m["J"]), lambda m: not m["Y"]], {
    "A": lambda m: m["J"] and m["B"] and m["D"], "B": lambda m: m["B"] and m["D"] and not m["J"],
    "C": lambda m: not m["J"] and not m["Y"], "D": lambda m: xor(m["B"], m["D"])}, "A")

# 1-6 考法十
n = ["G", "Z", "Y"]  # 地下停车场 充电桩 预留条件
violation("1-6-1", n, lambda m: imp(m["G"], m["Z"] or m["Y"]), {
    1: lambda m: m["G"] and not m["Z"] and m["Y"], 2: lambda m: m["G"] and not m["Z"] and not m["Y"],
    3: lambda m: not m["G"] and not m["Z"]}, {"A": {2}, "B": {1, 2}, "C": {2, 3}, "D": {1, 2, 3}}, "A")
n = ["K", "C", "H", "D"]  # 开平碉楼 赤坎古镇 海宴镇 川岛；三条建议都没采纳
entail("1-6-2", n, [lambda m: not imp(m["K"], not m["C"]), lambda m: not imp(m["D"], m["H"]),
                    lambda m: not imp(m["C"], m["H"])], {
    "A": lambda m: m["K"] and m["C"] and m["D"] and not m["H"],
    "B": lambda m: m["K"] and m["C"] and not m["D"] and not m["H"],
    "C": lambda m: m["C"] and m["H"] and m["D"] and not m["K"],
    "D": lambda m: m["K"] and m["C"] and m["H"] and m["D"]}, "A")
pr = ["Ye", "Ni"]   # 年轻人 选择夜间消费；"只有年轻人才会选择夜间消费"为假 ⇔ 有的夜消费者不是年轻人
st = {"A": ("E", lambda t: t["Ye"] and not t["Ni"]), "B": ("E", lambda t: (not t["Ye"]) and t["Ni"]),
      "C": None, "D": ("E", lambda t: t["Ye"] and not t["Ni"])}
# 能证明原断定为假 = 该选项为真时，原断定(所有夜消费者都是年轻人)不可能为真
def refutes(o):
    if o is None: return False   # C"大多数是年轻人"与原断定相容
    return not cok(pr, [lambda t: imp(t["Ni"], t["Ye"])], [o[1]])
check("1-6-3", {k: refutes(o) for k, o in st.items()}, "B")

# 1-7 考法十二（模态）
wcon = lambda w: imp(w["Y"], w["S"])   # 一年内完成 ⇒ 三年内完成
P = [lambda M: BOX(M, lambda w: not w["Y"]), lambda M: DIA(M, lambda w: w["S"])]
k_entail("1-7-1", ["Y", "S"], [], P, {
    "A": lambda M: BOX(M, lambda w: not w["Y"]) and DIA(M, lambda w: w["S"]),
    "B": lambda M: DIA(M, lambda w: not w["Y"]) and BOX(M, lambda w: w["S"]),
    "C": lambda M: BOX(M, lambda w: not w["Y"]) and BOX(M, lambda w: not w["S"]),
    "D": lambda M: DIA(M, lambda w: w["Y"]) and DIA(M, lambda w: w["S"])}, "A", wcon)
cs = ["c1", "c2", "c3"]   # 三个试点城市是否完成
P = [lambda M: not DIA(M, lambda w: all(w[c] for c in cs))]
k_entail("1-7-2", cs, [], P, {
    "A": lambda M: BOX(M, lambda w: not any(w[c] for c in cs)),
    "B": lambda M: BOX(M, lambda w: not all(w[c] for c in cs)),
    "C": lambda M: any(BOX(M, lambda w, c=c: w[c]) for c in cs),
    "D": lambda M: DIA(M, lambda w: all(w[c] for c in cs))}, "B")

# 1-8 考法七
n = ["J", "Y", "B", "D"]  # 甲乙丙丁镇
P = [lambda m: m["Y"] or m["B"], lambda m: not (m["B"] and m["D"]), lambda m: not m["Y"]]
bridge("1-8-1", n, P, {
    "A": lambda m: imp(m["J"], m["D"]), "B": lambda m: imp(not m["J"], m["D"]),
    "C": lambda m: imp(m["D"], m["J"]), "D": lambda m: imp(m["J"], not m["D"])}, lambda m: m["J"], "B")
n = ["H", "Z", "K", "F"]  # 小欣：绘本 自然观察 科学实验 非遗手作
P = [lambda m: m["H"] or m["Z"], lambda m: imp(m["H"], not m["K"]), lambda m: m["K"]]
bridge("1-8-2", n, P, {
    "A": lambda m: not m["H"], "B": lambda m: imp(m["Z"], not m["F"]),
    "C": lambda m: imp(not m["F"], m["Z"]), "D": lambda m: imp(m["F"], m["Z"])}, lambda m: not m["F"], "B")
n = ["K", "S", "Z", "P"]  # 客源 收入 付得起租金 线上平台；结论：Z→P
P = [lambda m: imp(not m["K"], not m["S"]), lambda m: imp(not m["S"], not m["Z"])]
bridge("1-8-3", n, P, {
    "A": lambda m: imp(m["P"], m["K"]), "B": lambda m: imp(m["K"], m["P"]),
    "C": lambda m: imp(m["S"], m["Z"]), "D": lambda m: True}, lambda m: imp(m["Z"], m["P"]), "B")

# =====================================================================
# 第 8 天
# =====================================================================
n = ["J", "B", "K", "Q", "Z"]  # 技能提升 标准化培训 实操考核 就业渠道 转化实效
notentail("8-1-1", n, [lambda m: imp(m["J"], m["B"] and m["K"]), lambda m: imp(m["Z"], m["Q"])], {
    "A": lambda m: imp(m["J"], m["B"]), "B": lambda m: imp(not m["Q"], not m["Z"]),
    "C": lambda m: imp(not m["K"], not m["J"]), "D": lambda m: imp(not m["B"], not m["Z"])}, "D")
n = ["X", "W", "S", "K"]  # 需求导向 问题导向 做深做实 决策科学
entail("8-1-2", n, [lambda m: imp(m["X"] and m["W"], m["S"]), lambda m: imp(m["K"], m["S"])], {
    "A": lambda m: imp(not m["S"], not m["X"]), "B": lambda m: imp(not m["S"], not m["X"] or not m["W"]),
    "C": lambda m: imp(m["K"], m["X"] and m["W"]), "D": lambda m: imp(m["S"], m["X"] and m["W"])}, "B")
n = ["D", "T", "L", "H"]  # 登高山 知天高 临深溪 知地厚
notentail("8-1-3", n, [lambda m: imp(not m["D"], not m["T"]), lambda m: imp(not m["L"], not m["H"])], {
    "A": lambda m: imp(m["T"], m["D"]), "B": lambda m: imp(not m["L"], not m["H"]),
    "C": lambda m: imp(m["H"], m["L"]), "D": lambda m: imp(m["D"], m["T"])}, "D")
n = ["Y", "P", "Z", "L", "D"]  # 走远 品牌 质量体系 冷链 电商发展
notentail("8-2-1", n, [lambda m: imp(m["Y"], m["P"]), lambda m: imp(m["P"], m["Z"])], {
    "A": lambda m: imp(not m["Z"], not m["P"]), "B": lambda m: imp(not m["P"], not m["Y"]),
    "C": lambda m: imp(m["Y"], m["Z"]), "D": lambda m: imp(not m["L"], not m["D"])}, "D")
n = ["M", "W", "X"]  # 群众满意 做到位 赢得信任
entail("8-2-2", n, [lambda m: imp(m["W"], m["M"]), lambda m: imp(m["X"], m["W"])], {
    "A": lambda m: imp(m["M"], m["X"]), "B": lambda m: imp(m["W"], m["X"]),
    "C": lambda m: imp(not m["M"], not m["X"]), "D": lambda m: imp(not m["X"], not m["W"])}, "C")
n = ["G", "Q", "Y", "M"]  # 参评社区中：获评 15分钟圈 一站式 满意度高（"一般认为"不入模）
entail("8-2-3", n, [lambda m: imp(m["G"], m["Q"] and m["Y"])], {
    "A": lambda m: imp(m["G"], m["M"]), "B": lambda m: imp(not m["Y"], not m["G"]),
    "C": lambda m: imp(m["Q"] and m["Y"], m["G"]), "D": lambda m: imp(m["M"], m["G"])}, "B")
n = ["L", "X", "M"]  # 落地 精准宣传 需求摸底
entail("8-2-4", n, [lambda m: imp(m["L"], m["X"]), lambda m: imp(m["X"], m["M"])], {
    "A": lambda m: imp(not m["M"], not m["L"]), "B": lambda m: imp(m["X"], m["L"]),
    "C": lambda m: m["L"] and not m["X"], "D": lambda m: imp(m["M"], m["X"])}, "A")
n = ["Y", "K"]  # 消防验收 开业
equiv("8-3-1", n, lambda m: imp(m["K"], m["Y"]), {
    "A": lambda m: imp(not m["Y"], not m["K"]), "B": lambda m: imp(m["Y"], m["K"]),
    "C": lambda m: imp(not m["K"], not m["Y"]), "D": lambda m: xor(m["Y"], not m["K"])}, "A")
n = ["J", "D"]  # 集训 单招
equiv("8-3-2", n, lambda m: imp(m["J"], not m["D"]), {
    "A": lambda m: imp(m["D"], not m["J"]), "B": lambda m: imp(not m["J"], m["D"]),
    "C": lambda m: xor(m["J"], m["D"]), "D": lambda m: imp(not m["D"], m["J"])}, "A")
n = ["Y", "S", "J", "G"]  # 原创 实用 获奖 收购
combo("8-4-1", n, [lambda m: imp(m["Y"] and m["S"], m["J"] or m["G"])], {
    1: lambda m: imp(not m["J"] and not m["G"], not (m["Y"] and m["S"])),
    2: lambda m: imp(m["Y"] and not m["J"], m["G"]),
    3: lambda m: imp(not m["J"] and not m["G"], not m["Y"]),
    4: lambda m: imp(m["Y"] and m["S"] and not m["J"], m["G"])},
    {"A": {1, 2}, "B": {1, 4}, "C": {2, 3}, "D": {3, 4}}, "B")
n = ["Y", "F", "J"]  # 演练 防诈 民警
entail("8-4-2", n, [lambda m: xor(m["Y"], m["F"]), lambda m: imp(m["F"], m["J"]), lambda m: not m["J"]], {
    "A": lambda m: m["Y"] and not m["F"], "B": lambda m: not m["Y"] and not m["F"],
    "C": lambda m: m["F"], "D": lambda m: m["Y"] and m["F"]}, "A")
n = ["Y", "P", "B", "D"]  # 演练 救护培训 应急包 登记
P = [lambda m: imp(m["Y"] or m["P"], m["B"] and m["D"])]
st = {"A": ent(n, P, lambda m: imp(not m["B"], not m["Y"] and not m["P"])),
      # B：没登记 → 没演练，且"可能参加了培训"——后半句要求 ¬登记∧培训 相容
      "B": ent(n, P, lambda m: imp(not m["D"], not m["Y"])) and cons(n, P + [lambda m: not m["D"] and m["P"]]),
      "C": ent(n, P, lambda m: imp(m["B"], m["Y"] or m["P"])),
      "D": ent(n, P, lambda m: imp(not m["Y"], not m["B"]))}
check("8-4-3", st, "A")
n = ["Z", "T"]  # 涨价 接团队客；要么涨价，要么不接团队客
equiv("8-4-4", n, lambda m: xor(m["Z"], not m["T"]), {
    "A": lambda m: m["Z"] or not m["T"], "B": lambda m: imp(m["T"], m["Z"]) and imp(m["Z"], m["T"]),
    "C": lambda m: imp(not m["Z"], not m["T"]), "D": lambda m: m["Z"] and not m["T"]}, "B")
n = ["Z", "R", "Y", "M", "G"]  # 政通 人和 业兴 民富 国强
combo("8-5-1", n, [lambda m: imp(m["Z"], m["R"]), lambda m: imp(m["R"], m["Y"]),
                   lambda m: imp(m["Y"], m["M"]), lambda m: imp(m["M"], m["G"])], {
    1: lambda m: imp(not m["Z"], not m["G"]), 2: lambda m: imp(m["R"], m["G"]),
    3: lambda m: imp(not m["G"], not m["Z"]), 4: lambda m: imp(m["M"], m["R"])},
    {"A": {1, 2}, "B": {2, 3}, "C": {3, 4}, "D": {2, 3, 4}}, "B")
n = ["G", "Z", "Y"]  # 管网改造 根治 影响出行
impossible("8-5-2", n, [lambda m: imp(m["Z"], m["G"]), lambda m: imp(not m["Z"], m["Y"])], {
    "A": lambda m: m["G"] and m["Y"], "B": lambda m: not m["G"] and not m["Y"],
    "C": lambda m: m["Z"] and m["Y"], "D": lambda m: not m["Z"] and m["G"]}, "B")
n = ["U", "G", "Z", "S"]  # 纳入更新 详细规划 完成征询 启动征收
entail("8-5-3", n, [lambda m: imp(m["U"], m["G"]), lambda m: imp(m["U"], m["Z"]), lambda m: imp(m["S"], m["Z"])], {
    "A": lambda m: imp(m["G"], m["Z"]), "B": lambda m: imp(not m["Z"], not m["S"] and not m["U"]),
    "C": lambda m: imp(m["S"], m["U"]), "D": lambda m: imp(m["U"], m["S"])}, "B")
n = ["S", "C", "H", "D"]  # 获批试点 处理中心 回收企业 新增用地
entail("8-5-4", n, [lambda m: imp(m["S"], m["C"] or m["H"]), lambda m: imp(m["C"], m["D"]),
                    lambda m: imp(m["H"], m["D"]), lambda m: not m["D"]], {
    "A": lambda m: not m["S"], "B": lambda m: not m["C"] and m["H"],
    "C": lambda m: m["S"] and not m["C"], "D": lambda m: m["S"] and m["D"]}, "A")
n = ["P", "K", "Y", "M"]  # 评为风情小镇 游客增多 压力加大 马拉松
entail("8-5-5", n, [lambda m: imp(m["P"], m["K"]), lambda m: imp(m["K"], m["Y"]), lambda m: imp(m["M"], not m["Y"])], {
    "A": lambda m: imp(m["P"], not m["M"]), "B": lambda m: imp(not m["M"], m["P"]),
    "C": lambda m: imp(not m["Y"], m["M"]), "D": lambda m: imp(m["M"], m["K"])}, "A")
n = ["N", "X", "G", "Z"]  # 南沙企业 芯片研发 考公 照顾父母
entail("8-6-1", n, [lambda m: imp(not m["N"], not m["X"]), lambda m: imp(not m["G"], not m["Z"]),
                    lambda m: not (m["N"] and m["G"]), lambda m: m["Z"]], {
    "A": lambda m: m["N"], "B": lambda m: not m["X"], "C": lambda m: not m["G"],
    "D": lambda m: m["G"] and m["X"]}, "B")
n = ["R", "J", "M", "K"]  # 认定成功 奖补 15㎡ 50个口袋公园
entail("8-6-2", n, [lambda m: imp(m["R"], m["J"]), lambda m: imp(m["J"], m["M"]), lambda m: imp(m["M"], m["K"]),
                    lambda m: not m["K"]], {
    "A": lambda m: not m["R"], "B": lambda m: m["M"], "C": lambda m: m["J"],
    "D": lambda m: m["J"] and not m["R"]}, "A")
n = ["W", "T", "B", "Y"]  # 引入物业 提高物业费 街道补贴 业主同意
entail("8-6-3", n, [lambda m: imp(m["W"], m["T"] or m["B"]), lambda m: not m["B"],
                    lambda m: imp(m["T"], m["Y"]), lambda m: m["W"]], {
    "A": lambda m: m["T"] and m["Y"], "B": lambda m: m["T"] and not m["Y"],
    "C": lambda m: m["B"], "D": lambda m: not m["T"]}, "A")
n = ["J", "Y", "B", "D", "W"]  # 甲乙丙丁戊
P = [lambda m: imp(m["J"], m["Y"]), lambda m: not (m["Y"] and m["B"]), lambda m: imp(m["B"], m["D"]),
     lambda m: m["W"] or m["J"]]
entail("8-6-4.1", n, P + [lambda m: m["B"]], {
    "A": lambda m: m["D"] and m["W"] and not m["J"] and not m["Y"], "B": lambda m: m["J"] and m["D"],
    "C": lambda m: m["Y"] and m["W"], "D": lambda m: m["D"] and not m["W"]}, "A")
entail("8-6-4.2", n, P + [lambda m: m["Y"]], {
    "A": lambda m: not m["B"] and (m["J"] or m["W"]), "B": lambda m: m["J"],
    "C": lambda m: not m["D"], "D": lambda m: m["W"]}, "A")

pr = ["X", "W", "Z", "Y"]  # 参加培训 提交心得 综合科 业务科
c_impossible("8-7-1", pr, [lambda t: imp(t["X"], t["W"]), lambda t: imp(t["Z"], not t["X"])],
             [lambda t: t["Y"] and not t["W"]], {
    "A": ("U", lambda t: imp(t["Y"], t["X"])), "B": ("E", lambda t: t["Z"] and t["W"]),
    "C": ("E", lambda t: t["Y"] and t["X"]), "D": ("E", lambda t: t["W"] and not t["X"])}, "A")
pr = ["V", "D", "L"]  # 志愿者 党员 楼栋长
c_entail("8-7-2", pr, [lambda t: imp(t["L"], t["D"])], [lambda t: t["V"] and not t["D"]], {
    "A": ("E", lambda t: t["L"] and not t["V"]), "B": ("E", lambda t: t["V"] and not t["L"]),
    "C": ("E", lambda t: t["D"] and not t["V"]), "D": ("U", lambda t: imp(t["V"], not t["L"]))}, "B")
pr = ["G", "F", "P", "X"]  # 公务员 辅警 普法宣讲 法律专业
c_entail("8-7-3", pr, [lambda t: imp(t["X"], t["P"])],
         [lambda t: t["G"] and not t["P"], lambda t: t["F"] and t["P"]], {
    "A": ("E", lambda t: t["G"] and not t["X"]), "B": ("E", lambda t: t["X"] and not t["G"]),
    "C": ("U", lambda t: imp(t["F"], t["P"])), "D": ("E", lambda t: t["G"] and t["X"])}, "A")
pr = ["Q", "Y", "C", "R"]  # 青年夜校 35岁以下 长者饭堂优惠 社区居民
c_impossible("8-7-4", pr, [lambda t: imp(t["Q"], t["Y"]), lambda t: imp(t["Y"], not t["C"])],
             [lambda t: t["R"] and t["C"]], {
    "A": ("E", lambda t: t["R"] and t["C"] and not t["Q"]), "B": ("E", lambda t: t["Q"] and t["C"]),
    "C": ("E", lambda t: t["R"] and not t["Y"]), "D": ("E", lambda t: t["R"] and not t["Q"])}, "B")
pr = ["K", "C", "D"]  # 创客营 创业经历 创业贷款
c_possible("8-7-5", pr, [lambda t: imp(t["K"], t["C"])], [lambda t: t["C"] and t["D"]], {
    "A": ("E", lambda t: t["K"] and not t["C"]), "B": ("U", lambda t: imp(t["D"], t["K"])),
    "C": ("U", lambda t: imp(t["C"], not t["D"])), "D": ("E", lambda t: t["K"] and not t["C"] and not t["D"])}, "B")

n = ["J", "Y", "B"]  # 甲乙丙
entail("8-8-1", n, [lambda m: imp(m["J"], m["Y"]), lambda m: imp(m["Y"], not m["B"]),
                    lambda m: imp(not m["B"], not m["J"]), lambda m: m["J"] or m["B"]], {
    "A": lambda m: m["J"], "B": lambda m: m["Y"], "C": lambda m: m["B"] and not m["J"] and not m["Y"],
    "D": lambda m: m["J"] and m["B"]}, "C")
n = ["B", "Y", "J", "Z"]  # 白云山 永庆坊 粤剧 早茶
entail("8-8-2", n, [lambda m: m["B"] or m["Y"], lambda m: imp(m["B"], m["Z"]), lambda m: imp(m["Y"], m["J"]),
                    lambda m: not (m["J"] and m["Z"])], {
    "A": lambda m: m["B"], "B": lambda m: xor(m["Z"], m["J"]), "C": lambda m: m["Z"],
    "D": lambda m: m["B"] and m["Y"]}, "B")
n = ["G", "S", "T"]  # 加大管控 失去烟火气 噪音投诉
entail("8-8-3", n, [lambda m: imp(m["G"], m["S"]), lambda m: imp(not m["G"], m["T"])], {
    "A": lambda m: xor(m["S"], m["T"]), "B": lambda m: m["S"] or m["T"], "C": lambda m: m["S"] and m["T"],
    "D": lambda m: imp(not m["S"], not m["T"])}, "B")

n = ["J", "Y", "B", "D"]  # 甲乙丙丁基地
P = [lambda m: m["J"] or m["Y"], lambda m: imp(m["Y"], not m["B"]), lambda m: not m["J"]]
bridge("8-9-1", n, P, {
    "A": lambda m: imp(m["D"], m["B"]), "B": lambda m: imp(m["B"], m["D"]),
    "C": lambda m: imp(not m["D"], m["B"]), "D": lambda m: imp(m["Y"], m["D"])}, lambda m: not m["D"], "A")
n = ["J", "B", "G", "Z"]  # 选甲镇 选丙镇 人才公寓 省级资金
P = [lambda m: imp(m["J"], m["G"]), lambda m: imp(m["G"], m["Z"]), lambda m: xor(m["J"], m["B"])]
bridge("8-9-2", n, P, {
    "A": lambda m: m["Z"], "B": lambda m: not m["Z"], "C": lambda m: m["G"], "D": lambda m: True},
    lambda m: m["B"], "B")
n = ["J", "Y", "C", "Z", "Y2"]  # 甲项目 乙项目 占用丙地块 追加预算 压减一般性支出
P = [lambda m: m["J"] or m["Y"], lambda m: imp(m["J"], m["C"]), lambda m: not m["C"], lambda m: imp(m["Y"], m["Z"])]
bridge("8-9-3", n, P, {
    "A": lambda m: imp(m["Y2"], m["Z"]), "B": lambda m: imp(not m["Y2"], not m["Z"]),
    "C": lambda m: m["Z"], "D": lambda m: imp(not m["Y"], not m["Y2"])}, lambda m: m["Y2"], "B")
n = ["Y", "R", "P"]  # 延时服务 增加人员 编制批准
P = [lambda m: imp(m["Y"], m["R"])]
S = {1: lambda m: imp(m["R"], m["P"]), 2: lambda m: not m["P"], 3: lambda m: m["R"], 4: lambda m: imp(m["P"], m["R"])}
pairs = {"A": (1, 2), "B": (2, 4), "C": (1, 3), "D": (3, 4)}
bridge("8-9-4", n, P, {k: (lambda m, a=a, b=b: S[a](m) and S[b](m)) for k, (a, b) in pairs.items()},
       lambda m: not m["Y"], "A")

# =====================================================================
# 第 15 天
# =====================================================================
k_entail("15-1-1", ["L"], [], [lambda M: not BOX(M, lambda w: w["L"])], {
    "A": lambda M: BOX(M, lambda w: not w["L"]), "B": lambda M: DIA(M, lambda w: not w["L"]),
    "C": lambda M: DIA(M, lambda w: w["L"]), "D": lambda M: not DIA(M, lambda w: w["L"])}, "B")
# 15-1-2：D=台风在珠江口登陆（现实事实），Q=航班大面积取消（随世界变化）；"如果D，那么必然Q"
k_contra("15-1-2", ["Q"], ["D"], [lambda M: imp(M["g"]["D"], BOX(M, lambda w: w["Q"]))], {
    "A": lambda M: M["g"]["D"] and DIA(M, lambda w: not w["Q"]),
    "B": lambda M: (not M["g"]["D"]) and M["w0"]["Q"],
    "C": lambda M: (not M["w0"]["Q"]) and not M["g"]["D"],
    "D": lambda M: not M["g"]["D"]}, "A")
ps = ["p1", "p2", "p3"]
k_entail("15-1-3", ps, [], [lambda M: not DIA(M, lambda w: not all(w[p] for p in ps))], {
    "A": lambda M: BOX(M, lambda w: all(w[p] for p in ps)), "B": lambda M: DIA(M, lambda w: not any(w[p] for p in ps)),
    "C": lambda M: DIA(M, lambda w: not all(w[p] for p in ps)), "D": lambda M: not BOX(M, lambda w: all(w[p] for p in ps))}, "A")
ts = ["t1", "t2", "t3"]   # 各时段是否有投诉；t3=现在
entail("15-1-4", ts, [lambda m: not all(not m[t] for t in ts)], {
    "A": lambda m: all(m[t] for t in ts), "B": lambda m: any(m[t] for t in ts),
    "C": lambda m: sum(m[t] for t in ts) >= 2, "D": lambda m: m["t3"]}, "B")

pr = ["X", "H", "D", "W"]  # 参加培训 通过考核 被调离 窗口人员
c_notentail("15-2-1", pr, [lambda t: imp(t["X"], t["H"]), lambda t: imp(t["H"], not t["D"])],
            [lambda t: t["W"] and t["D"]], {
    "A": ("E", lambda t: t["W"] and not t["X"]), "B": ("U", lambda t: imp(t["X"], not t["D"])),
    "C": ("E", lambda t: t["W"] and not t["H"]), "D": ("E", lambda t: (not t["H"]) and t["X"])}, "D")
pr = ["G", "T", "P", "S", "Q"]  # 南粤工匠 带徒 评审 高级技师 青年技师
c_impossible("15-2-2", pr, [lambda t: imp(t["G"], t["T"]), lambda t: imp(t["T"], t["P"]), lambda t: imp(t["Q"], not t["P"])],
             [lambda t: t["S"] and t["G"]], {
    "A": ("E", lambda t: t["Q"] and t["T"]), "B": ("E", lambda t: t["S"] and not t["T"]),
    "C": ("E", lambda t: t["P"] and not t["S"]), "D": ("E", lambda t: t["Q"] and t["S"])}, "A")
pr = ["Q", "B", "T", "D", "Y"]  # 全程 半马 体检 定向赛 夜跑团
c_impossible("15-2-3", pr, [lambda t: imp(t["Q"], t["B"]), lambda t: imp(t["B"], t["T"]), lambda t: imp(t["D"], not t["T"])],
             [lambda t: t["D"] and t["Y"]], {
    "A": ("E", lambda t: t["Q"] and t["D"]), "B": ("U", lambda t: imp(t["Y"], not t["T"])),
    "C": ("E", lambda t: t["Y"] and t["T"]), "D": ("E", lambda t: t["T"] and not t["Q"])}, "A")
# 15-2-4：40人，党员⊆报名⊆调研，未调研12人 ⇒ 调研28人
st = {"A": True, "B": True, "C": True, "D": True}
for r in range(0, 29):
    for p in range(0, r + 1):
        st["A"] &= p <= 28; st["B"] &= p == 28; st["C"] &= 0 >= 12; st["D"] &= r >= 28
check("15-2-4", st, "A")

n = ["Z", "L", "D"]  # 早茶节 龙舟赛 灯光节
entail("15-3-1", n, [lambda m: m["Z"] + m["L"] + m["D"] >= 2, lambda m: imp(m["D"], not m["L"])], {
    "A": lambda m: m["Z"], "B": lambda m: m["L"], "C": lambda m: m["Z"] and m["L"] and m["D"], "D": lambda m: m["D"]}, "A")
n = ["Zh", "Li", "W", "Zo"]  # 老张 老李 小王 小周
entail("15-3-2", n, [lambda m: not (m["Zh"] and m["Li"]), lambda m: m["Li"] or m["W"], lambda m: imp(m["W"], m["Zo"]),
                     lambda m: not m["Zo"]], {
    "A": lambda m: m["Li"] and not m["Zh"] and not m["W"], "B": lambda m: m["Zh"],
    "C": lambda m: m["Zh"] and m["Li"], "D": lambda m: not m["Li"]}, "A")
n = ["A", "B", "C", "D", "E"]
minmax("15-3-3", n, [lambda m: m["A"] or m["B"], lambda m: not (m["B"] and m["C"]), lambda m: imp(not m["C"], m["D"]),
                     lambda m: imp(m["A"], m["E"])], "min", {"A": 1, "B": 2, "C": 3, "D": 4}, "B")
n = ["J", "Y", "B", "D"]
entail("15-3-4", n, [lambda m: xor(m["J"], m["Y"]), lambda m: m["Y"] or m["B"], lambda m: imp(m["B"], m["D"]),
                     lambda m: not (m["J"] and m["D"])], {
    "A": lambda m: m["Y"] and not m["J"], "B": lambda m: m["B"] and m["D"], "C": lambda m: m["J"] and m["D"],
    "D": lambda m: not m["B"]}, "A")

n = ["H", "N", "X", "P", "Z", "C"]  # 回潮汕 南澳岛 小公园 南澎列岛 自驾 租到车
entail("15-4-1", n, [lambda m: imp(m["H"], m["N"] and m["X"]), lambda m: imp(m["N"] or m["P"], m["Z"]),
                     lambda m: imp(m["Z"], m["C"]), lambda m: not m["C"]], {
    "A": lambda m: m["X"] and not m["N"], "B": lambda m: not m["N"] and not m["P"],
    "C": lambda m: m["H"] and not m["N"], "D": lambda m: m["P"]}, "B")
n = ["J", "Y", "B", "D", "W"]  # 甲乙丙丁戊
entail("15-4-2", n, [lambda m: imp(m["J"], m["Y"]), lambda m: imp(m["D"], m["B"]),
                     lambda m: imp(m["Y"], not m["B"] or not m["W"]), lambda m: m["J"], lambda m: m["W"]], {
    "A": lambda m: m["Y"] and not m["B"] and not m["D"], "B": lambda m: m["B"] and not m["D"],
    "C": lambda m: m["Y"] and m["D"], "D": lambda m: m["Y"] and not m["B"] and m["D"]}, "A")
n = ["K", "W", "B", "E", "J"]  # 开设粤语课 外聘专家 本校教师 空余教室 增加经费
entail("15-4-3", n, [lambda m: imp(m["K"], m["W"] or m["B"]), lambda m: imp(m["K"], m["E"]),
                     lambda m: imp(m["W"], m["J"]), lambda m: m["K"], lambda m: not m["J"]], {
    "A": lambda m: m["B"] and m["E"], "B": lambda m: m["W"], "C": lambda m: m["W"] and m["B"], "D": lambda m: not m["E"]}, "A")

n = ["A", "B", "C", "D"]  # 华侨城 欢乐港湾 大梅沙 深圳湾公园；三条建议都没采纳
entail("15-5-1", n, [lambda m: not imp(m["A"], not m["B"]), lambda m: not imp(m["A"], m["C"]),
                     lambda m: not (not (m["B"] and m["D"]))], {
    "A": lambda m: m["A"] and m["B"] and m["D"] and not m["C"], "B": lambda m: m["A"] and m["B"] and m["C"] and not m["D"],
    "C": lambda m: m["A"] and m["C"] and m["D"] and not m["B"], "D": lambda m: m["B"] and m["D"] and not m["A"] and not m["C"]}, "A")
n = ["Z", "J", "R", "M"]  # 健康证 食品经营 燃气 灭火器
violation("15-5-2", n, lambda m: imp(m["J"], m["Z"]) and imp(m["J"] and m["R"], m["M"]), {
    1: lambda m: m["Z"] and m["J"] and m["R"] and m["M"], 2: lambda m: not m["Z"] and not m["J"],
    3: lambda m: m["Z"] and m["J"] and m["R"] and not m["M"], 4: lambda m: not m["Z"] and m["J"] and not m["R"]},
    {"A": {1, 3}, "B": {3, 4}, "C": {2, 4}, "D": {3}}, "B")
n = ["F", "Z", "J"]  # 反例城市：发展低空经济 出台政策 设立基金
entail("15-5-3", n, [lambda m: m["F"] and not xor(m["Z"], m["J"])], {
    "A": lambda m: m["F"] and ((m["Z"] and m["J"]) or (not m["Z"] and not m["J"])),
    "B": lambda m: m["F"] and not m["Z"], "C": lambda m: not m["F"] and not m["J"],
    "D": lambda m: imp(m["F"], not m["Z"] and not m["J"])}, "A")
# 15-5-4：直言等价——在所有"非空类型集合"模型上比较真值
types = ctypes(["Y", "S"])   # Y=参加夜校的年轻人 S=为了提升技能（只看Y为真的个体）
def holds(model, kind, f):
    return all(f(t) for t in model) if kind == "U" else any(f(t) for t in model)
models_c = [list(c) for r in range(1, 5) for c in itertools.combinations(types, r)]
stem = lambda M: not holds(M, "U", lambda t: imp(t["Y"], not t["S"]))
O = {"A": ("U", lambda t: imp(t["Y"], t["S"])), "B": ("E", lambda t: t["Y"] and t["S"]),
     "C": ("E", lambda t: t["Y"] and not t["S"]), "D": ("U", lambda t: imp(t["Y"], not t["S"]))}
check("15-5-4", {k: all(stem(M) == holds(M, o[0], o[1]) for M in models_c) for k, o in O.items()}, "B")

n = ["T", "J", "K", "M", "S"]  # 信用监管 减少检查 精力 满意度 招商顺利
count("15-6-1", n, [lambda m: imp(m["T"], m["J"]), lambda m: imp(m["K"], m["J"]), lambda m: imp(not m["K"], not m["M"]),
                    lambda m: imp(m["M"], m["S"])], {
    1: lambda m: imp(not m["J"], not m["M"]), 2: lambda m: imp(m["T"], m["S"]),
    3: lambda m: imp(m["M"], m["J"]), 4: lambda m: imp(not m["S"], not m["T"])},
    {"A": 1, "B": 2, "C": 3, "D": 4}, "B")
n = ["J", "Y", "B", "D", "W", "G"]  # 甲乙丙丁戊己
possible("15-6-2", n, [lambda m: imp(m["J"], m["Y"]), lambda m: imp(m["Y"], not m["B"]), lambda m: imp(not m["B"], m["D"]),
                       lambda m: imp(m["D"], not m["W"]), lambda m: m["W"] or m["G"], lambda m: m["J"]], {
    "A": lambda m: m["B"], "B": lambda m: m["W"], "C": lambda m: not m["D"],
    "D": lambda m: m["Y"] and m["D"] and m["G"] and not m["B"] and not m["W"]}, "D")
n = ["D", "S", "Z", "N"]  # 开通地铁 通勤缩短 租金上涨 年轻人租房
impossible("15-6-3", n, [lambda m: imp(m["D"], m["S"]), lambda m: imp(m["S"], m["Z"]), lambda m: imp(m["N"], not m["Z"])], {
    "A": lambda m: m["D"] and m["N"], "B": lambda m: not m["D"] and m["Z"],
    "C": lambda m: not m["Z"] and not m["N"], "D": lambda m: m["N"] and not m["S"]}, "A")

n = ["J", "Y", "B", "D"]
entail("15-7-1", n, [lambda m: imp(m["J"], m["Y"] and m["B"]), lambda m: imp(m["Y"], not m["D"]), lambda m: imp(m["B"], m["D"])], {
    "A": lambda m: not m["J"], "B": lambda m: m["Y"], "C": lambda m: m["D"], "D": lambda m: m["B"] and m["D"]}, "A")
n = ["L", "B", "S", "C", "T"]  # 长隆 白云山 沙面 陈家祠 广州塔
impossible("15-7-2", n, [lambda m: m["L"] or m["B"], lambda m: m["S"] + m["C"] + m["T"] >= 2,
                         lambda m: imp(m["L"], not m["S"] and not m["C"]), lambda m: imp(m["B"], not m["T"])], {
    "A": lambda m: m["B"] and m["S"], "B": lambda m: m["C"] and not m["T"], "C": lambda m: m["L"],
    "D": lambda m: sum(m.values()) == 3}, "C")
n = ["J", "Y", "B", "D", "W", "G", "K"]  # 甲乙丙丁戊己庚
entail("15-7-3", n, [lambda m: not (m["W"] and m["G"]), lambda m: m["W"] + m["G"] + m["K"] >= 2,
                     lambda m: imp(m["K"], not m["J"]), lambda m: imp(not m["J"], m["Y"] and m["B"]),
                     lambda m: imp(m["B"], not m["D"])], {
    "A": lambda m: m["Y"] and m["B"] and m["K"] and not m["J"] and not m["D"], "B": lambda m: m["J"],
    "C": lambda m: m["W"] and m["G"], "D": lambda m: m["D"]}, "A")
n = ["J", "Y", "B", "D", "W"]
entail("15-7-4", n, [lambda m: imp(m["J"], m["Y"] or m["B"]), lambda m: imp(m["Y"], m["D"]), lambda m: imp(m["B"], m["D"]),
                     lambda m: imp(m["D"], not m["J"]), lambda m: m["J"] or m["W"]], {
    "A": lambda m: not m["J"] and m["W"], "B": lambda m: m["D"], "C": lambda m: not m["Y"] and not m["B"],
    "D": lambda m: m["J"]}, "A")
n = ["A", "B", "C", "D", "E", "F"]
minmax("15-7-5", n, [lambda m: not (m["A"] and m["B"]), lambda m: imp(m["C"], not m["D"]), lambda m: imp(m["E"], m["A"]),
                     lambda m: imp(m["F"], m["B"]), lambda m: m["D"] or m["E"]], "max", {"A": 2, "B": 3, "C": 4, "D": 5}, "B")
n = ["Y", "C", "D"]  # 引进车企 产业园 新增用地
entail("15-7-6", n, [lambda m: imp(m["Y"], m["C"]), lambda m: imp(m["Y"], m["D"]), lambda m: (not m["C"]) or (not m["D"])], {
    "A": lambda m: not m["Y"], "B": lambda m: not m["C"], "C": lambda m: not m["D"], "D": lambda m: not m["C"] and not m["D"]}, "A")
n = ["F", "L", "H", "P", "W"]  # 凤凰单丛 六堡茶 英德红茶 普洱 白茶；附加：买了六堡茶
entail("15-7-7", n, [lambda m: not (m["F"] and m["L"]), lambda m: m["H"] + m["P"] + m["W"] >= 2,
                     lambda m: imp(m["W"], not m["H"]), lambda m: imp(not m["F"], m["P"]), lambda m: m["L"]], {
    "A": lambda m: m["P"] and xor(m["H"], m["W"]), "B": lambda m: m["P"] and m["W"], "C": lambda m: m["H"],
    "D": lambda m: m["F"]}, "A")
n = ["J", "Y", "B", "D"]
c = len(list(models(n, [lambda m: m["J"] or m["Y"], lambda m: imp(m["J"], not m["B"]), lambda m: imp(m["Y"], m["B"])])))
check("15-7-8", {k: c == v for k, v in {"A": 2, "B": 3, "C": 4, "D": 6}.items()}, "C", "方案数=%d" % c)

n = ["Y", "G", "X", "L"]  # 小罗：粤语入门 工夫茶 醒狮 凉茶
bridge("15-8-1", n, [lambda m: xor(m["Y"], m["G"]), lambda m: imp(m["Y"], not m["X"]), lambda m: m["X"]], {
    "A": lambda m: imp(m["G"], not m["L"]), "B": lambda m: imp(not m["L"], m["G"]),
    "C": lambda m: not m["Y"], "D": lambda m: imp(m["L"], m["X"])}, lambda m: not m["L"], "A")
# 15-8-2：五个展柜一一对应
items = ["G", "D", "C", "S", "Y"]   # 广彩 端砚 潮绣 石湾陶 英石
def ok1528(c):
    return imp(c[1] == "D", c[2] != "C") and (c[3] == "D" or c[1] == "D") and \
           imp(c[2] != "C", c[4] == "S") and imp(c[5] == "Y", c[4] != "S")
sols = [dict(zip([1, 2, 3, 4, 5], p)) for p in itertools.permutations(items) if ok1528(dict(zip([1, 2, 3, 4, 5], p)))]
O = {"A": lambda c: c[1] == "D", "B": lambda c: c[3] == "D", "C": lambda c: c[5] == "Y", "D": lambda c: c[2] != "G"}
check("15-8-2", {k: any(f(c) for c in sols) and all(c[2] == "C" for c in sols if f(c)) for k, f in O.items()}, "C")
n = ["J", "Y", "B", "D"]
bridge_fail("15-8-3", n, [lambda m: imp(m["J"], m["Y"]), lambda m: imp(m["Y"], m["B"]), lambda m: imp(m["D"], not m["B"])], {
    "A": lambda m: m["D"], "B": lambda m: not m["B"], "C": lambda m: not m["Y"], "D": lambda m: m["B"]},
    lambda m: not m["J"], "D")
n = ["Y", "C", "J", "S", "D"]  # 夜经济 城管 交警 促销 灯光秀
bridge("15-8-4", n, [lambda m: imp(m["Y"], m["C"] and m["J"]), lambda m: not m["C"], lambda m: m["S"] or m["Y"]], {
    "A": lambda m: imp(m["S"], m["D"]), "B": lambda m: imp(m["D"], m["S"]),
    "C": lambda m: imp(not m["D"], m["S"]), "D": lambda m: imp(not m["S"], m["D"])}, lambda m: m["D"], "A")
n = ["S", "G", "K", "T"]  # 收储 挂牌 开工 调整
bridge("15-8-5", n, [lambda m: imp(m["G"], m["S"]), lambda m: imp(not m["G"], not m["K"]), lambda m: xor(m["K"], m["T"])], {
    "A": lambda m: not m["S"], "B": lambda m: m["S"], "C": lambda m: m["G"], "D": lambda m: m["K"]}, lambda m: m["T"], "A")
pr = ["Q", "T", "Z", "Dy"]  # 集训 体测 主力 队员
c_bridge("15-8-6", pr, [lambda t: imp(t["Q"], t["T"])], [lambda t: t["Dy"] and not t["T"]], {
    "A": ("U", lambda t: imp(t["Z"], t["Q"])), "B": ("U", lambda t: imp(t["Q"], t["Z"])),
    "C": ("E", lambda t: t["Z"] and not t["T"]), "D": ("U", lambda t: imp(not t["T"], t["Q"]))},
    ("E", lambda t: t["Dy"] and not t["Z"]), "A")
n = ["J", "Y", "B", "D"]
impossible("15-8-7", n, [lambda m: imp(m["J"], m["Y"]), lambda m: imp(m["Y"], not m["B"]), lambda m: m["B"] or m["D"]], {
    "A": lambda m: m["J"] and m["B"], "B": lambda m: m["J"] and m["D"], "C": lambda m: m["Y"] and m["D"],
    "D": lambda m: m["B"] and m["D"]}, "A")
n = ["J", "Y", "B", "D"]  # 甲乙丙丁馆
P = [lambda m: not (m["J"] and m["Y"]), lambda m: m["Y"] or m["B"], lambda m: m["J"]]
S = {1: lambda m: imp(not m["D"], not m["B"]), 2: lambda m: imp(m["B"], m["D"]), 3: lambda m: not (m["B"] and m["D"]),
     4: lambda m: imp(m["B"], m["D"]), 5: lambda m: imp(m["D"], m["B"])}
c = sum(1 for f in S.values() if cons(n, P + [f]) and ent(n, P + [f], lambda m: m["D"]))
check("15-8-8", {k: c == v for k, v in {"A": 2, "B": 3, "C": 4, "D": 5}.items()}, "B", "可得出结论的项数=%d" % c)

# =====================================================================
# 第 21 天
# =====================================================================
n = ["G", "Z", "K", "T", "C"]  # 改善 绿色转型 科技支撑 投入多 成果多（"通常"不入模）
entail("21-1-1", n, [lambda m: imp(m["G"], m["Z"]), lambda m: imp(m["Z"], m["K"])], {
    "A": lambda m: imp(not m["K"], not m["G"]), "B": lambda m: imp(m["T"], m["G"]),
    "C": lambda m: imp(m["Z"], m["G"]), "D": lambda m: imp(m["T"], m["C"])}, "A")
n = ["W", "H", "S", "F"]  # 稳粮 红线 收益 社会化服务
entail("21-1-2", n, [lambda m: imp(m["W"], m["H"] and m["S"]), lambda m: imp(m["S"], m["F"])], {
    "A": lambda m: imp(m["H"] and m["S"], m["W"]), "B": lambda m: imp(not m["F"], not m["W"]),
    "C": lambda m: imp(m["H"], m["S"]), "D": lambda m: imp(not m["W"], not m["H"])}, "B")
n = ["L", "D", "G"]  # 落地 打通 获得感；"进而"两种读法都要只剩 A
O = {"A": lambda m: imp(not m["D"], not m["L"]), "B": lambda m: imp(m["D"], m["G"]),
     "C": lambda m: imp(not m["L"], not m["D"]), "D": lambda m: imp(m["D"], m["L"])}
entail("21-1-3(读法1:G→D)", n, [lambda m: imp(m["L"], m["D"]), lambda m: imp(m["G"], m["D"])], O, "A")
entail("21-1-3(读法2:L→G)", n, [lambda m: imp(m["L"], m["D"]), lambda m: imp(m["L"], m["G"])], O, "A")

ps = ["p1", "p2", "p3"]
k_entail("21-2-1", ps, [], [lambda M: not BOX(M, lambda w: all(w[p] for p in ps))], {
    "A": lambda M: DIA(M, lambda w: not any(w[p] for p in ps)), "B": lambda M: DIA(M, lambda w: not all(w[p] for p in ps)),
    "C": lambda M: any(BOX(M, lambda w, p=p: not w[p]) for p in ps),
    "D": lambda M: all(BOX(M, lambda w, p=p: not w[p]) for p in ps)}, "B")
k_entail("21-2-2", ["B", "C"], [], [lambda M: BOX(M, lambda w: imp(not w["B"], not w["C"]))], {
    "A": lambda M: imp(M["w0"]["C"], M["w0"]["B"]), "B": lambda M: imp(M["w0"]["B"], DIA(M, lambda w: w["C"])),
    "C": lambda M: DIA(M, lambda w: (not w["B"]) and w["C"]), "D": lambda M: imp(not M["w0"]["C"], not M["w0"]["B"])}, "A")
k_entail("21-2-3", ts, [], [lambda M: not DIA(M, lambda w: all(w[t] for t in ts))], {
    "A": lambda M: not any(M["w0"][t] for t in ts), "B": lambda M: BOX(M, lambda w: not all(w[t] for t in ts)),
    "C": lambda M: DIA(M, lambda w: all(w[t] for t in ts)), "D": lambda M: any(M["w0"][t] for t in ts)}, "B")

ws = ["w1", "w2", "w3"]
entail("21-3-1", ws, [lambda m: not all(m[w] for w in ws)], {
    "A": lambda m: not any(m[w] for w in ws), "B": lambda m: any(m[w] for w in ws),
    "C": lambda m: not all(m[w] for w in ws), "D": lambda m: not m["w1"]}, "C")
# 21-3-2：比较两句话的真假组合
dom = [dict(zip(ws, v)) for v in itertools.product([False, True], repeat=3)]
prof = lambda f1, f2: {(f1(m), f2(m)) for m in dom}
stem = prof(lambda m: any(m.values()), lambda m: not all(m.values()))
optp = {"A": prof(lambda m: all(m.values()), lambda m: not any(m.values())),
        "B": prof(lambda m: all(m.values()), lambda m: not all(m.values())),
        "C": pair_profile(["Y"], [], lambda M: DIA(M, lambda w: w["Y"]), lambda M: DIA(M, lambda w: not w["Y"])),
        "D": prof(lambda m: not any(m.values()), lambda m: any(m.values()))}
check("21-3-2", {k: v == stem for k, v in optp.items()}, "C")
st = {"A": True, "B": True, "C": True, "D": True}
for x in range(7, 33):          # 60人：粤语角35、书法班32，两者都报 x 人
    st["A"] &= x >= 7; st["B"] &= x == 7; st["C"] &= (x - 7) >= 7; st["D"] &= x > 16
check("21-3-3", st, "A")
entail("21-3-4", ws, [lambda m: any(m[w] for w in ws)], {
    "A": lambda m: not all(m[w] for w in ws), "B": lambda m: not all(not m[w] for w in ws),
    "C": lambda m: all(m[w] for w in ws), "D": lambda m: sum(m[w] for w in ws) >= 2}, "B")
entail("21-3-5", ws, [lambda m: not all(m[w] for w in ws), lambda m: m["w1"]], {
    "A": lambda m: any(m[w] for w in ws) and not all(m[w] for w in ws), "B": lambda m: not any(m[w] for w in ws),
    "C": lambda m: not m["w2"] and not m["w3"], "D": lambda m: m["w1"] and not m["w2"] and not m["w3"]}, "A")

pr = ["G", "E", "N", "D"]  # 干部 80后 农村经历 驻镇帮扶队长
c_notentail("21-4-1", pr, [lambda t: imp(t["D"], t["N"])], [lambda t: t["G"] and t["E"], lambda t: t["E"] and not t["N"]], {
    "A": ("E", lambda t: t["E"] and not t["D"]), "B": ("E", lambda t: t["E"] and not t["N"]),
    "C": ("U", lambda t: imp(not t["N"], not t["D"])), "D": ("E", lambda t: t["G"] and not t["N"])}, "D")
pr = ["D", "P", "L", "W", "T"]  # 导游证 普通话 礼仪 外语 退役军人
c_entail("21-4-2", pr, [lambda t: imp(t["D"], t["P"]), lambda t: imp(t["P"], t["L"]), lambda t: imp(t["T"], not t["L"])],
         [lambda t: t["W"] and t["D"]], {
    "A": ("E", lambda t: t["W"] and t["L"]), "B": ("E", lambda t: t["T"] and t["D"]),
    "C": ("U", lambda t: imp(t["W"], t["P"])), "D": ("E", lambda t: t["L"] and t["T"])}, "A")
pr = ["Y", "T", "J", "L"]  # 湾区夜跑 城市徒步 纪念章 龙舟体验
c_possible("21-4-3", pr, [lambda t: imp(t["Y"], t["T"]), lambda t: imp(t["T"], t["J"])], [lambda t: t["L"] and t["Y"]], {
    "A": ("E", lambda t: t["Y"] and not t["J"]), "B": ("U", lambda t: imp(t["L"], not t["J"])),
    "C": ("U", lambda t: imp(t["J"], t["Y"])), "D": ("U", lambda t: imp(t["T"], not t["L"]))}, "C")
pr = ["W", "K", "Z", "X", "M"]  # 无废学校 课程 专职教师 新建 民办
c_entail("21-4-4", pr, [lambda t: imp(t["W"], t["K"]), lambda t: imp(t["K"], t["Z"]), lambda t: imp(t["X"], not t["Z"])],
         [lambda t: t["M"] and not t["K"]], {
    "A": ("U", lambda t: imp(t["X"], not t["W"])), "B": ("E", lambda t: t["M"] and t["Z"]),
    "C": ("E", lambda t: t["W"] and t["X"]), "D": ("U", lambda t: imp(t["M"], not t["Z"]))}, "A")
pr = ["S", "L", "Y", "X"]  # 示范县 路长制 列养率100% 粤西县
c_entail("21-4-5", pr, [lambda t: imp(t["S"], t["L"]), lambda t: imp(t["L"], t["Y"])], [lambda t: t["X"] and not t["Y"]], {
    "A": ("E", lambda t: t["X"] and not t["S"]), "B": ("E", lambda t: t["S"] and t["X"]),
    "C": ("U", lambda t: imp(t["X"], not t["L"])), "D": ("U", lambda t: imp(t["Y"], t["S"]))}, "A")
pr = ["J", "B", "F", "G"]  # 实习计划 保密协议 发布照片 港澳大学生
U = [lambda t: imp(t["J"], t["B"]), lambda t: imp(t["B"], not t["F"])]; E = [lambda t: t["G"] and t["F"]]
c_impossible("21-4-6.1", pr, U, E, {
    "A": ("E", lambda t: t["J"] and t["F"]), "B": ("E", lambda t: t["G"] and not t["B"]),
    "C": ("E", lambda t: t["B"] and not t["G"]), "D": ("E", lambda t: t["G"] and t["B"])}, "A")
c_notentail("21-4-6.2", pr, U, E, {
    "A": ("E", lambda t: t["G"] and not t["J"]), "B": ("U", lambda t: imp(t["J"], not t["F"])),
    "C": ("E", lambda t: t["G"] and not t["B"]), "D": ("E", lambda t: t["J"] and t["G"])}, "D")

pr = ["V", "H", "C"]  # 志愿者 服务超300小时 获称号
c_bridge("21-5-1", pr, [], [lambda t: t["V"] and t["H"]], {
    "A": ("U", lambda t: imp(t["H"], t["C"])), "B": ("U", lambda t: imp(t["C"], t["H"])),
    "C": ("E", lambda t: t["H"] and not t["C"]), "D": ("E", lambda t: t["C"] and not t["H"])},
    ("E", lambda t: t["V"] and t["C"]), "A")
n = ["L", "S", "Z"]  # M企业：灯塔工厂 全流程数字化 数据中台
bridge("21-5-2", n, [lambda m: imp(m["L"], m["S"]), lambda m: imp(m["S"], m["Z"])], {
    "A": lambda m: not m["Z"], "B": lambda m: True, "C": lambda m: imp(m["Z"], m["S"]), "D": lambda m: m["S"]},
    lambda m: not m["L"], "A")
# 21-5-3：必要前提——充分前提里最弱的那个（照 2020SZS-70 的判法）
pr = ["W", "L", "H"]   # 网红打卡点 临水临崖 安全隐患
U0 = [lambda t: imp(t["L"], t["H"])]; concl = lambda t: t["W"] and t["H"]
suffA = c_exist(pr, U0, [lambda t: t["W"] and t["L"]], concl)
suffB = c_exist(pr, U0 + [lambda t: imp(t["W"], t["L"])], [lambda t: t["W"]], concl)
suffC = cok(pr, U0, [lambda t: t["H"] and t["L"]]) and c_exist(pr, U0, [lambda t: t["H"] and t["L"]], concl)
B_implies_A = c_exist(pr, [lambda t: imp(t["W"], t["L"])], [lambda t: t["W"]], lambda t: t["W"] and t["L"])
check("21-5-3", {"A": suffA, "B": suffB and not B_implies_A, "C": suffC, "D": False}, "A", "B充分但蕴含A")
pr = ["S", "T", "Y"]   # 社区食堂 24小时 夜宵
c_bridge("21-5-4", pr, [], [lambda t: t["S"] and not t["T"]], {
    "A": ("U", lambda t: imp(t["Y"], t["T"])), "B": ("U", lambda t: imp(t["T"], t["Y"])),
    "C": ("E", lambda t: (not t["T"]) and not t["Y"]), "D": ("E", lambda t: t["Y"] and not t["S"])},
    ("E", lambda t: t["S"] and not t["Y"]), "A")
n = ["G", "Z"]  # 该社区：获评五星 专职社工
bridge("21-5-5", n, [lambda m: not m["Z"]], {
    "A": lambda m: imp(m["G"], m["Z"]), "B": lambda m: imp(m["Z"], m["G"]), "C": lambda m: True,
    "D": lambda m: imp(m["Z"], m["G"])}, lambda m: not m["G"], "A")

n = ["Z", "H"]  # 增加班次 缓解
violation("21-6-1", n, lambda m: imp(m["Z"], m["H"]), {
    1: lambda m: m["Z"] and not m["H"], 2: lambda m: not m["Z"] and m["H"], 3: lambda m: not m["Z"] and not m["H"],
    4: lambda m: m["H"]}, {"A": {1}, "B": {2}, "C": {3}, "D": {4}}, "A")
pr = ["R", "S", "J"]  # 入选 硕士 50万经费
c_entail("21-6-2", pr, [lambda t: imp(t["R"], t["J"])], [lambda t: t["R"] and not t["S"]], {
    "A": ("E", lambda t: (not t["S"]) and t["J"]), "B": ("U", lambda t: imp(t["S"], t["R"])),
    "C": ("E", lambda t: t["S"] and not t["R"]), "D": ("E", lambda t: t["J"] and not t["R"])}, "A")
n = ["L", "G"]  # 修路 文化广场；"要么…要么"
impossible("21-6-3", n, [lambda m: xor(m["L"], m["G"])], {
    "A": lambda m: m["L"] and m["G"], "B": lambda m: m["L"] and not m["G"], "C": lambda m: not m["L"] and m["G"],
    "D": lambda m: m["L"] or m["G"]}, "A")

n = ["J", "Y", "B", "W"]  # 甲乙丙戊
entail("21-7-1", n, [lambda m: m["J"] + m["Y"] + m["B"] >= 2, lambda m: imp(m["J"] or m["Y"], m["W"]),
                     lambda m: imp(m["W"], not m["B"])], {
    "A": lambda m: m["J"] and m["Y"] and m["W"] and not m["B"], "B": lambda m: m["B"],
    "C": lambda m: m["J"] and m["Y"] and not m["B"] and not m["W"], "D": lambda m: not m["W"]}, "A")
n = ["E", "G", "Z", "F"]  # 电梯 绿地 座椅 维修资金
entail("21-7-2", n, [lambda m: imp(m["E"], m["G"]), lambda m: imp(not m["E"], m["Z"]), lambda m: imp(m["G"] or m["Z"], m["F"])], {
    "A": lambda m: m["F"], "B": lambda m: m["E"], "C": lambda m: m["Z"], "D": lambda m: not m["G"]}, "A")
n = ["J", "Y", "B", "D", "W"]
entail("21-7-3", n, [lambda m: imp(m["J"], m["Y"]), lambda m: imp(m["Y"], m["B"] and m["D"]), lambda m: imp(m["D"], not m["W"]),
                     lambda m: imp(not m["J"], m["W"]), lambda m: not (m["B"] and m["W"])], {
    "A": lambda m: xor(m["J"], m["W"]), "B": lambda m: m["J"], "C": lambda m: m["D"], "D": lambda m: m["Y"] and m["W"]}, "A")
n = ["K", "H", "T", "S"]  # 扩建码头 新建航道 填海 疏浚
entail("21-7-4", n, [lambda m: imp(m["K"], m["T"]), lambda m: imp(m["H"], m["S"]), lambda m: not (m["T"] and m["S"])], {
    "A": lambda m: not (m["K"] and m["H"]), "B": lambda m: not m["K"], "C": lambda m: xor(m["K"], m["H"]),
    "D": lambda m: not m["K"] and not m["H"]}, "A")
n = ["A", "B", "C", "D", "E", "F", "G"]
minmax("21-7-5", n, [lambda m: m["A"] or m["B"], lambda m: imp(m["A"], m["C"] and m["D"]), lambda m: imp(m["B"], m["E"]),
                     lambda m: not (m["C"] and m["E"]), lambda m: imp(m["D"], m["F"])], "min", {"A": 1, "B": 2, "C": 3, "D": 4}, "B")

n = ["A", "B", "C", "D"]
bridge("21-8-1", n, [lambda m: m["A"] or m["B"], lambda m: imp(m["B"], m["C"]), lambda m: not m["A"]], {
    "A": lambda m: imp(m["D"], not m["C"]), "B": lambda m: imp(not m["C"], m["D"]),
    "C": lambda m: imp(not m["D"], m["C"]), "D": lambda m: imp(m["D"], m["C"])}, lambda m: not m["D"], "A")
n = ["P", "L", "J", "Y"]  # 配套 龙头 集群 园区
bridge("21-8-2", n, [lambda m: imp(not m["P"], not m["L"]), lambda m: imp(not m["L"], not m["J"])], {
    "A": lambda m: imp(m["P"], m["Y"]), "B": lambda m: imp(m["Y"], m["P"]), "C": lambda m: imp(m["L"], m["J"]),
    "D": lambda m: True}, lambda m: imp(m["J"], m["Y"]), "A")
n = ["J", "Y", "B", "D", "W"]
bridge("21-8-3", n, [lambda m: imp(m["J"], not m["Y"]), lambda m: imp(not m["Y"], m["B"]), lambda m: imp(m["B"], not m["D"]),
                     lambda m: m["D"] or m["W"]], {
    "A": lambda m: m["J"], "B": lambda m: m["Y"], "C": lambda m: m["D"], "D": lambda m: not m["B"]}, lambda m: m["W"], "A")
n = ["Q", "N", "P", "E"]  # 前海 南沙 培训 英语
bridge("21-8-4", n, [lambda m: xor(m["Q"], m["N"]), lambda m: imp(m["Q"], m["P"]), lambda m: imp(m["P"], m["E"])], {
    "A": lambda m: imp(m["E"], not m["Q"]), "B": lambda m: imp(m["N"], not m["E"]),
    "C": lambda m: imp(m["N"], m["E"]), "D": lambda m: imp(m["E"], m["P"])}, lambda m: m["N"], "A")
n = ["J", "Y", "B", "D"]
bridge("21-8-5", n, [lambda m: imp(m["B"], m["J"]), lambda m: imp(m["J"], (not m["Y"]) or m["D"]), lambda m: not m["D"]], {
    "A": lambda m: m["B"], "B": lambda m: not m["Y"], "C": lambda m: not m["D"], "D": lambda m: imp(not m["Y"], m["J"])},
    lambda m: m["J"] and not m["Y"], "A")
n = ["J", "Y", "B", "D"]
bridge("21-8-6", n, [lambda m: imp(m["J"], m["B"]), lambda m: imp(m["Y"], m["B"])], {
    "A": lambda m: m["J"] or m["Y"], "B": lambda m: imp(not m["B"], not m["J"]), "C": lambda m: m["J"] or m["D"],
    "D": lambda m: imp(m["Y"], m["B"])}, lambda m: m["B"], "A")

# =====================================================================
# 第 28 天
# =====================================================================
def unique_model(n, P):
    return len(list(models(n, P))) == 1
n = ["H", "S", "G", "Q", "H2", "S2", "G2", "Q2"]   # 业主：合法 审核 公示 抢险；H2..=泛指另一业主
R = lambda h, s, g, q: imp(h, (s and g) or q)
P = [lambda m: R(m["H"], m["S"], m["G"], m["Q"]), lambda m: R(m["H2"], m["S2"], m["G2"], m["Q2"]),
     lambda m: m["H"], lambda m: not m["Q"]]
entail("28-1-1", n, P, {
    "A": lambda m: m["S"] and m["G"], "B": lambda m: m["Q"],
    "C": lambda m: not (m["S2"] and not m["G2"] and not m["Q2"]) or m["H2"],  # "审核但未公示且非抢险，仍合法"
    "D": lambda m: m["H2"]}, "A")
n = ["L", "J", "Y", "L2", "J2", "Y2"]   # 老郑：合规 驾驶员证 运输证；L2..=泛指另一司机
P = [lambda m: imp(m["L"], m["J"] and m["Y"]), lambda m: imp(m["L2"], m["J2"] and m["Y2"]), lambda m: m["L"]]
entail("28-1-2", n, P, {
    "A": lambda m: m["J"] and m["Y"], "B": lambda m: not m["L"], "C": lambda m: imp(m["J2"] and m["Y2"], m["L2"]),
    "D": lambda m: m["Y2"]}, "A")
n = ["H", "B", "F", "T", "D", "X", "H2", "D2"]  # 合规 本科 购房 住满超12月 博士 超24月；H2,D2泛指他人
P = [lambda m: imp(m["H"], m["B"] and not m["F"] and imp(m["T"], m["D"]) and not m["X"]),
     lambda m: m["H"], lambda m: m["T"]]
entail("28-1-3", n, P, {
    "A": lambda m: m["D"], "B": lambda m: m["F"], "C": lambda m: imp(m["D2"], m["H2"]), "D": lambda m: m["X"] and m["H"]}, "A")
n = ["Y", "J", "B", "A"]  # 55岁以下 救生衣 有病 被允许；"除此之外不会拒绝"⇒充要
entail("28-1-4", n, [lambda m: iff(m["A"], m["Y"] and m["J"] and not m["B"]), lambda m: m["J"], lambda m: not m["A"]], {
    "A": lambda m: (not m["Y"]) or m["B"], "B": lambda m: m["B"], "C": lambda m: (not m["Y"]) and m["B"],
    "D": lambda m: xor(not m["Y"], m["B"])}, "A")
# 原题 2024SZ-36 若不补"除此之外不会拒绝"，四项都推不出
st = {k: ent(n, [lambda m: imp(m["A"], m["Y"] and m["J"]), lambda m: imp(m["B"], not m["A"]), lambda m: m["J"],
                 lambda m: not m["A"]], f) for k, f in {"A": lambda m: (not m["Y"]) or m["B"], "B": lambda m: m["B"],
                 "C": lambda m: (not m["Y"]) and m["B"], "D": lambda m: xor(not m["Y"], m["B"])}.items()}
check("28-1-4(对照:原题读法)", st, [], "原题严格读法无选项成立")
n = ["J", "R", "B"]  # 紧急任务 人行道停放 24小时补报
violation("28-1-5", n, lambda m: imp(m["R"] and not m["J"], False) and imp(m["R"] and m["J"], m["B"]), {
    1: lambda m: m["J"] and m["R"] and m["B"], 2: lambda m: not m["J"] and m["R"], 3: lambda m: m["J"] and m["R"] and not m["B"]},
    {"A": {2}, "B": {2, 3}, "C": {1, 3}, "D": {1, 2, 3}}, "B")

n = ["C", "L", "I", "T"]  # 来创业 留下 产业基础 跨境交通
entail("28-2-1", n, [lambda m: imp(m["C"] and m["L"], m["I"] and m["T"])], {
    "A": lambda m: imp(not m["T"], not (m["C"] and m["L"])), "B": lambda m: imp(m["I"] and m["T"], m["C"]),
    "C": lambda m: imp(m["C"], m["T"]), "D": lambda m: imp(m["I"], m["T"])}, "A")
n = ["S", "G", "Z", "L", "K"]  # 数字湾区 5G 算力 绿电 跨境流动(重要内容)
notentail("28-2-2", n, [lambda m: imp(m["S"], m["G"] and m["Z"]), lambda m: imp(m["Z"], m["L"])], {
    "A": lambda m: imp(not m["L"], not m["S"]), "B": lambda m: imp(m["S"], m["Z"]),
    "C": lambda m: imp(not m["G"], not m["S"]), "D": lambda m: imp(not m["K"], not m["S"])}, "D")
n = ["Q", "S", "X", "P", "T"]  # 制造业高质量 制造业数字化 中小企业数字化 破解障碍 公共平台
entail("28-2-3", n, [lambda m: imp(m["Q"], m["S"]), lambda m: imp(m["X"], m["P"]), lambda m: imp(m["P"], m["T"])], {
    "A": lambda m: imp(not m["T"], not m["X"]), "B": lambda m: imp(m["T"], m["Q"]),
    "C": lambda m: imp(m["S"], m["Q"]), "D": lambda m: imp(m["P"], m["X"])}, "A")
n = ["Z", "S", "R", "Y"]  # 照护需求满足 设施 人才 院校
notentail("28-2-4", n, [lambda m: imp(m["Z"], m["S"] and m["R"]), lambda m: imp(m["R"], m["Y"])], {
    "A": lambda m: imp(not m["Y"], not m["Z"]), "B": lambda m: imp(m["Z"], m["S"]),
    "C": lambda m: imp(not m["R"], not m["Z"]), "D": lambda m: imp(m["S"] and m["R"], m["Z"])}, "D")
n = ["Y", "G", "Z"]  # 老年友好型 适老化改造 助餐点
entail("28-2-5", n, [lambda m: imp(m["Y"], m["G"]), lambda m: imp(m["G"], m["Z"])], {
    "A": lambda m: imp(m["Y"], m["Z"]), "B": lambda m: imp(m["Z"], m["Y"]), "C": lambda m: (not m["G"]) and m["Y"],
    "D": lambda m: imp(m["G"], m["Y"])}, "A")

def excluded(rel):
    return {(x, y) for x in (True, False) for y in (True, False) if not rel(x, y)}
stem = excluded(lambda x, y: imp(not x, not y))       # 不入虎穴(x)，焉得虎子(y)
O = {"A": excluded(lambda x, y: imp(x, y)), "B": excluded(lambda x, y: imp(not x, not y)),
     "C": excluded(lambda x, y: not (x and y)), "D": excluded(lambda x, y: xor(x, y))}
check("28-3-1", {k: v == stem for k, v in O.items()}, "B")
n = ["R", "U"]  # 实名认证 使用App
equiv("28-3-2", n, lambda m: iff(m["R"], m["U"]), {
    "A": lambda m: iff(m["R"], m["U"]), "B": lambda m: xor(m["R"], m["U"]), "C": lambda m: m["R"] or m["U"],
    "D": lambda m: True}, "A")
n = ["W", "C"]  # 午托 学校午餐
equiv("28-3-3", n, lambda m: imp(not m["W"], not m["C"]), {
    "A": lambda m: imp(m["C"], m["W"]), "B": lambda m: imp(m["W"], m["C"]), "C": lambda m: xor(m["W"], not m["C"]),
    "D": lambda m: m["W"] or m["C"]}, "A")
stem = excluded(lambda x, y: imp(y, x))               # 除非亲自去(x)，否则办不成(y)：y→x
O = {"A": excluded(lambda x, y: imp(y, x)), "B": excluded(lambda x, y: imp(x, y)),
     "C": excluded(lambda x, y: imp(not x, y)), "D": excluded(lambda x, y: xor(x, y))}
check("28-3-4", {k: v == stem for k, v in O.items()}, "A")
k_entail("28-3-5", ["Z", "W"], [], [lambda M: not BOX(M, lambda w: imp(w["Z"], w["W"]))], {
    "A": lambda M: DIA(M, lambda w: w["Z"] and not w["W"]), "B": lambda M: DIA(M, lambda w: (not w["Z"]) and w["W"]),
    "C": lambda M: BOX(M, lambda w: imp(w["W"], w["Z"])), "D": lambda M: BOX(M, lambda w: imp(w["Z"], not w["W"]))}, "A")

n = ["X", "L", "C"]  # 诚信 立 成事
impossible("28-4-1", n, [lambda m: imp(not m["X"], not m["L"]), lambda m: imp(not m["L"], not m["C"])], {
    "A": lambda m: m["X"] and not m["C"], "B": lambda m: (not m["X"]) and m["C"], "C": lambda m: m["L"] and not m["C"],
    "D": lambda m: (not m["L"]) and not m["X"]}, "B")
n = ["D", "Y", "J", "Q", "B"]  # 产权登记 抵押 二手交易 契税 保险
combo("28-4-2", n, [lambda m: imp(m["Y"], m["D"]), lambda m: imp(m["J"], m["D"]), lambda m: imp(m["J"], m["Q"]),
                    lambda m: imp(m["Y"], m["B"])], {
    1: lambda m: imp(m["Y"], m["D"]), 2: lambda m: imp(m["J"], m["Y"]), 3: lambda m: imp(not m["D"], not m["Q"]),
    4: lambda m: imp(not m["D"], not m["Y"] and not m["J"])}, {"A": {1, 4}, "B": {1, 2}, "C": {3, 4}, "D": {1, 3, 4}}, "A")
n = ["K", "P", "Q", "J", "L", "S"]
entail("28-4-3", n, [lambda m: imp(m["K"], m["P"]), lambda m: imp(m["P"], m["Q"]), lambda m: imp(m["Q"], m["J"]),
                     lambda m: imp(m["J"], not m["L"]), lambda m: m["L"] or m["S"], lambda m: m["K"]], {
    "A": lambda m: m["S"], "B": lambda m: m["L"], "C": lambda m: not m["Q"], "D": lambda m: not m["S"]}, "A")
n = ["Y", "T", "X", "W"]  # 暴雨 台风 限流 延误
entail("28-4-4", n, [lambda m: imp(m["Y"], m["X"]), lambda m: imp(m["T"], m["X"]), lambda m: imp(m["X"], m["W"])], {
    "A": lambda m: imp(not m["W"], not m["Y"] and not m["T"]), "B": lambda m: imp(m["W"], m["Y"] or m["T"]),
    "C": lambda m: imp(m["X"], m["Y"]), "D": lambda m: imp(not m["Y"], not m["W"])}, "A")

n = ["K", "H", "Z", "G"]  # 考上 回梅州 照顾父母 在广州工作
possible("28-5-1", n, [lambda m: imp(m["K"], m["H"]), lambda m: imp(m["Z"], m["H"]), lambda m: m["H"],
                       lambda m: imp(m["G"], not m["H"])], {
    "A": lambda m: not m["H"], "B": lambda m: m["K"] and not m["Z"], "C": lambda m: m["K"] and m["G"],
    "D": lambda m: m["Z"] and not m["H"]}, "B")
n = ["J", "Y", "B", "D", "W"]
entail("28-5-2", n, [lambda m: imp(m["J"], m["Y"] and m["B"]), lambda m: imp(m["Y"], not m["D"]), lambda m: m["D"] or m["W"],
                     lambda m: not m["W"]], {
    "A": lambda m: not m["J"] and not m["Y"], "B": lambda m: m["B"], "C": lambda m: m["J"], "D": lambda m: not m["B"]}, "A")
n = ["T", "R", "Z", "G", "Q"]  # 听证 人大代表 政协委员 公示30天 提前一周
entail("28-5-3", n, [lambda m: imp(m["T"], m["R"] and m["Z"]), lambda m: imp(m["T"], m["G"]), lambda m: imp(m["R"], m["Q"]),
                     lambda m: m["G"], lambda m: not m["Q"]], {
    "A": lambda m: not m["T"], "B": lambda m: m["T"] and not m["R"], "C": lambda m: m["Z"], "D": lambda m: m["T"]}, "A")
n = ["Q", "N", "S", "Z", "C"]  # 前海 南沙 留校 租房 买车
entail("28-5-4", n, [lambda m: imp(m["Q"], m["Z"]), lambda m: imp(m["N"], m["C"]), lambda m: m["Q"] + m["N"] + m["S"] == 1,
                     lambda m: not m["Z"] and not m["C"]], {
    "A": lambda m: m["S"], "B": lambda m: m["N"], "C": lambda m: m["Q"] and not m["Z"], "D": lambda m: m["C"]}, "A")

pr = ["W", "F", "H"]  # 文明家庭 失信记录 五好家庭
c_impossible("28-6-1", pr, [lambda t: imp(t["W"], not t["F"])], [lambda t: t["H"] and t["F"]], {
    "A": ("U", lambda t: imp(t["H"], t["W"])), "B": ("E", lambda t: t["H"] and not t["W"]),
    "C": ("E", lambda t: t["W"] and t["H"]), "D": ("U", lambda t: imp(t["W"], not t["H"]))}, "A")
n = ["X1", "T1", "Y1", "X2", "T2", "Y2"]  # 小周/小吴：学员 团干部 3年以上
P = [lambda m: imp(m["X1"], m["T1"]), lambda m: imp(m["T1"], m["Y1"]), lambda m: imp(m["X2"], m["T2"]),
     lambda m: imp(m["T2"], m["Y2"]), lambda m: not m["Y1"], lambda m: m["X2"]]
entail("28-6-2", n, P, {"A": lambda m: not m["X1"] and m["Y2"], "B": lambda m: m["T1"], "C": lambda m: not m["Y2"],
                        "D": lambda m: m["X1"]}, "A")
pr = ["R", "T", "G", "Z"]  # 入驻 天使投资 港澳青年创办 租金减免
c_unknown("28-6-3", pr, [lambda t: imp(t["R"], t["T"]), lambda t: imp(t["G"], t["Z"])], [lambda t: t["T"] and t["G"]], {
    "A": ("E", lambda t: t["T"] and t["Z"]), "B": ("U", lambda t: imp(t["R"], t["T"])),
    "C": ("E", lambda t: t["R"] and t["Z"]), "D": ("E", lambda t: t["Z"] and t["T"])}, "C")
pr = ["S", "Y", "B"]  # 试点商圈 延长营业 安保
c_entail("28-6-4", pr, [lambda t: imp(t["Y"], t["B"])], [lambda t: t["S"] and not t["Y"]], {
    "A": ("E", lambda t: t["S"] and not t["B"]), "B": ("E", lambda t: t["S"] and not t["Y"]),
    "C": ("U", lambda t: imp(t["B"], t["Y"])), "D": ("E", lambda t: (not t["B"]) and t["S"])}, "B")

n = ["J", "Y", "B", "D", "W", "G"]
entail("28-7-1", n, [lambda m: m["J"] + m["Y"] + m["B"] >= 2, lambda m: imp(m["Y"] or m["B"], not m["D"] and not m["W"]),
                     lambda m: imp(m["J"] or m["D"], m["W"] and not m["G"])], {
    "A": lambda m: m["Y"] and m["B"], "B": lambda m: m["J"], "C": lambda m: not m["G"], "D": lambda m: m["W"]}, "A")
n = ["J", "Y", "B", "D", "W"]
entail("28-7-2", n, [lambda m: not (m["J"] and m["Y"]), lambda m: m["Y"] or m["B"], lambda m: imp(m["B"], m["J"] and m["D"]),
                     lambda m: imp(m["D"], m["Y"])], {
    "A": lambda m: not m["J"], "B": lambda m: not m["Y"], "C": lambda m: not m["D"], "D": lambda m: not m["W"]}, "A")
entail("28-7-3", n, [lambda m: m["J"] or m["Y"], lambda m: imp(m["J"], m["B"] and m["D"]), lambda m: imp(m["Y"], m["D"] and m["W"]),
                     lambda m: not (m["B"] and m["W"])], {
    "A": lambda m: m["D"] and sum(m.values()) == 3, "B": lambda m: m["J"], "C": lambda m: m["B"] and m["W"],
    "D": lambda m: sum(m.values()) >= 4}, "A")
n = ["J", "Y", "B", "D"]
impossible("28-7-4", n, [lambda m: imp(m["J"], m["Y"]), lambda m: imp(m["B"], not m["Y"]), lambda m: m["J"] or m["B"],
                         lambda m: imp(m["D"], m["B"])], {
    "A": lambda m: m["J"] and m["D"], "B": lambda m: m["Y"] and not m["D"], "C": lambda m: m["B"] and m["D"],
    "D": lambda m: not m["J"]}, "A")
n = ["T", "B", "Y"]  # 提价 商户不满 拥堵
entail("28-7-5", n, [lambda m: imp(m["T"], m["B"]), lambda m: imp(not m["T"], m["Y"]), lambda m: imp(m["Y"], m["B"])], {
    "A": lambda m: m["B"], "B": lambda m: m["Y"], "C": lambda m: m["T"], "D": lambda m: imp(m["B"], m["T"])}, "A")

n = ["H", "S", "W", "R", "J"]  # 小卢：海上 山地 无人机 绳索 急救
bridge("28-8-1", n, [lambda m: m["H"] or m["S"], lambda m: imp(m["H"], not m["W"]), lambda m: m["W"]], {
    "A": lambda m: not m["H"], "B": lambda m: imp(not m["R"] and not m["J"], not m["S"]),
    "C": lambda m: imp(m["R"] or m["J"], m["S"]), "D": lambda m: not m["S"]}, lambda m: m["R"] or m["J"], "B")
n = ["Y", "J", "C", "D"]  # 社区医疗 居家 床位紧张 增医生
bridge("28-8-2", n, [lambda m: imp(not m["Y"], not m["J"]), lambda m: imp(not m["J"], m["C"])], {
    "A": lambda m: imp(m["Y"], m["D"]), "B": lambda m: imp(m["D"], m["Y"]), "C": lambda m: m["J"],
    "D": lambda m: imp(m["C"], not m["D"])}, lambda m: imp(not m["C"], m["D"]), "A")
n = ["Y", "C", "K", "M", "L"]  # 小谢：粤语 潮州话 客家话 闽南语 雷州话
bridge("28-8-3", n, [lambda m: m["Y"] or m["C"], lambda m: imp(m["Y"], not m["K"]), lambda m: imp(m["C"], m["M"]), lambda m: m["K"]], {
    "A": lambda m: imp(not m["L"], not m["M"]), "B": lambda m: m["M"], "C": lambda m: imp(m["L"], m["C"]),
    "D": lambda m: imp(not m["M"], m["L"])}, lambda m: m["L"], "A")
n = ["S", "T", "J", "X", "Z"]  # 社区食堂 托育中心 架空层 闲置教室 申请资金
bridge("28-8-4", n, [lambda m: xor(m["S"], m["T"]), lambda m: imp(m["S"], m["J"]), lambda m: imp(m["T"], m["X"])], {
    "A": lambda m: imp(m["J"], m["Z"]) and imp(m["X"], m["Z"]), "B": lambda m: imp(m["T"], m["Z"]),
    "C": lambda m: imp(m["Z"], m["J"] or m["X"]), "D": lambda m: imp(m["J"], m["Z"])}, lambda m: m["Z"], "A")
pr = ["G", "T", "P", "B"]  # 网格员 退役军人 应急培训 表彰
c_bridge("28-8-5", pr, [lambda t: imp(t["T"], t["P"])], [lambda t: t["G"] and t["T"]], {
    "A": ("U", lambda t: imp(t["G"], t["B"])), "B": ("U", lambda t: imp(t["B"], t["P"])),
    "C": ("E", lambda t: t["B"] and t["G"]), "D": ("E", lambda t: t["P"] and not t["G"])},
    ("E", lambda t: t["P"] and t["B"]), "A")
n = ["K", "H", "Z", "B", "T"]  # 科学中心 海洋馆 植物园 博物馆 天文台
P = [lambda m: not (m["H"] and m["Z"]), lambda m: m["B"] or m["H"], lambda m: not m["B"]]
O = {"A": lambda m: imp(not m["K"], m["Z"]), "B": lambda m: iff(m["K"], m["T"]),
     "C": lambda m: imp(not m["K"], m["Z"]) and imp(m["K"], m["T"]), "D": lambda m: m["T"] or m["Z"]}
check("28-8-6", {k: unique_model(n, P + [f]) for k, f in O.items()}, "C")
n = ["M", "L", "T", "Y"]  # 马拉松 龙舟 体检 游泳证
bridge("28-8-7", n, [lambda m: imp(m["M"], m["T"]), lambda m: imp(m["L"], m["Y"])], {
    "A": lambda m: not m["T"], "B": lambda m: m["Y"], "C": lambda m: m["T"], "D": lambda m: imp(m["M"], m["L"])},
    lambda m: not (m["M"] and m["L"]), "A")

# =====================================================================
# 第 34 天
# =====================================================================
n = ["H", "T", "F", "G"]  # 红线内 填海 被否决 国务院审批
entail("34-1-1", n, [lambda m: imp(m["H"] and m["T"], xor(m["F"], m["G"])), lambda m: not m["F"], lambda m: not m["G"], lambda m: m["H"]], {
    "A": lambda m: not m["T"], "B": lambda m: m["T"], "C": lambda m: not m["H"], "D": lambda m: m["F"] and m["G"]}, "A")
n = ["D", "M"]  # 灯光节 美食节
entail("34-1-2", n, [lambda m: not xor(m["D"], m["M"])], {
    "A": lambda m: m["D"] and m["M"], "B": lambda m: imp(m["D"], m["M"]) and imp(not m["D"], not m["M"]),
    "C": lambda m: not m["D"] and not m["M"], "D": lambda m: xor(m["D"], m["M"])}, "B")
n = ["A", "B", "C", "D"]
entail("34-1-3", n, [lambda m: xor(m["A"], m["B"]), lambda m: m["B"] + m["C"] + m["D"] >= 2, lambda m: imp(m["C"], m["A"])], {
    "A": lambda m: m["D"], "B": lambda m: m["A"], "C": lambda m: sum(m.values()) == 2, "D": lambda m: m["B"] and m["C"]}, "A")
n = ["S", "T"]  # 安全员到场 技术员到场；"不是S就是T"：相容、不相容两种读法都只剩 A
O = {"A": lambda m: imp(not m["S"], m["T"]), "B": lambda m: imp(not m["T"], not m["S"]),
     "C": lambda m: m["S"] and m["T"], "D": lambda m: imp(m["S"], m["T"])}
entail("34-1-4(相容读法)", n, [lambda m: m["S"] or m["T"]], O, "A")
entail("34-1-4(不相容读法)", n, [lambda m: xor(m["S"], m["T"])], O, "A")

# 34-2-1：大多数种荔枝(L)、大多数开网店(W)；种荔枝者中少部分(≥1且<一半)种龙眼(Y)
tps = list(itertools.product([False, True], repeat=3))
st = {"A": True, "B": True, "C": True, "D": True}
def comps(total, k):
    if k == 1: yield (total,); return
    for i in range(total + 1):
        for rest in comps(total - i, k - 1): yield (i,) + rest
for N in range(3, 8):
    for cnt in comps(N, 8):
        L = sum(c for c, t in zip(cnt, tps) if t[0]); W = sum(c for c, t in zip(cnt, tps) if t[1])
        LY = sum(c for c, t in zip(cnt, tps) if t[0] and t[2])
        if not (2 * L > N and 2 * W > N and LY >= 1 and 2 * LY < L): continue
        LW = sum(c for c, t in zip(cnt, tps) if t[0] and t[1]); YW = sum(c for c, t in zip(cnt, tps) if t[2] and t[1])
        Ynot = sum(c for c, t in zip(cnt, tps) if t[2] and not t[0])
        st["A"] &= LW >= 1; st["B"] &= YW >= 1; st["C"] &= 2 * LW > W; st["D"] &= Ynot == 0
check("34-2-1", st, "A")
tm = ["t1", "t2", "t3"]
entail("34-2-2", tm, [lambda m: xor(all(m[t] for t in tm), any(m[t] for t in tm))], {
    "A": lambda m: any(m[t] for t in tm) and not all(m[t] for t in tm), "B": lambda m: not any(m[t] for t in tm),
    "C": lambda m: all(m[t] for t in tm), "D": lambda m: sum(m[t] for t in tm) >= 2}, "A")
entail("34-2-3", tm, [lambda m: not all(m[t] for t in tm)], {
    "A": lambda m: not any(m[t] for t in tm), "B": lambda m: not all(m[t] for t in tm), "C": lambda m: any(m[t] for t in tm),
    "D": lambda m: sum(not m[t] for t in tm) >= 2}, "B")

k_entail("34-3-1", ["f1", "f2"], ["Y"], [lambda M: imp(M["g"]["Y"], BOX(M, lambda w: w["f1"] and w["f2"]))], {
    "A": lambda M: imp(DIA(M, lambda w: not (w["f1"] and w["f2"])), not M["g"]["Y"]),
    "B": lambda M: imp(not M["g"]["Y"], DIA(M, lambda w: not w["f1"] and not w["f2"])),
    "C": lambda M: imp(M["w0"]["f1"] and M["w0"]["f2"], M["g"]["Y"]),
    "D": lambda M: M["g"]["Y"] and DIA(M, lambda w: not (w["f1"] and w["f2"]))}, "A")
ss = ["s1", "s2", "s3"]
maj_unhappy = lambda w: sum(not w[s] for s in ss) >= 2
k_entail("34-3-2", ss, [], [lambda M: BOX(M, lambda w: not all(w[s] for s in ss)), lambda M: DIA(M, lambda w: not maj_unhappy(w))], {
    "A": lambda M: BOX(M, lambda w: not all(w[s] for s in ss)) and DIA(M, lambda w: not maj_unhappy(w)),
    "B": lambda M: DIA(M, lambda w: all(w[s] for s in ss)), "C": lambda M: BOX(M, maj_unhappy),
    "D": lambda M: DIA(M, lambda w: not all(w[s] for s in ss)) and BOX(M, lambda w: not maj_unhappy(w))}, "A")
stemp = pair_profile(["P"], [], lambda M: BOX(M, lambda w: w["P"]), lambda M: BOX(M, lambda w: not w["P"]))
optp = {"A": prof(lambda m: all(m.values()), lambda m: not any(m.values())),
        "B": prof(lambda m: any(m.values()), lambda m: not all(m.values())),
        "C": pair_profile(["P"], [], lambda M: BOX(M, lambda w: w["P"]), lambda M: DIA(M, lambda w: not w["P"])),
        "D": pair_profile(["P"], [], lambda M: DIA(M, lambda w: w["P"]), lambda M: DIA(M, lambda w: not w["P"]))}
check("34-3-3", {k: v == stemp for k, v in optp.items()}, "A")

n = ["W", "J", "K", "H", "R", "C", "F"]  # 稳外贸 接单 快速交付 海外仓 柔性产线 降成本 附加值
base = [lambda m: imp(m["W"], m["J"]), lambda m: imp(m["K"], m["H"]), lambda m: imp(m["J"], m["K"] and m["R"]),
        lambda m: imp(m["R"], m["C"])]
O = {"A": lambda m: imp(m["W"], m["H"]), "B": lambda m: imp(m["R"], m["J"]), "C": lambda m: imp(m["C"], m["R"]),
     "D": lambda m: imp(m["C"], m["F"])}
entail("34-4-1(从而读法1:F→C)", n, base + [lambda m: imp(m["F"], m["C"])], O, "A")
entail("34-4-1(从而读法2:R→F)", n, base + [lambda m: imp(m["R"], m["F"])], O, "A")
n = ["T", "S", "Z", "G", "R"]  # 产业体系 做强实体 制造业转型 工业互联网 数实融合
entail("34-4-2", n, [lambda m: imp(m["T"], m["S"]), lambda m: imp(m["S"], m["Z"]), lambda m: imp(m["Z"], m["G"])], {
    "A": lambda m: imp(not m["G"], not m["T"]), "B": lambda m: imp(m["G"], m["R"]), "C": lambda m: imp(m["Z"], m["S"]),
    "D": lambda m: imp(not m["R"], not m["G"])}, "A")
n = ["U", "H", "V", "E", "P", "X"]  # 使用资金 合规 表决 紧急 事后公示 以后都免表决
entail("34-4-3", n, [lambda m: imp(m["U"] and m["H"], m["V"] or m["E"]), lambda m: imp(m["U"] and m["H"] and not m["V"], m["E"] and m["P"]),
                     lambda m: m["U"], lambda m: m["H"], lambda m: not m["V"]], {
    "A": lambda m: m["E"], "B": lambda m: m["V"], "C": lambda m: m["X"], "D": lambda m: not m["P"]}, "A")
n = ["K", "B", "S", "T", "N", "X"]  # 建口袋公园 边角地 联合审批 15日内 年内建成 就近享受
P = [lambda m: imp(m["K"], m["B"]), lambda m: imp(m["B"], m["S"]), lambda m: imp(m["N"], m["T"]), lambda m: imp(m["N"], m["X"])]
entail("34-4-4.1", n, P, {"A": lambda m: imp(not m["S"], not m["K"]), "B": lambda m: imp(m["T"], m["N"]),
                          "C": lambda m: imp(not m["X"], not m["K"]), "D": lambda m: imp(m["B"], m["K"])}, "A")
notentail("34-4-4.2", n, P, {"A": lambda m: imp(m["N"], m["T"]), "B": lambda m: imp(not m["B"], not m["K"]),
                             "C": lambda m: imp(not m["X"], not m["N"]), "D": lambda m: imp(not m["T"], not m["K"])}, "D")

n = ["G", "R", "H", "X", "F", "Z"]  # 走出去 人才 合规能力 校企 法务 熟悉规则
entail("34-5-1", n, [lambda m: imp(m["G"], m["R"] and m["H"]), lambda m: imp(m["R"], m["X"]), lambda m: imp(m["H"], m["F"] and m["Z"])], {
    "A": lambda m: imp(m["F"], m["X"]), "B": lambda m: imp(not m["Z"], not m["G"]), "C": lambda m: imp(m["X"], m["R"]),
    "D": lambda m: imp(m["F"], m["H"])}, "B")
n = ["S", "P", "C", "V", "R", "B"]  # 实施 盘活 社会资本 村级公司 风险评估 保障利益
combo("34-5-2", n, [lambda m: imp(m["S"], m["P"]), lambda m: imp(m["P"], m["C"] or m["V"]), lambda m: imp(m["C"], m["R"]),
                    lambda m: imp(m["B"], m["R"])], {
    1: lambda m: imp(m["S"], m["R"]), 2: lambda m: imp(not m["C"] and not m["V"], not m["S"]),
    3: lambda m: imp(not m["R"], not m["B"]), 4: lambda m: imp(not m["R"], not m["C"])},
    {"A": {2, 3}, "B": {2, 3, 4}, "C": {1, 3, 4}, "D": {1, 2, 3, 4}}, "B")
n = ["J", "Y", "B", "D", "W", "G"]
possible("34-5-3", n, [lambda m: imp(m["J"], m["Y"]), lambda m: not (m["Y"] and m["B"]), lambda m: imp(not m["B"], m["D"]),
                       lambda m: imp(m["D"], not m["W"]), lambda m: m["W"] or m["G"], lambda m: m["J"]], {
    "A": lambda m: m["B"], "B": lambda m: m["W"], "C": lambda m: not m["G"], "D": lambda m: m["Y"] and m["D"] and m["G"]}, "D")
n = ["A", "P", "Y", "X", "B"]  # 申报 评估 上云 安全员 补贴
count("34-5-4", n, [lambda m: imp(m["A"], m["P"]), lambda m: imp(m["P"], m["Y"]), lambda m: imp(m["Y"], m["X"]),
                    lambda m: imp(not m["X"], not m["B"])], {
    1: lambda m: imp(m["A"], m["X"]), 2: lambda m: imp(m["B"], m["A"]), 3: lambda m: imp(not m["Y"], not m["A"]),
    4: lambda m: imp(m["B"], m["Y"]), 5: lambda m: imp(not m["X"], not m["P"])}, {"A": 2, "B": 3, "C": 4, "D": 5}, "B")
n = ["Z", "R", "Y", "M"]  # 政通 人和 业兴 民富（环）
combo("34-5-5", n, [lambda m: imp(m["Z"], m["R"]), lambda m: imp(m["R"], m["Y"]), lambda m: imp(m["Y"], m["M"]), lambda m: imp(m["M"], m["Z"])], {
    1: lambda m: imp(not m["Z"], not m["M"]), 2: lambda m: imp(not m["Y"], not m["Z"]), 3: lambda m: imp(m["R"], m["M"]),
    4: lambda m: imp(not m["M"], not m["R"])}, {"A": {1, 2}, "B": {1, 3, 4}, "C": {2, 3, 4}, "D": {1, 2, 3, 4}}, "D")
n = ["J", "Y", "B", "D", "W"]
impossible("34-5-6", n, [lambda m: imp(m["J"], m["Y"]), lambda m: imp(m["Y"], xor(m["B"], m["D"])), lambda m: imp(m["B"], m["W"]),
                         lambda m: imp(m["D"], m["W"])], {
    "A": lambda m: m["J"] and not m["W"], "B": lambda m: m["W"] and not m["J"], "C": lambda m: m["B"] and not m["Y"],
    "D": lambda m: m["D"] and m["W"]}, "A")

n = ["A", "B", "C", "D"]  # 罗浮山 双月湾 西湖 巽寮湾；四条建议都没采纳
entail("34-6-1", n, [lambda m: not imp(m["B"], m["A"]), lambda m: not xor(m["C"], m["D"]), lambda m: not (m["A"] or m["D"]),
                     lambda m: not imp(m["B"], m["C"])], {
    "A": lambda m: m["B"] and not m["A"] and not m["C"] and not m["D"], "B": lambda m: m["B"] and m["C"] and m["D"] and not m["A"],
    "C": lambda m: m["A"] and m["B"], "D": lambda m: not any(m.values())}, "A")
n = ["H", "Y", "G", "Z"]  # 本地户籍 居住证满1年 申请到公租房 转租
violation("34-6-2", n, lambda m: imp(m["G"], m["H"] or m["Y"]) and imp(m["G"], not m["Z"]), {
    1: lambda m: m["H"] and m["G"] and m["Z"], 2: lambda m: not m["H"] and m["Y"] and m["G"] and not m["Z"],
    3: lambda m: not m["H"] and not m["Y"] and m["G"], 4: lambda m: m["H"] and not m["G"]},
    {"A": {1, 3}, "B": {1, 2, 3}, "C": {3}, "D": {3, 4}}, "A")
n = ["T", "D", "P"]  # 贴息 营收下降 提交计划
violation("34-6-3", n, lambda m: imp(m["T"] and m["D"], m["P"]), {
    1: lambda m: m["T"] and m["D"] and not m["P"], 2: lambda m: m["T"] and not m["D"] and not m["P"],
    3: lambda m: not m["T"] and m["D"] and not m["P"], 4: lambda m: m["T"] and m["D"] and m["P"]},
    {"A": {1}, "B": {2}, "C": {3}, "D": {4}}, "A")
n = ["H", "F", "K"]  # 获批 焚烧厂 扩建填埋场
entail("34-6-4", n, [lambda m: m["H"] and not m["F"], lambda m: imp(m["H"], m["K"] or m["F"])], {
    "A": lambda m: m["H"] and m["K"], "B": lambda m: not m["H"], "C": lambda m: m["F"], "D": lambda m: not m["K"] and not m["F"]}, "A")

pr = ["Y", "W", "G"]  # 议事会居民 业委会成员 关心公共收益
c_bridge("34-7-1", pr, [], [lambda t: t["Y"] and t["W"]], {
    "A": ("U", lambda t: imp(t["W"], t["G"])), "B": ("U", lambda t: imp(t["G"], t["W"])),
    "C": ("E", lambda t: t["W"] and t["G"]), "D": ("E", lambda t: t["Y"] and not t["W"])}, ("E", lambda t: t["Y"] and t["G"]), "A")
pr = ["T", "N", "Z"]  # 科技特派员 农技专家 种植大户
c_bridge("34-7-2", pr, [lambda t: imp(t["T"], t["N"])], [], {
    "A": ("E", lambda t: t["Z"] and not t["N"]), "B": ("E", lambda t: t["N"] and not t["Z"]),
    "C": ("U", lambda t: imp(t["Z"], t["N"])), "D": ("E", lambda t: t["T"] and not t["Z"])}, ("E", lambda t: t["Z"] and not t["T"]), "A")
pr = ["S", "Z", "Q", "C"]  # 省级专业镇 主导产业 千年古镇 能申报产业强镇
c_bridge("34-7-3", pr, [lambda t: imp(t["S"], t["Z"])], [lambda t: t["Q"] and not t["Z"]], {
    "A": ("U", lambda t: imp(t["C"], t["Z"])), "B": ("U", lambda t: imp(t["Z"], t["C"])),
    "C": ("U", lambda t: imp(t["S"], t["C"])), "D": ("E", lambda t: t["Q"] and t["S"])}, ("E", lambda t: t["Q"] and not t["C"]), "A")

n = ["J", "Y", "B", "D", "W", "G"]
entail("34-8-1", n, [lambda m: m["J"] + m["Y"] + m["B"] >= 2, lambda m: not (m["J"] and m["D"]), lambda m: imp(m["Y"], m["D"]),
                     lambda m: imp(m["B"], not m["W"]), lambda m: imp(not m["W"], m["G"])], {
    "A": lambda m: m["B"] and m["G"] and not m["W"], "B": lambda m: m["J"], "C": lambda m: m["D"],
    "D": lambda m: not m["Y"] and not m["D"]}, "A")
n = ["J", "Y", "B", "D", "W"]
entail("34-8-2", n, [lambda m: m["J"] or m["Y"] or m["B"], lambda m: imp(m["J"], m["D"]), lambda m: imp(m["Y"], m["D"]),
                     lambda m: imp(m["B"], m["W"]), lambda m: imp(m["W"], m["D"])], {
    "A": lambda m: m["D"], "B": lambda m: m["W"], "C": lambda m: m["J"], "D": lambda m: not m["B"]}, "A")
n = ["A", "B", "C", "D", "E", "F"]
minmax("34-8-3", n, [lambda m: m["A"] or m["B"], lambda m: imp(m["A"], m["C"]), lambda m: imp(m["B"], m["D"] and m["E"]),
                     lambda m: imp(m["C"], m["F"]), lambda m: not (m["D"] and m["F"])], "min", {"A": 2, "B": 3, "C": 4, "D": 5}, "B")
n = ["J", "Y", "B"]
entail("34-8-4", n, [lambda m: imp(m["J"], m["Y"]), lambda m: imp(not m["J"], m["B"]), lambda m: not (m["Y"] and m["B"])], {
    "A": lambda m: iff(m["J"], m["Y"]), "B": lambda m: m["Y"], "C": lambda m: m["B"], "D": lambda m: not m["Y"] and not m["B"]}, "A")
n = ["A", "B", "C", "D"]
entail("34-8-5", n, [lambda m: imp(m["A"], m["B"]), lambda m: imp(m["B"], not m["C"]), lambda m: m["A"] or m["C"],
                     lambda m: imp(m["D"], m["C"])], {
    "A": lambda m: xor(m["A"], m["C"]), "B": lambda m: not m["D"], "C": lambda m: m["B"], "D": lambda m: m["C"]}, "A")
n = ["K", "W", "S", "J", "Y"]  # 放宽 维持 收紧 加强监管 优化流程
entail("34-8-6", n, [lambda m: m["K"] + m["W"] + m["S"] == 1, lambda m: imp(m["K"], m["J"]), lambda m: imp(m["W"], m["Y"]),
                     lambda m: imp(m["S"], m["J"])], {
    "A": lambda m: xor(m["J"], m["Y"]), "B": lambda m: m["J"] or m["Y"], "C": lambda m: m["J"],
    "D": lambda m: imp(not m["Y"], m["K"])}, "B")

n = ["A", "B", "C", "D", "E", "F"]  # 小苏：A/B 至少一项；A→¬C；B→D；C；目标 E∨F
bridge("34-9-1", n, [lambda m: m["A"] or m["B"], lambda m: imp(m["A"], not m["C"]), lambda m: imp(m["B"], m["D"]), lambda m: m["C"]], {
    "A": lambda m: imp(not m["E"] and not m["F"], not m["D"]), "B": lambda m: imp(m["E"] or m["F"], m["D"]),
    "C": lambda m: m["D"], "D": lambda m: not m["B"]}, lambda m: m["E"] or m["F"], "A")
n = ["J", "Y", "B", "D", "W"]
bridge("34-9-2", n, [lambda m: m["J"] or m["Y"], lambda m: imp(m["Y"], not m["B"]), lambda m: m["B"] or m["D"], lambda m: not m["J"]], {
    "A": lambda m: imp(m["D"], m["W"]), "B": lambda m: imp(m["W"], m["D"]), "C": lambda m: imp(not m["D"], m["W"]),
    "D": lambda m: imp(m["W"], m["B"])}, lambda m: m["W"], "A")
svc = ["S", "Y", "G", "H", "T"]   # 社保 医保 公积金 户籍 税务
def ok3493(c):
    return imp(c[1] == "S", c[2] == "Y") and (c[3] == "S" or c[1] == "S") and imp(c[2] == "Y", c[4] != "G") and \
           imp(c[5] == "H", c[4] == "G")
sols = [dict(zip([1, 2, 3, 4, 5], p)) for p in itertools.permutations(svc) if ok3493(dict(zip([1, 2, 3, 4, 5], p)))]
O = {"A": lambda c: c[5] == "H", "B": lambda c: c[4] != "G", "C": lambda c: c[2] == "Y", "D": lambda c: c[1] != "H"}
check("34-9-3", {k: any(f(c) for c in sols) and all(c[3] == "S" for c in sols if f(c)) for k, f in O.items()}, "A")
n = ["J", "Y", "B", "D", "W"]
bridge_fail("34-9-4", n, [lambda m: imp(m["J"], m["Y"] and m["B"]), lambda m: imp(m["D"], not m["Y"]), lambda m: m["W"] or m["J"]], {
    "A": lambda m: m["D"], "B": lambda m: not m["B"], "C": lambda m: not m["W"], "D": lambda m: imp(m["Y"], m["D"])},
    lambda m: not m["J"], "C")
n = ["K", "P", "B"]  # 开设培训班 聘请特级厨师 人社补贴
S = {1: lambda m: imp(m["P"], m["B"]), 2: lambda m: not m["B"], 3: lambda m: imp(m["B"], m["P"]), 4: lambda m: m["P"]}
pairs = {"A": (1, 2), "B": (2, 3), "C": (1, 4), "D": (3, 4)}
bridge("34-9-5", n, [lambda m: imp(m["K"], m["P"])], {k: (lambda m, a=a, b=b: S[a](m) and S[b](m)) for k, (a, b) in pairs.items()},
       lambda m: not m["K"], "A")
pr = ["S", "X", "Q", "M"]  # 摄影班 购买相机 社区青年 摄影达人
c_bridge("34-9-6", pr, [lambda t: imp(t["S"], t["X"])], [lambda t: t["Q"] and not t["X"]], {
    "A": ("U", lambda t: imp(t["M"], t["X"])), "B": ("U", lambda t: imp(t["X"], t["M"])),
    "C": ("E", lambda t: t["M"] and t["Q"]), "D": ("U", lambda t: imp(t["S"], t["M"]))}, ("E", lambda t: t["Q"] and not t["M"]), "A")
n = ["T", "S", "K", "Y"]  # 托管班 双师 课后服务 研学营
P = [lambda m: imp(m["T"], m["S"]), lambda m: not (m["S"] and m["K"]), lambda m: m["K"]]
S = {1: lambda m: imp(not m["T"], m["Y"]), 2: lambda m: imp(not m["Y"], not m["S"]), 3: lambda m: m["T"] or m["Y"],
     4: lambda m: imp(not m["S"], m["Y"]), 5: lambda m: imp(m["K"], m["Y"])}
c = sum(1 for f in S.values() if cons(n, P + [f]) and ent(n, P + [f], lambda m: m["Y"]))
check("34-9-7", {k: c == v for k, v in {"A": 2, "B": 3, "C": 4, "D": 5}.items()}, "C", "可得出结论的项数=%d" % c)
n = ["J", "Y", "B", "D"]
possible("34-9-8", n, [lambda m: imp(m["J"], m["Y"]), lambda m: imp(m["Y"], not m["B"]), lambda m: m["B"] or m["D"],
                       lambda m: imp(m["D"], m["J"])], {
    "A": lambda m: m["B"] and m["J"], "B": lambda m: not m["J"] and not m["B"], "C": lambda m: m["D"] and m["B"],
    "D": lambda m: m["J"] and m["D"]}, "D")

# =====================================================================
# 第 41 天
# =====================================================================
n = ["Y", "X", "S", "Z", "N", "C", "J"]  # 营业 消防验收 上线 执照 纳税 餐饮资格 健康证
notentail("41-1-1", n, [lambda m: imp(m["Y"], m["X"]), lambda m: imp(m["S"], m["Z"]), lambda m: imp(m["Z"], m["N"]),
                        lambda m: imp(m["C"], m["J"])], {
    "A": lambda m: imp(not m["X"], not m["Y"]), "B": lambda m: imp(m["S"], m["N"]), "C": lambda m: imp(m["C"], m["J"]),
    "D": lambda m: imp(m["Z"], m["S"])}, "D")
n = ["Y", "C"]  # 提前预约 参观
entail("41-1-2", n, [lambda m: imp(m["C"], m["Y"])], {
    "A": lambda m: imp(not m["Y"], not m["C"]), "B": lambda m: imp(m["Y"], m["C"]),
    "C": lambda m: imp(not m["C"], not m["Y"]), "D": lambda m: m["C"] and not m["Y"]}, "A")
n = ["F", "M", "H", "T"]  # 复审 进入面试 成绩合格 体检
count("41-1-3", n, [lambda m: imp(m["M"], m["F"]), lambda m: imp(m["T"], m["M"] and m["H"])], {
    1: lambda m: imp(not m["F"], not m["M"]), 2: lambda m: imp(m["T"], m["F"]), 3: lambda m: imp(m["M"] and m["H"], m["T"]),
    4: lambda m: imp(not m["H"], not m["T"]), 5: lambda m: imp(m["M"], m["T"])}, {"A": 2, "B": 3, "C": 4, "D": 5}, "B")
n = ["L", "S", "B", "G", "J"]  # 列支 审计 拨付 公示 结项
entail("41-1-4", n, [lambda m: imp(m["L"], m["S"]), lambda m: imp(m["B"], m["G"]), lambda m: imp(m["J"], m["S"] and m["G"])], {
    "A": lambda m: imp(m["J"], m["S"]), "B": lambda m: imp(m["S"] and m["G"], m["J"]), "C": lambda m: imp(m["B"], m["S"]),
    "D": lambda m: imp(not m["L"], not m["S"])}, "A")

n = ["M", "P", "B", "T", "X", "Z"]  # 卖得出且卖得好 品牌 标准化生产 全流程标准体系 做好文章 乡村振兴
entail("41-2-1", n, [lambda m: imp(m["M"], m["P"]), lambda m: imp(m["P"], m["B"]), lambda m: imp(m["B"], m["T"])], {
    "A": lambda m: imp(not m["T"], not m["M"]), "B": lambda m: imp(not m["X"], not m["Z"]), "C": lambda m: imp(m["T"], m["P"]),
    "D": lambda m: imp(m["P"], m["M"])}, "A")
n = ["K", "S", "Q", "R", "D"]  # 更可及 设施 质量 人员 待遇
notentail("41-2-2", n, [lambda m: imp(m["K"], m["S"]), lambda m: imp(m["Q"], m["S"] and m["R"]), lambda m: imp(m["R"], m["D"])], {
    "A": lambda m: imp(not m["S"], not m["K"]), "B": lambda m: imp(not m["D"], not m["Q"]), "C": lambda m: imp(m["Q"], m["S"]),
    "D": lambda m: imp(m["R"], m["Q"])}, "D")
n = ["H", "B", "F", "Q", "H2", "B2", "F2", "Q2"]  # 合法新建 报批 汛期 抢险；*2 泛指他人
R = lambda h, b, f, q: imp(h, b) and imp(h and f, q)
entail("41-2-3", n, [lambda m: R(m["H"], m["B"], m["F"], m["Q"]), lambda m: R(m["H2"], m["B2"], m["F2"], m["Q2"]),
                     lambda m: m["H"], lambda m: m["F"]], {
    "A": lambda m: m["Q"] and m["B"], "B": lambda m: not m["Q"], "C": lambda m: imp(m["F2"] and m["B2"], m["H2"]),
    "D": lambda m: not m["B"]}, "A")
n = ["M", "T", "Y"]  # 民生工程 听取意见 议事会
entail("41-2-4", n, [lambda m: imp(m["M"], m["T"]), lambda m: imp(m["T"], m["Y"])], {
    "A": lambda m: imp(m["M"], m["Y"]), "B": lambda m: imp(m["Y"], m["M"]), "C": lambda m: m["M"] and not m["T"],
    "D": lambda m: m["M"] and not m["Y"]}, "A")

stem = excluded(lambda x, y: imp(not x, not y))     # 人不犯我(¬x)，我不犯人(¬y)
O = {"A": excluded(lambda x, y: imp(not x, not y)),  # 若要人不知(¬x)，除非己莫为(¬y)：¬x→¬y
     "B": excluded(lambda x, y: imp(x, y)), "C": excluded(lambda x, y: not (x and y)), "D": excluded(lambda x, y: imp(x, y))}
check("41-3-1", {k: v == stem for k, v in O.items()}, "A")
n = ["H", "C"]  # 好评≥98% 超时订单
violation("41-3-2", n, lambda m: iff(m["H"], not m["C"]), {
    1: lambda m: not m["C"] and not m["H"], 2: lambda m: m["C"] and not m["H"], 3: lambda m: m["H"] and not m["C"],
    4: lambda m: not m["H"] and m["C"]}, {"A": {1}, "B": {2}, "C": {3}, "D": {4}}, "A")
pr = ["W", "P"]  # 周末 需要排队；老李否定"排队→周末"
c_entail("41-3-3", pr, [], [lambda t: t["P"] and not t["W"]], {
    "A": ("U", lambda t: imp(t["W"], not t["P"])), "B": ("E", lambda t: t["P"] and not t["W"]),
    "C": ("E", lambda t: t["W"] and not t["P"]), "D": ("U", lambda t: imp(t["P"], not t["W"]))}, "B")

n = ["K", "A", "B", "Ph", "Zg", "Ms", "Ys", "F"]  # 满1年 A卡 B卡 博士 正高 硕士 院士/国家级 可买二套
entail("41-4-1", n, [lambda m: imp(m["A"] or m["B"], m["K"]), lambda m: imp(m["A"], m["Ys"]),
                     lambda m: imp(m["B"], m["Ph"] or (m["Zg"] and m["Ms"])), lambda m: imp(m["A"], m["F"]),
                     lambda m: m["B"], lambda m: not m["Ph"]], {
    "A": lambda m: m["Zg"], "B": lambda m: m["F"], "C": lambda m: m["Ys"], "D": lambda m: not m["K"]}, "A")
# 41-4-2：逐个情形判断是否合规
def ok_trash(kind, poke, booked, at_point, hour):
    window = (7 <= hour < 9) or (19 <= hour < 21)
    if kind == "厨余" and not poke: return False
    if kind == "大件" and not (booked and at_point): return False
    return window or (kind == "大件" and booked)
cases = {"A": ("厨余", False, False, True, 20), "B": ("大件", True, True, True, 15),
         "C": ("大件", True, False, True, 8), "D": ("厨余", True, False, True, 22)}
check("41-4-2", {k: ok_trash(*v) for k, v in cases.items()}, "B")
n = ["S", "Z", "W", "Q"]  # 缴社保满3年 子女公办就读 工作满3年 区统筹
bridge("41-4-3", n, [lambda m: m["Z"]], {
    "A": lambda m: imp(m["Z"], m["S"]), "B": lambda m: imp(m["S"], m["Z"]), "C": lambda m: m["Q"], "D": lambda m: m["W"]},
    lambda m: m["S"], "A")
n = ["A18", "Z", "J", "R"]  # 满18 有效证件 饮酒 允许；"只会因须知情形拒绝"⇒充要
entail("41-4-4", n, [lambda m: iff(m["R"], m["A18"] and m["Z"] and not m["J"]), lambda m: m["A18"], lambda m: m["Z"],
                     lambda m: not m["R"]], {
    "A": lambda m: m["J"], "B": lambda m: not m["A18"], "C": lambda m: not m["Z"],
    "D": lambda m: cons(n, [lambda x: iff(x["R"], x["A18"] and x["Z"] and not x["J"]), lambda x: x["A18"], lambda x: x["Z"],
                            lambda x: not x["J"], lambda x: not x["R"]])}, "A")

n = ["N", "M", "J", "D", "W"]  # 不出村 慢病管理 签约机制 待遇保障 稳定队伍
entail("41-5-1", n, [lambda m: imp(m["N"], m["J"]), lambda m: imp(m["M"], m["J"]), lambda m: imp(m["J"], m["D"]),
                     lambda m: imp(m["W"], m["D"])], {
    "A": lambda m: imp(not m["W"], not m["N"]), "B": lambda m: imp(m["M"], m["D"]), "C": lambda m: imp(m["J"], m["N"]),
    "D": lambda m: imp(not m["M"], not m["N"])}, "B")
n = ["Z", "K", "R", "C", "T"]  # 总部企业 空置率下降 租金上涨 初创入驻 调整策略
entail("41-5-2", n, [lambda m: imp(m["Z"], m["K"]), lambda m: imp(m["K"], m["R"]), lambda m: imp(m["C"], not m["R"]),
                     lambda m: imp(not m["C"], m["T"]), lambda m: m["Z"]], {
    "A": lambda m: m["T"], "B": lambda m: m["C"], "C": lambda m: not m["R"], "D": lambda m: not m["K"]}, "A")
n = ["P1", "J1", "Z1", "P2", "J2", "Z2"]  # 甲/乙村：评上 奖补 整治
ring = lambda p, j, z: imp(p, j) and imp(j, z) and imp(z, p)
entail("41-5-3", n, [lambda m: ring(m["P1"], m["J1"], m["Z1"]), lambda m: ring(m["P2"], m["J2"], m["Z2"]), lambda m: m["J1"],
                     lambda m: not m["Z2"]], {
    "A": lambda m: m["P1"] and not m["J2"], "B": lambda m: not m["Z1"], "C": lambda m: m["P2"], "D": lambda m: m["J2"]}, "A")
n = ["J", "Y", "B", "D", "W"]
impossible("41-5-4", n, [lambda m: imp(m["J"], m["Y"] or m["B"]), lambda m: imp(m["Y"], m["D"]), lambda m: imp(m["B"], m["D"]),
                         lambda m: imp(m["D"], not m["W"])], {
    "A": lambda m: m["J"] and m["W"], "B": lambda m: m["Y"] and not m["B"], "C": lambda m: m["D"] and not m["J"],
    "D": lambda m: m["W"] and not m["D"]}, "A")
n = ["G", "S", "Z", "M", "C"]  # 广州 深圳 珠海 澳门 中山
entail("41-5-5", n, [lambda m: imp(m["G"], not m["S"]), lambda m: xor(m["S"], m["Z"]), lambda m: imp(m["Z"], m["M"]),
                     lambda m: imp(m["M"], m["C"]), lambda m: m["G"]], {
    "A": lambda m: m["Z"] and m["M"] and m["C"], "B": lambda m: m["S"], "C": lambda m: m["Z"] and not m["M"], "D": lambda m: not m["C"]}, "A")

n = ["L", "U", "F", "J", "T", "U2", "T2"]  # A企业：链主 联盟 基金 奖励 培训任务；B企业：联盟 培训任务
entail("41-6-1", n, [lambda m: imp(m["L"], xor(m["U"], m["F"])), lambda m: imp(m["F"], m["J"]), lambda m: imp(m["U"], m["T"]),
                     lambda m: imp(m["U2"], m["T2"]), lambda m: m["L"], lambda m: not m["J"], lambda m: m["T2"]], {
    "A": lambda m: m["U"] and m["T"], "B": lambda m: m["F"], "C": lambda m: m["U2"], "D": lambda m: m["U"] and m["F"]}, "A")
n = ["A", "B", "C", "D", "E"]
P = [lambda m: imp(m["A"], m["B"]), lambda m: not (m["B"] and m["C"]), lambda m: imp(m["C"], m["D"]), lambda m: m["D"] or m["E"]]
entail("41-6-2.1", n, P + [lambda m: m["A"]], {
    "A": lambda m: m["B"] and not m["C"], "B": lambda m: m["D"], "C": lambda m: m["C"], "D": lambda m: not m["E"]}, "A")
entail("41-6-2.2", n, P + [lambda m: not m["E"]], {
    "A": lambda m: m["D"], "B": lambda m: m["C"], "C": lambda m: not m["A"], "D": lambda m: m["B"]}, "A")

pr = ["J", "L", "F", "Z"]  # 决赛团队 路演 风投 注册公司
c_possible("41-7-1", pr, [lambda t: imp(t["J"], t["L"]), lambda t: imp(t["F"], t["Z"])], [lambda t: t["L"] and t["F"]], {
    "A": ("E", lambda t: t["J"] and not t["L"]), "B": ("U", lambda t: imp(t["F"], not t["Z"])),
    "C": ("U", lambda t: imp(t["L"], not t["Z"])), "D": ("U", lambda t: imp(t["J"], not t["F"]))}, "D")
pr = ["P", "X", "S", "J"]  # 入选品牌 星级评定 失信 家政企业
c_impossible("41-7-2", pr, [lambda t: imp(t["P"], t["X"]), lambda t: imp(t["X"], not t["S"])], [lambda t: t["J"] and t["S"]], {
    "A": ("E", lambda t: t["S"] and t["X"]), "B": ("E", lambda t: t["J"] and not t["P"]),
    "C": ("E", lambda t: (not t["P"]) and t["X"]), "D": ("E", lambda t: t["X"] and t["J"])}, "A")
pr = ["A", "B", "C", "D"]
c_notentail("41-7-3", pr, [lambda t: imp(t["A"], t["B"]), lambda t: imp(t["B"], t["C"])], [lambda t: t["D"] and t["A"]], {
    "A": ("E", lambda t: t["D"] and t["C"]), "B": ("E", lambda t: t["C"] and t["D"]), "C": ("U", lambda t: imp(t["A"], t["C"])),
    "D": ("E", lambda t: t["C"] and not t["A"])}, "D")
st = {"A": True, "B": True, "C": True, "D": True}
for r in range(25, 33):        # 50人：党员25⊆报课r⊆调研32
    st["A"] &= r >= 25; st["B"] &= 0 >= 18; st["C"] &= r == 32; st["D"] &= (50 - r) >= 25
check("41-7-4", st, "A")

pr = ["W", "K", "I"]  # 网约车 客运经营 营运险
def c_bridge_univ(code, preds, U, E, O, f, e):
    st = {}
    for k, o in O.items():
        U2 = U + ([o[1]] if o[0] == "U" else []); E2 = E + ([o[1]] if o[0] == "E" else [])
        st[k] = cok(preds, U2, E2) and c_univ(preds, U2, E2, f)
    check(code, st, e)
c_bridge_univ("41-8-1", pr, [lambda t: imp(t["K"], t["I"])], [], {
    "A": ("U", lambda t: imp(t["W"], t["K"])), "B": ("E", lambda t: t["W"] and t["K"]),
    "C": ("U", lambda t: imp(t["K"], t["W"])), "D": ("E", lambda t: True)}, lambda t: imp(t["W"], t["I"]), "A")
pr = ["Z", "S", "X"]  # 带货主播 食品安全知识 能销售预包装食品
c_bridge("41-8-2", pr, [], [lambda t: t["Z"] and not t["S"]], {
    "A": ("U", lambda t: imp(t["X"], t["S"])), "B": ("U", lambda t: imp(t["S"], t["X"])),
    "C": ("E", lambda t: t["X"] and not t["S"]), "D": ("E", lambda t: True)}, ("E", lambda t: t["Z"] and not t["X"]), "A")
pr = ["Z", "Y", "G"]  # 专精特新 省级研发中心 高新企业；选"不能使结论成立"
st = {}
for k, o in {"A": ("U", lambda t: imp(t["Y"], t["G"])), "B": ("U", lambda t: imp(t["Z"], t["G"])),
             "C": ("U", lambda t: imp(not t["G"], not t["Y"])), "D": ("U", lambda t: imp(t["G"], t["Y"]))}.items():
    U2 = [o[1]]; E2 = [lambda t: t["Z"] and t["Y"]]
    st[k] = not (cok(pr, U2, E2) and c_exist(pr, U2, E2, lambda t: t["Z"] and t["G"]))
check("41-8-3", st, "D")

n = ["J", "Y", "B", "D", "W", "G", "K", "X"]  # 甲乙丙丁戊己庚辛
entail("41-9-1", n, [lambda m: m["J"] + m["Y"] + m["B"] >= 2, lambda m: not (m["D"] and m["W"]),
                     lambda m: imp(m["J"] and m["Y"], m["D"] and m["W"]), lambda m: imp(m["B"], m["G"]),
                     lambda m: imp(m["G"], not m["K"] and m["X"])], {
    "A": lambda m: m["B"] and m["G"] and m["X"] and not m["K"], "B": lambda m: m["J"] and m["Y"], "C": lambda m: m["D"],
    "D": lambda m: m["K"]}, "A")
n = ["A", "B", "C", "D", "E", "F"]
minmax("41-9-2", n, [lambda m: m["A"] or m["B"], lambda m: imp(m["A"], m["C"]), lambda m: imp(m["B"], m["D"]),
                     lambda m: not (m["C"] and m["D"]), lambda m: imp(m["E"], m["C"]), lambda m: imp(m["F"], m["D"])], "max",
       {"A": 2, "B": 3, "C": 4, "D": 5}, "B")
n = ["J", "Y", "B", "D"]
possible("41-9-3", n, [lambda m: imp(m["J"], m["Y"]), lambda m: imp(m["Y"], not m["B"]), lambda m: imp(not m["B"], m["D"]),
                       lambda m: imp(m["D"], not m["J"])], {
    "A": lambda m: m["J"] and m["D"], "B": lambda m: m["Y"] and m["B"], "C": lambda m: m["Y"] and not m["D"],
    "D": lambda m: m["B"] and m["D"]}, "D")
n = ["J", "Y", "B", "D", "W"]
P = [lambda m: imp(m["J"], m["Y"]), lambda m: imp(m["Y"], m["B"] and m["D"]), lambda m: imp(m["D"], not m["J"]),
     lambda m: imp(m["W"], m["J"])]
ms = list(models(n, P)); never = sum(1 for x in n if all(not m[x] for m in ms))
check("41-9-4", {k: never == v for k, v in {"A": 1, "B": 2, "C": 3, "D": 4}.items()}, "B", "一定不获奖人数=%d" % never)
n = ["K", "W", "S", "J", "H"]  # 放宽 维持 收紧 加强监管 增加审批人手
entail("41-9-5", n, [lambda m: m["K"] + m["W"] + m["S"] == 1, lambda m: imp(m["K"], m["J"]), lambda m: imp(m["S"], m["H"]),
                     lambda m: not m["J"] and not m["H"]], {
    "A": lambda m: m["W"], "B": lambda m: m["K"], "C": lambda m: m["S"], "D": lambda m: not m["K"] and not m["W"]}, "A")

ppl = ["方", "简", "古", "麦"]; roles = ["主持", "记录", "摄影", "后勤"]
def ok41101(a):
    return imp(a["方"] == "主持", a["简"] == "摄影") and imp(a["简"] == "摄影", a["古"] == "记录") and \
           xor(a["方"] == "主持", a["麦"] == "主持") and imp(a["古"] == "记录", a["麦"] == "后勤")
sols = [dict(zip(ppl, p)) for p in itertools.permutations(roles) if ok41101(dict(zip(ppl, p)))]
O = {"A": lambda a: a["古"] != "记录", "B": lambda a: a["简"] == "摄影", "C": lambda a: a["古"] == "记录", "D": lambda a: a["简"] == "主持"}
check("41-10-1", {k: any(f(a) for a in sols) and all(a["麦"] == "主持" for a in sols if f(a)) for k, f in O.items()}, "A")
n = ["J", "Y", "B", "D", "W"]
bridge("41-10-2", n, [lambda m: m["J"] or m["Y"], lambda m: imp(m["Y"], not m["B"]), lambda m: m["B"] or m["D"], lambda m: not m["J"]], {
    "A": lambda m: imp(m["D"], not m["W"]), "B": lambda m: imp(m["W"], m["D"]), "C": lambda m: imp(not m["W"], m["D"]),
    "D": lambda m: imp(m["B"], m["W"])}, lambda m: not m["W"], "A")
pr = ["X", "Z", "B", "N"]  # 调研之星 座谈会 提交报告 90后干部
c_bridge("41-10-3", pr, [lambda t: imp(t["X"], t["Z"])], [lambda t: t["N"] and not t["B"]], {
    "A": ("U", lambda t: imp(t["Z"], t["B"])), "B": ("U", lambda t: imp(t["B"], t["Z"])),
    "C": ("E", lambda t: t["N"] and t["Z"]), "D": ("E", lambda t: t["B"] and t["X"])}, ("E", lambda t: t["N"] and not t["X"]), "A")
n = ["E", "C", "K", "J", "F", "S"]  # 长者饭堂 儿童之家 四点半课堂 健康驿站 法律门诊 社区书房
P = [lambda m: m["E"] or m["C"], lambda m: imp(m["E"], m["J"]), lambda m: imp(m["C"], m["K"]), lambda m: not (m["J"] and m["K"]),
     lambda m: iff(m["F"], m["J"]), lambda m: imp(m["C"], m["S"])]
O = {"A": lambda m: m["F"], "B": lambda m: m["S"], "C": lambda m: m["K"], "D": lambda m: m["E"] or m["S"]}
check("41-10-4", {k: unique_model(n, P + [f]) for k, f in O.items()}, "C", "原条件下方案数=%d" % len(list(models(n, P))))
n = ["A", "B", "C"]
combo("41-10-5", n, [lambda m: imp(m["A"], m["B"]), lambda m: imp(m["C"], not m["B"])], {
    1: (lambda m: m["C"], lambda m: not m["A"]), 2: (lambda m: not m["B"], lambda m: not m["A"]),
    3: (lambda m: imp(m["A"], m["C"]), lambda m: not m["A"]), 4: (lambda m: imp(m["B"], m["C"]), lambda m: not m["A"])},
    {"A": {1, 2}, "B": {1, 2, 3}, "C": {2, 4}, "D": {1, 2, 3, 4}}, "D", kind="bridge")
n = ["L", "X", "H"]  # 冷链 县域市场 供销社合作
bridge("41-10-6", n, [lambda m: imp(not m["L"], not m["X"])], {
    "A": lambda m: imp(m["L"], m["H"]), "B": lambda m: imp(m["H"], m["L"]), "C": lambda m: imp(m["L"], m["X"]), "D": lambda m: True},
    lambda m: imp(m["X"], m["H"]), "A")
n = ["J", "Y", "B", "D"]
bridge("41-10-7", n, [lambda m: imp(m["J"], m["B"]), lambda m: imp(m["Y"], m["D"])], {
    "A": lambda m: not (m["B"] and m["D"]), "B": lambda m: m["B"] or m["D"], "C": lambda m: imp(m["B"], m["J"]), "D": lambda m: m["J"]},
    lambda m: not (m["J"] and m["Y"]), "A")

if __name__ == "__main__":
    import sys
    sys.exit(1 if run_and_report("L01 改编设计验算") else 0)
