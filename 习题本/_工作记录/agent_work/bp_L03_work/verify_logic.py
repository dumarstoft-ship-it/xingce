"""Independent checks for L03 blueprint: formal-bridging items and numeric data in variant ideas.
Each argument is modelled from the stem; we test which option (added as a premise) makes the
conclusion valid. 'Most/大多' statements are modelled as imposing no constraint on an individual."""
import itertools

def valid_individual(vars_, premises, option, conclusion):
    """Propositional check for one named individual (universal premises instantiated)."""
    for vals in itertools.product([False, True], repeat=len(vars_)):
        env = dict(zip(vars_, vals))
        if all(p(env) for p in premises) and option(env) and not conclusion(env):
            return False
    return True

imp = lambda a, b: (not a) or b

def report(name, vars_, premises, options, conclusion):
    res = {k: valid_individual(vars_, premises, f, conclusion) for k, f in options.items()}
    ok = [k for k, v in res.items() if v]
    print(f"{name}: options making argument valid -> {ok}")
    # sanity: argument without any option must be invalid
    print("   valid without option?", valid_individual(vars_, premises, lambda e: True, conclusion))
    return ok

# 1. Real 2024SZ-38. X=想从事专门性社会服务工作, Z=想取得证书, R=报名考试, Q=已取得证书, S=有资格从事
report("2024SZ-38", ["X", "Z", "R", "Q", "S"],
       [lambda e: imp(e["X"], e["Z"]), lambda e: e["Z"]],
       {"A": lambda e: imp(not e["Z"], not e["R"]),
        "B": lambda e: imp(e["Z"], e["X"]),
        "C": lambda e: imp(e["S"], e["Q"]),
        "D": lambda e: True},  # 大都 -> no constraint on the individual
       lambda e: e["X"])

# 2. Day10 G1 V2: C=符合人才公寓申请条件, S=社保满3年, M=硕士. Premise C->S; facts S, M; conclusion C
report("D10-G1-V2 人才公寓", ["C", "S", "M"],
       [lambda e: imp(e["C"], e["S"]), lambda e: e["S"], lambda e: e["M"]],
       {"正确:(S且M)->C": lambda e: imp(e["S"] and e["M"], e["C"]),
        "只有硕士才符合:C->M": lambda e: imp(e["C"], e["M"]),
        "符合者都社保满3年:C->S": lambda e: imp(e["C"], e["S"]),
        "多数硕士符合(无约束)": lambda e: True},
       lambda e: e["C"])

# 3. Day10 G9 V1: X=获示范店称号, Z=承诺七天无理由退货, P=门口张贴承诺书
report("D10-G9-V1 示范店", ["X", "Z", "P"],
       [lambda e: imp(e["X"], e["Z"]), lambda e: e["Z"]],
       {"正确:只有获称号才承诺 Z->X": lambda e: imp(e["Z"], e["X"]),
        "获称号者都张贴承诺书 X->P": lambda e: imp(e["X"], e["P"]),
        "承诺者大多获称号(无约束)": lambda e: True,
        "未承诺者都未获称号 ~Z->~X": lambda e: imp(not e["Z"], not e["X"])},
       lambda e: e["X"])

# 4. Day23 G5 V1 (否前修复): Y=优秀网格员, T=参加消防培训. Premise Y->T; fact ~Y; conclusion ~T
report("D23-G5-V1 网格员", ["Y", "T", "D"],
       [lambda e: imp(e["Y"], e["T"]), lambda e: not e["Y"]],
       {"正确:只有优秀才培训 T->Y": lambda e: imp(e["T"], e["Y"]),
        "培训者大多优秀(无约束)": lambda e: True,
        "未培训者都不优秀 ~T->~Y": lambda e: imp(not e["T"], not e["Y"]),
        "优秀者都参加应急演练 Y->D": lambda e: imp(e["Y"], e["D"])},
       lambda e: not e["T"])

# 5. Day37 G11 V10 (两步链): Y=优秀社区, W=无违建社区, Q=完成楼道清理. Premises Y->W, W->Q; fact Q; concl Y
report("D37-G11-V10 优秀社区", ["Y", "W", "Q"],
       [lambda e: imp(e["Y"], e["W"]), lambda e: imp(e["W"], e["Q"]), lambda e: e["Q"]],
       {"正确:只有优秀才完成清理 Q->Y": lambda e: imp(e["Q"], e["Y"]),
        "无违建都入选优秀 W->Y": lambda e: imp(e["W"], e["Y"]),
        "只有无违建才完成清理 Q->W": lambda e: imp(e["Q"], e["W"]),
        "完成清理的都是无违建 Q->W(同义)": lambda e: imp(e["Q"], e["W"])},
       lambda e: e["Y"])

# 6. Day30 G11 V3 (特称结论, 一元谓词): G=绿色社区, J=积分制, E=旧物交换站
# premises: all G are J; some J are E. conclusion: some E are G. Enumerate inhabited type sets.
types = list(itertools.product([False, True], repeat=3))  # (G,J,E)
def models():
    for mask in range(1, 2 ** len(types)):
        yield [t for i, t in enumerate(types) if mask >> i & 1]
def holds_all(m, f):  return all(f(*t) for t in m)
def holds_some(m, f): return any(f(*t) for t in m)
prem = [lambda m: holds_all(m, lambda G, J, E: imp(G, J)), lambda m: holds_some(m, lambda G, J, E: J and E)]
concl = lambda m: holds_some(m, lambda G, J, E: E and G)
opts = {"正确:所有积分制社区都获评绿色 J->G": lambda m: holds_all(m, lambda G, J, E: imp(J, G)),
        "有些绿色社区没开交换站": lambda m: holds_some(m, lambda G, J, E: G and not E),
        "所有开交换站的都实行积分制 E->J": lambda m: holds_all(m, lambda G, J, E: imp(E, J)),
        "有些绿色社区实行积分制": lambda m: holds_some(m, lambda G, J, E: G and J)}
print("D30-G11-V3 绿色社区:")
print("   valid without option?", all(concl(m) for m in models() if all(p(m) for p in prem)))
for k, f in opts.items():
    v = all(concl(m) for m in models() if all(p(m) for p in prem) and f(m))
    print(f"   {k}: {'VALID' if v else 'invalid'}")

# ---- numeric checks for data-type variant ideas ----
print("\nNumeric checks")
print("D2-G4-V1 新能源增量贡献:", 9 / 10)
r = 260 / 200; print("D10-G5-V1 事故 7月/4月:", r, "| 若订单+40%, 事故率比值:", round(260 / 1.4 / 200, 3))
# helmet: share among deaths 80% unhelmeted; share among riders 20% unhelmeted
rr = (0.8 / 0.2) / (0.2 / 0.8); print("D10-G5-V2 头盔 相对死亡风险(未戴/戴):", rr)
print("D17-G2-V5 培训再就业率:", 1360 / 2000, 3600 / 8000, "| 绝对数比:", 3600 / 1360)
print("D30-G2-V2 薄膜发电 Wh:", 0.01 * 200 * 8, "(常见手机电池约 15~19 Wh: 4000mAh*3.85V=", 4 * 3.85, ", 5000mAh=", 5 * 3.85, ")")
hk_last, fo_last = 2760 / 1.15, 320 / 1.6
print("D30-G2-V3 港澳去年/增量:", round(hk_last, 2), round(2760 - hk_last, 2), "| 外国去年/增量:", fo_last, 320 - fo_last,
      "| 港澳增量占比:", round((2760 - hk_last) / ((2760 - hk_last) + (320 - fo_last)), 3))
print("D37-G5-V2 疫苗 节省(万元):", 20000 * 0.3 * 15000 / 1e4, "vs 接种费用 6000 万元")
print("D37-G10-V3 新业态净增占比:", 4500 / 6000, "| 传统业态 毛增/净增:", 12000 - 4800, 6000 - 4500)
print("D2-G5? SPF 阻挡率 30/50:", round(1 - 1 / 30, 4), round(1 - 1 / 50, 4), "差", round((1 / 30 - 1 / 50) * 100, 2), "个百分点")
