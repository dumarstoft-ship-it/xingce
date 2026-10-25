# -*- coding: utf-8 -*-
"""翻译推理（L01）穷举验证：对每道题列真值表，检查各选项是否被题干必然推出。"""
from itertools import product


def imp(a, b):
    return (not a) or b


def entails(names, premises, conclusion):
    """premises/conclusion: functions of a dict env. Returns (entailed?, #models)."""
    models = 0
    for vals in product([False, True], repeat=len(names)):
        env = dict(zip(names, vals))
        if all(p(env) for p in premises):
            models += 1
            if not conclusion(env):
                return False, models
    return True, models


def show(title, results):
    print("==", title)
    for k, v in results.items():
        print("  ", k, v)
    print()


# ---------------------------------------------------------------- 2026ZJA-96
# 要求：升级提星 U -> (设施完备 F 且 通过考核 P)。问：哪些情形说明“没有遵守要求”（即要求被违反）。
def q_zja96():
    names = ["U", "F", "P"]
    rule = lambda e: imp(e["U"], e["F"] and e["P"])
    cases = {
        "(1) 升级 且 未通过考核": lambda e: e["U"] and not e["P"],
        "(2) 升级 且 设施不完备": lambda e: e["U"] and not e["F"],
        "(3) 设施完备 且 通过 且 未升级": lambda e: e["F"] and e["P"] and not e["U"],
    }
    res = {}
    for k, c in cases.items():
        # 情形 c 成立时，规则是否必然被违反
        ok, n = entails(names, [c], lambda e: not rule(e))
        res[k] = "必然违反要求" if ok else "不构成违反"
    show("2026ZJA-96", res)
    # 选项 A=(1)(2) B=(2)(3) C=(3) D=(1)(2)(3)
    viol = {i for i, k in enumerate(cases, 1) if res[k] == "必然违反要求"}
    opts = {"A": {1, 2}, "B": {2, 3}, "C": {3}, "D": {1, 2, 3}}
    print("  answer:", [o for o, s in opts.items() if s == viol], "\n")


# ---------------------------------------------------------------- 2026GD-51
# J 集约高效 -> D 资源消耗量减少； (D 且 Sl 减少缓慢) -> 非 N（不造成负面影响）
def q_gd51():
    names = ["J", "D", "Sl", "N"]
    prem = [lambda e: imp(e["J"], e["D"]),
            lambda e: imp(e["D"] and e["Sl"], not e["N"])]
    opts = {
        "A 非D -> 非J": lambda e: imp(not e["D"], not e["J"]),
        "B 非J -> 非D": lambda e: imp(not e["J"], not e["D"]),
        "C D -> J": lambda e: imp(e["D"], e["J"]),
        "D (D且非Sl) -> N": lambda e: imp(e["D"] and not e["Sl"], e["N"]),
    }
    show("2026GD-51", {k: entails(names, prem, c)[0] for k, c in opts.items()})


# ---------------------------------------------------------------- 2026GK-111
# S 三医协同；W 提高卫生事业水平；Co 部门密切合作；D 深化医改领导体制和推进机制；
# R 强化规划刚性约束；E 更好满足新期待；G 提高获得感幸福感安全感
def q_gk111():
    names = ["S", "W", "Co", "D", "R", "E", "G"]
    base = [lambda e: imp(e["S"], e["W"] and e["Co"]),   # 只有 W且Co 才 S
            lambda e: imp(e["S"], e["D"]),                # 只有 D 才 S
            lambda e: imp(e["D"], e["R"])]                # D 必须 R
    # 读法1（常规）：只有D，才能E，进而G  ->  E->D 且 G->D（D 是 E、G 的必要条件）
    read1 = base + [lambda e: imp(e["E"], e["D"]), lambda e: imp(e["G"], e["D"])]
    # 读法2（严格）：E->D，且 E->G（“进而”只表示 E 导致 G）
    read2 = base + [lambda e: imp(e["E"], e["D"]), lambda e: imp(e["E"], e["G"])]
    opts = {
        "A W -> Co": lambda e: imp(e["W"], e["Co"]),
        "B G -> R（只有R才G）": lambda e: imp(e["G"], e["R"]),
        "C D -> S": lambda e: imp(e["D"], e["S"]),
        "D 非E -> 非S": lambda e: imp(not e["E"], not e["S"]),
    }
    show("2026GK-111 读法1 (G->D)", {k: entails(names, read1, c)[0] for k, c in opts.items()})
    show("2026GK-111 读法2 (E->G)", {k: entails(names, read2, c)[0] for k, c in opts.items()})


# ---------------------------------------------------------------- 2026GD-54
# K 科技馆 W 文化馆 B 博物馆 M 美术馆
def q_gd54():
    names = ["K", "W", "B", "M"]
    prem = [lambda e: not (e["K"] and e["W"] and e["B"] and e["M"]),  # 4 个不能都去
            lambda e: not (e["W"] and e["B"]),                          # (1)
            lambda e: e["M"] or e["W"],                                 # (2)
            lambda e: not e["M"]]                                       # (3)
    opts = {
        "A 非K -> B": lambda e: imp(not e["K"], e["B"]),
        "B 只有非K才B: B -> 非K": lambda e: imp(e["B"], not e["K"]),
        "C 只有非B才非K: 非K -> 非B": lambda e: imp(not e["K"], not e["B"]),
        "D B -> 非K": lambda e: imp(e["B"], not e["K"]),
    }
    res = {}
    for k, c in opts.items():
        ok, n = entails(names, prem + [c], lambda e: e["K"])
        res[k] = ("推出必去科技馆" if ok else "推不出") + f"（模型数 {n}）"
    show("2026GD-54", res)


# ---------------------------------------------------------------- 2026ZJA-99
# 比较两命题 X、Y 之间允许的真值组合（关系）。
def allowed(rel):
    return {(x, y) for x, y in product([0, 1], repeat=2) if rel(bool(x), bool(y))}


def q_zja99():
    # 但使龙城飞将在(X)，不教胡马度阴山(Y)：X -> 非Y
    stem = allowed(lambda x, y: imp(x, not y))
    opts = {
        # 不破楼兰(非X)终不还(非Y)：非X -> 非Y   （X=破楼兰, Y=还）
        "A": allowed(lambda x, y: imp(not x, not y)),
        # 清如许(X) 因为 源头活水来(Y)：Y -> X（因果读作充分）；另一读法 X -> Y
        "B(Y->X)": allowed(lambda x, y: imp(y, x)),
        "B(X->Y)": allowed(lambda x, y: imp(x, y)),
        # 不畏浮云遮望眼 因为 身在最高层：身在最高层(Y) -> 浮云不能遮望眼(非X)
        "C": allowed(lambda x, y: imp(y, not x)),
        # 若非群玉山头见(非X)，会向瑶台月下逢(Y)：非X -> Y
        "D": allowed(lambda x, y: imp(not x, y)),
    }
    print("== 2026ZJA-99")
    print("   stem allowed (X,Y):", sorted(stem))
    for k, s in opts.items():
        print("  ", k, sorted(s), "SAME" if s == stem else "diff")
    print()


if __name__ == "__main__":
    q_zja96()
    q_gd51()
    q_gk111()
    q_gd54()
    q_zja99()
