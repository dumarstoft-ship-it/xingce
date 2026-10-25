# L01 翻译推理 —— 验算工具库（命题逻辑真值表 / 直言类型模型 / 可能世界）
# 原则：只根据题面条件建模，逐项判断选项，确认恰好一个选项满足设问。
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
def unknown(code, n, P, O, e):   # 真假不能确定
    check(code, {k: cons(n, P + [f]) and cons(n, P + [lambda m, f=f: not f(m)]) for k, f in O.items()}, e)
def bridge(code, n, P, O, T, e):
    check(code, {k: cons(n, P + [f]) and ent(n, P + [f], T) for k, f in O.items()}, e)
def bridge_fail(code, n, P, O, T, e):   # 选非：补充后不能得出结论
    check(code, {k: not (cons(n, P + [f]) and ent(n, P + [f], T)) for k, f in O.items()}, e)
def combo(code, n, P, S, C, e, kind="entail"):
    if kind == "entail":
        got = {i for i, f in S.items() if ent(n, P, f)}
    elif kind == "notentail":
        got = {i for i, f in S.items() if not ent(n, P, f)}
    elif kind == "impossible":
        got = {i for i, f in S.items() if not cons(n, P + [f])}
    elif kind == "possible":
        got = {i for i, f in S.items() if cons(n, P + [f])}
    elif kind == "bridge":   # S 中每项为 (补充条件, 目标)
        got = {i for i, (f, t) in S.items() if cons(n, P + [f]) and ent(n, P + [f], t)}
    check(code, {k: got == set(v) for k, v in C.items()}, e, "成立项=" + str(sorted(got)))
def count(code, n, P, S, C, e):
    c = sum(1 for f in S.values() if ent(n, P, f))
    check(code, {k: c == v for k, v in C.items()}, e, "成立项数=%d" % c)
def equiv(code, n, stem, O, e):
    allv = [dict(zip(n, v)) for v in itertools.product([False, True], repeat=len(n))]
    check(code, {k: all(stem(m) == f(m) for m in allv) for k, f in O.items()}, e)
def contradict(code, n, stem, O, e):   # 与题干矛盾 = 真值处处相反
    allv = [dict(zip(n, v)) for v in itertools.product([False, True], repeat=len(n))]
    check(code, {k: all(stem(m) != f(m) for m in allv) for k, f in O.items()}, e)
def violation(code, n, rule, cases, C, e):
    vio = {i for i, c in cases.items() if ent(n, [c], lambda m: not rule(m))}
    check(code, {k: vio == set(v) for k, v in C.items()}, e, "违反=" + str(sorted(vio)))
def minmax(code, n, P, which, C, e, over=None):
    ms = list(models(n, P)); assert ms
    over = over or n
    sizes = [sum(m[x] for x in over) for m in ms]
    val = min(sizes) if which == "min" else max(sizes)
    check(code, {k: val == v for k, v in C.items()}, e, "%s=%d" % (which, val))
def nmodels(n, P): return len(list(models(n, P)))

# ---------------- 直言命题：类型模型 ----------------
# 一个"模型"= 若干非空类型（谓词真假组合）的集合；全称句限制允许出现的类型，特称句要求有见证类型。
def ctypes(preds): return [dict(zip(preds, v)) for v in itertools.product([False, True], repeat=len(preds))]
def callowed(preds, U): return [t for t in ctypes(preds) if all(u(t) for u in U)]
def cok(preds, U, E):
    a = callowed(preds, U); return all(any(e(t) for t in a) for e in E)
def c_univ(preds, U, E, f):
    assert cok(preds, U, E), "直言前提不相容"
    return all(f(t) for t in callowed(preds, U))
def c_exist(preds, U, E, g):
    assert cok(preds, U, E), "直言前提不相容"
    rest = [t for t in callowed(preds, U) if not g(t)]
    return not all(any(e(t) for t in rest) for e in E)
def c_poss_exist(preds, U, E, g):
    return cok(preds, U, E) and any(g(t) for t in callowed(preds, U))
def c_poss_univ(preds, U, E, f):
    a = [t for t in callowed(preds, U) if f(t)]
    return all(any(e(t) for t in a) for e in E)
def c_true(preds, U, E, o):
    return c_univ(preds, U, E, o[1]) if o[0] == "U" else c_exist(preds, U, E, o[1])
def c_poss(preds, U, E, o):
    return c_poss_univ(preds, U, E, o[1]) if o[0] == "U" else c_poss_exist(preds, U, E, o[1])
def c_entail(code, preds, U, E, O, e): check(code, {k: c_true(preds, U, E, o) for k, o in O.items()}, e)
def c_notentail(code, preds, U, E, O, e): check(code, {k: not c_true(preds, U, E, o) for k, o in O.items()}, e)
def c_impossible(code, preds, U, E, O, e): check(code, {k: not c_poss(preds, U, E, o) for k, o in O.items()}, e)
def c_possible(code, preds, U, E, O, e): check(code, {k: c_poss(preds, U, E, o) for k, o in O.items()}, e)
def c_neg(o):
    return ("E", lambda x, f=o[1]: not f(x)) if o[0] == "U" else ("U", lambda x, g=o[1]: not g(x))
def c_unknown(code, preds, U, E, O, e):
    def unk(o):
        return (not c_true(preds, U, E, o)) and c_poss(preds, U, E, o) and c_poss(preds, U, E, c_neg(o))
    check(code, {k: unk(o) for k, o in O.items()}, e)
def c_bridge(code, preds, U, E, O, concl, e):
    st = {}
    for k, o in O.items():
        if o is None:
            st[k] = False; continue
        U2 = U + ([o[1]] if o[0] == "U" else []); E2 = E + ([o[1]] if o[0] == "E" else [])
        st[k] = cok(preds, U2, E2) and c_true(preds, U2, E2, concl)
    check(code, st, e)

# ---------------- 可能世界（模态） ----------------
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
def k_notentail(code, wv, gv, P, O, e, wcon=lambda w: True):
    check(code, {k: not k_ent(wv, gv, P, f, wcon) for k, f in O.items()}, e)
def k_contra(code, wv, gv, P, O, e, wcon=lambda w: True):
    check(code, {k: not k_cons(wv, gv, P + [f], wcon) for k, f in O.items()}, e)
def k_equiv(code, wv, gv, stem, O, e, wcon=lambda w: True):
    ms = list(kmodels(wv, gv, wcon))
    check(code, {k: all(stem(M) == f(M) for M in ms) for k, f in O.items()}, e)

def report(title, only_fail=False):
    w = max(len(r[0]) for r in REPORT) if REPORT else 4
    bad = 0
    for code, got, want, ok, note in REPORT:
        if not ok: bad += 1
        if ok and only_fail: continue
        print(f"{code:<{w}}  程序={got:<10} 设计={want:<6} {'OK' if ok else '**FAIL**'}  {note}")
    print(f"{title}: 共 {len(REPORT)} 项，失败 {bad} 项")
    return bad
