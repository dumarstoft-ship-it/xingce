# L01 翻译推理 —— 对有官方答案的可形式化真题做独立复核（真值表/集合模型穷举），
# 并对 4 道"答案待 OCR"的真题给出程序预判，供 OCR 结果核对。
# 输出：每题 程序答案 / 官方答案 / 是否一致；若某题有不止一个选项满足设问，打印出来。
import itertools

def imp(a, b):
    return (not a) or b

def xor(a, b):
    return a != b

def models(names, premises):
    for vals in itertools.product([False, True], repeat=len(names)):
        m = dict(zip(names, vals))
        if all(p(m) for p in premises):
            yield m

def entails(names, premises, concl):
    ms = list(models(names, premises))
    assert ms, "题干不相容"
    return all(concl(m) for m in ms)

def consistent(names, premises):
    return any(True for _ in models(names, premises))

def bridge(names, premises, option, target):
    """补充 option 后能推出 target，且补充后仍相容"""
    return consistent(names, premises + [option]) and entails(names, premises + [option], target)

out = []
def record(qid, status, official):
    hits = sorted(k for k, v in status.items() if v)
    ans = hits[0] if len(hits) == 1 else "/".join(hits) if hits else "无"
    flag = "OK" if (len(hits) == 1 and (official is None or hits[0] == official)) else "CHECK"
    out.append((qid, ans, official, flag))

# ---------------- 命题逻辑题 ----------------
# 2020HB-102  ¬J ∧ ¬C → W（J=激流勇进创造产品, C=适时撤退, W=陷入危机）；设问"说法正确"，C项为"可能"
n = ["J", "C", "W"]; P = [lambda m: imp(not m["J"] and not m["C"], m["W"])]
record("2020HB-102", {
    "A": entails(n, P, lambda m: imp(not m["J"], m["W"])),
    "B": entails(n, P, lambda m: imp(m["C"], not m["W"])),
    "C": consistent(n, P + [lambda m: m["C"] and m["J"] and not m["W"]]),   # 可能不会陷入危机
    "D": entails(n, P, lambda m: imp(m["J"], not m["W"])),
}, "C")

# 2020JSA-91  ¬(认识∧解决)→被动；¬(认识∧解决)→¬根本；看清本质→分析；抓住根本→解决
n = ["RS", "JJ", "BD", "GB", "FX", "KQ", "ZG"]
P = [lambda m: imp(not (m["RS"] and m["JJ"]), m["BD"]),
     lambda m: imp(not (m["RS"] and m["JJ"]), not m["GB"]),
     lambda m: imp(m["KQ"], m["FX"]),
     lambda m: imp(m["ZG"], m["JJ"])]
record("2020JSA-91", {
    "A": entails(n, P, lambda m: imp(m["GB"], m["RS"] and m["JJ"])),
    "B": False,   # "提高政治能力"未被条件化，推不出（无对应变量）
    "C": entails(n, P, lambda m: imp(m["BD"], not m["GB"])),
    "D": entails(n, P, lambda m: imp(not m["KQ"] and not m["ZG"], not m["FX"] and not m["JJ"])),
}, "A")

# 2020SC1206-81
n = ["NJ", "MQ", "JZ", "TG", "HF", "JH"]
P = [lambda m: imp(not m["NJ"], m["JZ"]), lambda m: imp(not m["MQ"], not m["TG"]),
     lambda m: not (m["NJ"] and m["MQ"]), lambda m: imp(not m["TG"], not m["HF"]),
     lambda m: imp(not m["HF"], not m["JH"]), lambda m: m["JH"]]
record("2020SC1206-81", {
    "A": entails(n, P, lambda m: not m["NJ"]), "B": entails(n, P, lambda m: not m["MQ"]),
    "C": entails(n, P, lambda m: not m["JZ"]), "D": False}, "A")

# 2020SD-73
n = ["H", "W", "K", "F", "G"]
P = [lambda m: imp(m["W"] and m["K"] and m["F"], m["H"]), lambda m: imp(not m["W"], not m["K"]),
     lambda m: imp(not m["K"], not m["G"]), lambda m: not m["H"], lambda m: m["G"]]
record("2020SD-73", {
    "A": entails(n, P, lambda m: m["W"] and m["K"] and m["F"]), "B": entails(n, P, lambda m: m["W"] and m["K"]),
    "C": entails(n, P, lambda m: m["K"] and m["F"]), "D": entails(n, P, lambda m: m["W"] and m["F"])}, "B")

# 2020SZ1-36
n = ["U", "Q", "W", "H", "M", "Y", "K"]
P = [lambda m: imp(m["U"], m["Q"] or m["W"]), lambda m: imp(m["Q"] or m["W"], m["H"] and m["M"]),
     lambda m: imp(m["M"], m["Y"] and m["K"]), lambda m: not m["K"]]
record("2020SZ1-36", {
    "A": entails(n, P, lambda m: xor(m["Q"], m["W"])), "B": entails(n, P, lambda m: not m["H"] and not m["M"]),
    "C": entails(n, P, lambda m: not m["U"]), "D": False}, "C")

# 2021JSA-91
n = ["RJ", "RL", "GJ", "GQ", "GD", "FY"]
P = [lambda m: imp(not m["RJ"], not m["RL"]), lambda m: imp(not m["GJ"], not m["GQ"]),
     lambda m: imp(m["FY"], m["GD"])]
record("2021JSA-91", {
    "A": entails(n, P, lambda m: imp(m["RJ"], m["RL"]) and imp(m["GJ"], m["GQ"])),
    "B": False, "C": entails(n, P, lambda m: imp(m["FY"], m["GD"])),
    "D": entails(n, P, lambda m: imp(m["GD"], m["FY"]))}, "C")

# 2021SC2-83  落地L→抓基层J；提质Q→改革G
n = ["L", "J", "Q", "G"]; P = [lambda m: imp(m["L"], m["J"]), lambda m: imp(m["Q"], m["G"])]
record("2021SC2-83", {
    "A": entails(n, P, lambda m: imp(not m["J"], not m["Q"])), "B": entails(n, P, lambda m: imp(m["J"], m["L"])),
    "C": entails(n, P, lambda m: imp(not m["G"], not m["Q"])), "D": entails(n, P, lambda m: imp(m["G"], m["Q"]))}, "C")

# 2022GD-59  羽Y∧体T→登S，对个体逐一判断
n = ["Y", "T", "S"]; P = [lambda m: imp(m["Y"] and m["T"], m["S"])]
record("2022GD-59", {
    "A": entails(n, P, lambda m: imp(m["Y"] and m["S"], m["T"])),
    "B": entails(n, P, lambda m: imp(m["T"] and m["S"], m["Y"])),
    "C": entails(n, P, lambda m: imp(not m["Y"] and not m["S"], not m["T"])),
    "D": entails(n, P, lambda m: imp(m["Y"] and not m["S"], not m["T"]))}, "D")

# 2023JSA-91（选"不能推出"）
n = ["SL", "XL", "QS", "JD", "GY", "QG", "RB", "MS"]
P = [lambda m: imp(m["SL"], m["XL"]), lambda m: imp(m["JD"], m["GY"]),
     lambda m: imp(m["QS"] or not m["JD"], m["QG"] and m["RB"] and m["MS"])]
st = {"A": entails(n, P, lambda m: imp(not m["SL"], not m["XL"])),
      "B": entails(n, P, lambda m: imp(not m["GY"], not m["JD"])),
      "C": entails(n, P, lambda m: imp(m["QS"], m["RB"])),
      "D": entails(n, P, lambda m: imp(not m["MS"], m["JD"]))}
record("2023JSA-91", {k: not v for k, v in st.items()}, "A")

# 2024GD-51  ¬J→K；K→Z；S→L；良性循环 L→¬K
n = ["J", "K", "Z", "L", "S"]
P = [lambda m: imp(not m["J"], m["K"]), lambda m: imp(m["K"], m["Z"]),
     lambda m: imp(m["S"], m["L"]), lambda m: imp(m["L"], not m["K"])]
record("2024GD-51", {
    "A": entails(n, P, lambda m: imp(not m["K"], m["S"])), "B": entails(n, P, lambda m: imp(m["J"], m["S"])),
    "C": entails(n, P, lambda m: imp(not m["Z"], m["J"])), "D": entails(n, P, lambda m: imp(not m["S"], not m["L"]))}, "C")

# 2024GK-106  源泉S→扎根R
n = ["S", "R", "X1", "X2"]; P = [lambda m: imp(m["S"], m["R"])]
record("2024GK-106", {"A": False, "B": entails(n, P, lambda m: imp(not m["R"], not m["S"])), "C": False,
                      "D": entails(n, P, lambda m: imp(not m["X1"], not m["X2"]))}, "B")

# 2024JSA-91  飞F→W∧G，①~④组合
n = ["F", "W", "G"]; P = [lambda m: imp(m["F"], m["W"] and m["G"])]
s = {1: entails(n, P, lambda m: imp(m["W"] and m["G"], m["F"])),
     2: entails(n, P, lambda m: imp(m["F"], m["W"] and m["G"])),
     3: entails(n, P, lambda m: imp(not m["W"] or not m["G"], not m["F"])),
     4: entails(n, P, lambda m: imp(not m["F"], not m["W"] or not m["G"]))}
vs = {i for i, v in s.items() if v}
record("2024JSA-91", {k: vs == c for k, c in {"A": {1, 2}, "B": {2, 3}, "C": {3, 4}, "D": {2, 4}}.items()}, "B")

# 2024JSA-92（选"不可能为真"）
n = ["A", "B", "C", "D"]
P = [lambda m: imp(m["A"], m["B"]), lambda m: imp(m["C"], not m["D"]), lambda m: imp(m["B"], m["C"])]
record("2024JSA-92", {
    "A": not consistent(n, P + [lambda m: m["A"] and m["C"]]),
    "B": not consistent(n, P + [lambda m: m["D"] and not m["B"]]),
    "C": not consistent(n, P + [lambda m: m["A"] and m["D"]]),
    "D": not consistent(n, P + [lambda m: m["A"] and not m["D"]])}, "C")

# 2024SD-97  实施S→坚持J
n = ["S", "J", "G"]; P = [lambda m: imp(m["S"], m["J"])]
record("2024SD-97", {"A": entails(n, P, lambda m: imp(not m["S"], not m["G"])),
                     "B": entails(n, P, lambda m: imp(m["G"], m["S"])),
                     "C": entails(n, P, lambda m: imp(m["J"], m["S"])),
                     "D": entails(n, P, lambda m: imp(not m["J"], not m["S"]))}, "D")

# 2025JSA-91
n = ["YY", "WR", "DL", "YK", "JW", "JY", "DD"]
P = [lambda m: imp(m["YY"], m["WR"]), lambda m: imp(m["DL"], m["YK"]),
     lambda m: imp(m["JW"] and m["JY"], m["DD"])]
record("2025JSA-91", {"A": entails(n, P, lambda m: imp(not m["WR"], not m["YY"])), "B": False,
                      "C": entails(n, P, lambda m: imp(not m["DD"], not m["JW"])),
                      "D": entails(n, P, lambda m: imp(m["DD"], m["JY"]))}, "A")

# 2020SC0725-85  玫瑰R 郁金香T 牡丹P 雏菊D 百合L
n = ["R", "T", "P", "D", "L"]
P = [lambda m: not (m["R"] and m["T"]), lambda m: m["P"] or m["R"] or m["D"],
     lambda m: m["T"] + m["D"] + m["L"] >= 2, lambda m: imp(m["T"], not m["P"])]
record("2020SC0725-85", {"A": entails(n, P, lambda m: m["L"]), "B": entails(n, P, lambda m: m["T"] or m["P"]),
                         "C": entails(n, P, lambda m: m["D"] or m["R"]),
                         "D": entails(n, P, lambda m: sum(m.values()) >= 3)}, "C")

# 2020ZJB-63  ¬举措R→¬增长G；¬G→攀升D
n = ["R", "G", "D"]; P = [lambda m: imp(not m["R"], not m["G"]), lambda m: imp(not m["G"], m["D"])]
record("2020ZJB-63", {"A": entails(n, P, lambda m: imp(m["D"], not m["R"])),
                      "B": entails(n, P, lambda m: imp(m["D"], not m["R"])),
                      "C": entails(n, P, lambda m: imp(m["R"], not m["D"])),
                      "D": entails(n, P, lambda m: imp(not m["D"], m["R"]))}, "D")

# 2021JSA-97 / 2023GD-71 / 2024ZJA-103（同一模板）：X或Y；X→¬Z；某人Z；目标 W
for qid in ["2021JSA-97", "2023GD-71", "2024ZJA-103"]:
    n = ["X", "Y", "Z", "W"]
    P = [lambda m: m["X"] or m["Y"], lambda m: imp(m["X"], not m["Z"]), lambda m: m["Z"]]
    T = lambda m: m["W"]
    if qid == "2021JSA-97":    # X诗词 Y书法 Z合唱 W戏迷；A 李没诗词 B 戏迷→书法 C 李没书法 D ¬戏迷→¬书法
        o = {"A": lambda m: not m["X"], "B": lambda m: imp(m["W"], m["Y"]), "C": lambda m: not m["Y"],
             "D": lambda m: imp(not m["W"], not m["Y"])}
    elif qid == "2023GD-71":   # X跑步 Y羽毛球 Z篮球 W排球；A 没跑步 B 没羽毛球 C 排球→羽毛球 D ¬排球→¬羽毛球
        o = {"A": lambda m: not m["X"], "B": lambda m: not m["Y"], "C": lambda m: imp(m["W"], m["Y"]),
             "D": lambda m: imp(not m["W"], not m["Y"])}
    else:                      # X艺术阅读 Y版画 Z书法小课堂 W剪纸；A 没艺术阅读 B 没版画 C 剪纸→版画 D ¬剪纸→¬版画
        o = {"A": lambda m: not m["X"], "B": lambda m: not m["Y"], "C": lambda m: imp(m["W"], m["Y"]),
             "D": lambda m: imp(not m["W"], not m["Y"])}
    record(qid, {k: bridge(n, P, f, T) for k, f in o.items()}, "D")

# 2022GD-57  名正A 言顺B 事成C 礼乐兴D 刑罚中E 民措F；¬A→¬B→¬C→¬D→¬E→¬F
n = ["A", "B", "C", "D", "E", "F"]
P = [lambda m: imp(not m["A"], not m["B"]), lambda m: imp(not m["B"], not m["C"]),
     lambda m: imp(not m["C"], not m["D"]), lambda m: imp(not m["D"], not m["E"]),
     lambda m: imp(not m["E"], not m["F"])]
s = {1: entails(n, P, lambda m: imp(m["A"], m["B"])), 2: entails(n, P, lambda m: imp(m["D"], m["C"])),
     3: entails(n, P, lambda m: imp(not m["A"], not m["F"])), 4: entails(n, P, lambda m: imp(m["C"], m["A"] and m["B"]))}
vs = {i for i, v in s.items() if v}
record("2022GD-57", {k: vs == c for k, c in {"A": {1, 2}, "B": {2, 3}, "C": {2, 3, 4}, "D": {1, 2, 3, 4}}.items()}, "C")

# 2022GK-111  五柜五矿一一对应
minerals = ["赤", "黑", "绿", "黄", "方"]
sols = []
for perm in itertools.permutations(minerals):
    c = dict(zip([1, 2, 3, 4, 5], perm))
    ok = imp(c[1] == "赤", c[2] != "黑") and (c[3] == "赤" or c[1] == "赤") and \
         imp(c[2] != "黑", c[4] != "绿") and imp(c[5] == "方", c[4] == "绿")
    if ok:
        sols.append(c)
o = {"A": lambda c: c[2] != "黑", "B": lambda c: c[1] != "黄", "C": lambda c: c[5] == "方", "D": lambda c: c[4] != "绿"}
record("2022GK-111", {k: any(f(c) for c in sols) and all(c[3] == "赤" for c in sols if f(c)) for k, f in o.items()}, "C")

# 2023GK-114
n = ["W", "Z", "DG", "JS", "YS", "FG", "NS"]
P = [lambda m: imp(m["W"], m["Z"]), lambda m: imp(m["DG"], m["JS"]),
     lambda m: imp(m["YS"], m["JS"] and m["FG"]), lambda m: imp(m["NS"], m["YS"])]
record("2023GK-114", {"A": entails(n, P, lambda m: imp(m["DG"], m["JS"])), "B": entails(n, P, lambda m: imp(m["Z"], m["W"])),
                      "C": entails(n, P, lambda m: imp(m["FG"], m["YS"])), "D": False}, "A")

# 2023SC-84  三条建议都没采纳 = 三个命题都为假
n = ["S", "T", "M"]
P = [lambda m: not imp(m["S"], not m["M"]), lambda m: not xor(m["T"], m["M"]), lambda m: not (not m["T"] and not m["M"])]
o = {"A": lambda m: m["S"] and m["T"] and m["M"], "B": lambda m: m["T"] and m["M"] and not m["S"],
     "C": lambda m: m["S"] and not m["T"] and not m["M"], "D": lambda m: not m["S"] and not m["T"] and m["M"]}
record("2023SC-84", {k: entails(n, P, f) for k, f in o.items()}, "A")

# 2024GK-115
n = ["A", "B", "C", "D"]
P = [lambda m: imp(not m["A"] and not m["B"], m["C"]), lambda m: imp(m["B"] or m["C"], m["D"]),
     lambda m: imp(m["A"] or m["B"], m["C"] and not m["D"])]
o = {"A": lambda m: m["C"] and m["D"], "B": lambda m: m["A"] and m["D"], "C": lambda m: m["A"] and m["B"],
     "D": lambda m: m["B"] and m["C"]}
record("2024GK-115", {k: entails(n, P, f) for k, f in o.items()}, "A")

# 2024SZ-36（疑问题）：漂流P→55以下Y∧救生衣J；病H→¬P；事实 J ∧ ¬P
n = ["P", "Y", "J", "H"]
P = [lambda m: imp(m["P"], m["Y"] and m["J"]), lambda m: imp(m["H"], not m["P"]), lambda m: m["J"], lambda m: not m["P"]]
o = {"A": lambda m: imp(not m["Y"], m["H"]), "B": lambda m: m["H"], "C": lambda m: not m["Y"] and m["H"],
     "D": lambda m: xor(not m["Y"], m["H"])}
st = {k: entails(n, P, f) for k, f in o.items()}
# 再试"规则穷尽"读法（满足年龄+救生衣且无病就一定允许）
P2 = P + [lambda m: imp(m["Y"] and m["J"] and not m["H"], m["P"])]
st2 = {k: entails(n, P2, f) for k, f in o.items()}
incl = entails(n, P2, lambda m: (not m["Y"]) or m["H"])
out.append(("2024SZ-36", "严格读法无选项成立" if not any(st.values()) else str(st), "D",
            "CHECK(规则穷尽读法下: D(要么…要么)成立={}；相容或'年满55或有病'成立={})".format(st2["D"], incl)))

# 2025GD-55  ¬体魄T→¬状态S；¬S→¬成绩G；结论 G→体育课K
n = ["T", "S", "G", "K"]
P = [lambda m: imp(not m["T"], not m["S"]), lambda m: imp(not m["S"], not m["G"])]
target = lambda m: imp(m["G"], m["K"])
o = {"A": lambda m: imp(m["T"], m["K"]), "B": lambda m: True, "C": lambda m: True, "D": lambda m: True}
record("2025GD-55", {k: entails(n, P + [f], target) for k, f in o.items()}, "A")

# 2025GD-64  欢乐H 动物Z 艺术A 人民P 博物B
n = ["H", "Z", "A", "P", "B"]
P = [lambda m: m["H"] or m["Z"], lambda m: m["A"] or m["H"] or m["P"],
     lambda m: m["Z"] + m["P"] + m["B"] >= 2, lambda m: imp(m["Z"], not m["A"])]
o = {"A": lambda m: m["B"], "B": lambda m: m["Z"] or m["A"], "C": lambda m: m["P"] or m["H"],
     "D": lambda m: sum(m.values()) >= 3}
record("2025GD-64", {k: entails(n, P, f) for k, f in o.items()}, "C")

# 2025GK-113
n = ["G", "T", "R", "S", "F", "E", "K", "L"]
P = [lambda m: imp(m["G"], m["T"] and m["R"]), lambda m: imp(m["T"], m["S"]),
     lambda m: imp(m["S"], m["F"] and m["E"]), lambda m: imp(m["R"], m["K"] and m["L"])]
o = {"A": lambda m: imp(m["S"], m["T"]), "B": lambda m: imp(m["L"], m["K"]),
     "C": lambda m: imp(m["R"], m["F"] and m["E"]), "D": lambda m: imp(m["G"], m["K"] and m["L"])}
record("2025GK-113", {k: entails(n, P, f) for k, f in o.items()}, "D")

# 2025GK-115  甲a 乙b 丙c 丁d 戊e 己f 庚g
n = list("abcdefg")
P = [lambda m: m["e"] + m["f"] + m["g"] >= 2, lambda m: imp(m["a"] or m["c"] or m["e"], not m["d"] and not m["f"]),
     lambda m: imp(m["b"] or m["e"] or m["f"], m["d"] and not m["c"])]
record("2025GK-115", {k: entails(n, P, lambda m, v=v: m[v]) for k, v in {"A": "a", "B": "b", "C": "c", "D": "d"}.items()}, "D")

# 2025JSA-103  四人四项一一对应
people = ["全", "陈", "吴", "刘"]; sports = ["游泳", "跳水", "水球", "赛艇"]
sols = []
for perm in itertools.permutations(sports):
    a = dict(zip(people, perm))
    ok = imp(a["全"] == "游泳", a["陈"] != "跳水") and imp(a["刘"] == "水球", a["陈"] == "跳水") and \
         xor(a["吴"] == "游泳", a["全"] == "游泳") and xor(a["全"] != "赛艇", a["刘"] == "水球")
    if ok:
        sols.append(a)
o = {"A": lambda a: a["全"] == "赛艇", "B": lambda a: a["陈"] != "跳水", "C": lambda a: a["陈"] == "水球",
     "D": lambda a: a["刘"] != "水球"}
record("2025JSA-103", {k: any(f(a) for a in sols) and all(a["吴"] == "游泳" for a in sols if f(a)) for k, f in o.items()}, "A")

# ---- 待 OCR：2022SC1-79 / 2023SZ-41 ----
n = ["RY", "BZ", "XC", "CG", "XL", "XD"]
P = [lambda m: imp(m["RY"], m["BZ"]), lambda m: imp(m["XC"], m["CG"]), lambda m: imp(m["XD"], m["XL"])]
st = {"A": entails(n, P, lambda m: imp(not m["RY"], not m["BZ"])), "B": entails(n, P, lambda m: imp(m["XD"], m["XL"])),
      "C": consistent(n, P + [lambda m: m["XC"] and not m["CG"]]) and False,  # 与题干矛盾，不能推出
      "D": entails(n, P, lambda m: imp(m["CG"], m["XC"]))}
record("2022SC1-79(待OCR)", st, None)

n = ["CY", "WT", "XH", "QN", "XX", "YD", "SJ"]
P = [lambda m: imp(m["CY"], m["WT"] and m["XH"]), lambda m: imp(m["WT"] or m["QN"], m["XX"]),
     lambda m: imp(m["XX"], m["YD"]), lambda m: imp(m["YD"], m["SJ"]), lambda m: not m["SJ"]]
record("2023SZ-41(待OCR)", {"A": entails(n, P, lambda m: not m["CY"]), "B": entails(n, P, lambda m: m["QN"]),
                            "C": entails(n, P, lambda m: m["XH"]), "D": entails(n, P, lambda m: m["XX"])}, None)

# ---------------- 直言命题：集合模型 ----------------
# 模型 = 若干"类型"(各谓词真假组合)的非空集合；全称命题限制允许的类型；特称命题要求有见证类型。
def cat_models(preds, universals, existentials, extra_exist=()):
    types = [dict(zip(preds, v)) for v in itertools.product([False, True], repeat=len(preds))]
    allowed = [t for t in types if all(u(t) for u in universals)]
    return types, allowed

def cat_entails_universal(preds, U, E, f):
    _, allowed = cat_models(preds, U, E)
    if not all(any(e(t) for t in allowed) for e in E):
        raise ValueError("前提不相容")
    return not any(not f(t) for t in allowed)

def cat_entails_exist(preds, U, E, g):
    _, allowed = cat_models(preds, U, E)
    rest = [t for t in allowed if not g(t)]
    return not (rest and all(any(e(t) for t in rest) for e in E))

def cat_impossible(preds, U, E, h):
    _, allowed = cat_models(preds, U, E)
    return not any(h(t) for t in allowed)

# 2025ZJA-101  正式Z 团建T 后勤H 综合C
pr = ["Z", "T", "H", "C"]
U = [lambda t: imp(t["Z"], t["T"]), lambda t: imp(t["H"], not t["Z"])]
E = [lambda t: t["C"] and not t["T"]]
record("2025ZJA-101", {
    "A": cat_entails_exist(pr, U, E, lambda t: t["C"] and not t["Z"]),
    "B": cat_entails_exist(pr, U, E, lambda t: t["Z"] and not t["C"]),
    "C": cat_entails_exist(pr, U, E, lambda t: t["H"] and not t["T"]),
    "D": cat_entails_universal(pr, U, E, lambda t: imp(t["H"], t["T"]))}, "A")

# 2020SZS-68  环保主义E 爱旅游T 企业代表R 支持减少S 反对减少O（S、O不同真）
pr = ["E", "T", "R", "S", "O"]
U = [lambda t: imp(t["R"], t["S"]), lambda t: imp(t["T"], t["O"]), lambda t: not (t["S"] and t["O"])]
E = [lambda t: t["E"] and t["T"]]
record("2020SZS-68", {
    "A": cat_entails_universal(pr, U, E, lambda t: imp(t["E"], t["O"])),
    "B": cat_entails_universal(pr, U, E, lambda t: imp(t["R"], not t["T"])),
    "C": False,
    "D": cat_entails_exist(pr, U, E, lambda t: t["E"] and t["S"])}, "B")

# 2023GD-73  干部G 博士B 统计S 男M 工勤W
pr = ["G", "B", "S", "M", "W"]
U = [lambda t: imp(t["M"], t["S"])]
E = [lambda t: t["G"] and t["B"], lambda t: t["B"] and not t["S"]]
record("2023GD-73", {
    "A": cat_entails_exist(pr, U, E, lambda t: t["M"] and not t["B"]),
    "B": cat_entails_exist(pr, U, E, lambda t: t["B"] and not t["M"]),
    "C": cat_entails_exist(pr, U, E, lambda t: t["M"] and t["W"]),
    "D": cat_entails_exist(pr, U, E, lambda t: t["G"] and not t["S"])}, "B")

# 2023SD-68（选"一定为假"）法学F 法律证L 教师证T 公务员G 逻辑学J
pr = ["F", "L", "T", "G", "J"]
U = [lambda t: imp(t["F"], t["L"]), lambda t: imp(t["L"], t["T"]), lambda t: imp(t["J"], not t["T"])]
E = [lambda t: t["F"] and t["G"], lambda t: t["J"] and t["G"]]
record("2023SD-68", {
    "A": cat_impossible(pr, U, E, lambda t: t["T"] and not t["J"]),
    "B": cat_impossible(pr, U, E, lambda t: t["G"] and not t["L"] and not t["J"]),
    "C": cat_impossible(pr, U, E, lambda t: t["L"] and not t["F"]),
    "D": cat_impossible(pr, U, E, lambda t: t["J"] and t["L"])}, "D")

# 2024JSA-101（选"不能推出"）800米E 100米H 跳高G 跳远Y 链球L
pr = ["E", "H", "G", "Y", "L"]
U = [lambda t: imp(t["E"], t["H"]), lambda t: imp(t["H"], t["G"]), lambda t: imp(t["Y"], not t["G"])]
E = [lambda t: t["Y"] and t["L"]]
st = {"A": cat_entails_universal(pr, U, E, lambda t: imp(t["E"], t["G"])),
      "B": cat_entails_universal(pr, U, E, lambda t: imp(t["L"], not t["G"])),
      "C": cat_entails_universal(pr, U, E, lambda t: imp(t["Y"], not t["H"])),
      "D": cat_entails_exist(pr, U, E, lambda t: t["E"] and t["Y"])}
record("2024JSA-101", {k: not v for k, v in st.items()}, "D")
d_false = cat_impossible(pr, U, E, lambda t: t["E"] and t["Y"])
out.append(("2024JSA-101附注", "D项一定为假={}；B项只是不能推出(可真可假)".format(d_false), "D", "择优"))

# 2020SZ1-31  上位者S 缺乏Q 不愿动脑N；论据：有的S是N；结论：有的S是Q
pr = ["S", "Q", "N"]
E = [lambda t: t["S"] and t["N"]]
concl = lambda t: t["S"] and t["Q"]
opt = {"A": ([lambda t: True], []), "B": ([], [lambda t: t["N"] and not t["Q"]]),
       "C": ([], [lambda t: t["Q"] and t["N"]]), "D": ([lambda t: imp(t["N"], t["Q"])], [])}
record("2020SZ1-31", {k: cat_entails_exist(pr, u, E + e, concl) for k, (u, e) in opt.items()}, "D")

# 2020SZS-70  错绘C 有损H 违法V；论据：H→V；结论：有的C是V；"必须补充"取最弱的充分前提
pr = ["C", "H", "V"]
U0 = [lambda t: imp(t["H"], t["V"])]
concl = lambda t: t["C"] and t["V"]
opt = {"A": ([], []), "B": ([], [lambda t: t["V"] and t["H"]]),
       "C": ([lambda t: imp(t["C"], t["H"])], [lambda t: t["C"]]),     # 全称作前提时默认主项存在
       "D": ([], [lambda t: t["C"] and t["H"]])}
suff = {k: cat_entails_exist(pr, U0 + u, e, concl) if e else False for k, (u, e) in opt.items()}
# C、D 都充分；D 被 C 蕴含（C + 主项存在 ⇒ D），故必要前提为 D
c_implies_d = cat_entails_exist(pr, U0 + opt["C"][0], opt["C"][1], lambda t: t["C"] and t["H"])
record("2020SZS-70", {"A": False, "B": False, "C": suff["C"] and not c_implies_d, "D": suff["D"]}, "D")

# 2021SD-73（待OCR） 捷径J 弯路W 必经B 依附强者Y；J→W→B；结论 Y→¬J；考试默认"捷径"存在
pr = ["J", "W", "B", "Y"]
U0 = [lambda t: imp(t["J"], t["W"]), lambda t: imp(t["W"], t["B"])]
E0 = [lambda t: t["J"], lambda t: t["Y"]]
concl = lambda t: imp(t["Y"], not t["J"])
opt = {"A": [lambda t: imp(t["J"], t["B"])], "B": [lambda t: imp(t["Y"], not t["B"])],
       "C": [lambda t: imp(t["W"], not t["J"])], "D": [lambda t: imp(t["Y"], t["W"])]}
def ok_premise(u):
    _, allowed = cat_models(pr, U0 + u, E0)
    if not all(any(e(t) for t in allowed) for e in E0):
        return False            # 与"捷径存在"相矛盾，不能作为前提
    return cat_entails_universal(pr, U0 + u, E0, concl)
record("2021SD-73(待OCR)", {k: ok_premise(u) for k, u in opt.items()}, None)

# 2021SD-69（待OCR）：用人数穷举，N 人，工学>N/2，已就业>N/2，人文社科>0
def sd69():
    res = {"A": True, "B": True, "C": True, "D": True}
    for N in range(2, 9):
        for eng in range(N // 2 + 1, N):          # 工学人数；其余至少1人为人文社科
            hum = N - eng
            for emp_e in range(0, eng + 1):
                for emp_h in range(0, hum + 1):
                    if emp_e + emp_h <= N / 2:
                        continue
                    res["A"] &= emp_e > eng / 2
                    res["B"] &= emp_h < hum
                    res["C"] &= emp_e >= 1
                    res["D"] &= emp_h >= 1
    return res
record("2021SD-69(待OCR)", sd69(), None)

# ---------------- 对当关系：2023SD-67 ----------------
def combos(pair_fn, worlds):
    return {pair_fn(w) for w in worlds}
lie_worlds = range(0, 5)                       # 说谎次数
stem = combos(lambda k: (k == 0, k >= 2), lie_worlds)
cls = list(itertools.product([False, True], repeat=3))   # 3 名同学/工作人员/科室人员的状态
opts = {
    "A": combos(lambda w: (any(w), not all(w)), cls),
    "B": combos(lambda w: (all(w), not all(w)), cls),
    "C": combos(lambda w: (all(w), not any(w)), cls),
    "D": combos(lambda w: w, list(itertools.product([False, True], repeat=2))),   # 过去与将来互不相关
}
record("2023SD-67", {k: v == stem for k, v in opts.items()}, "C")

w = max(len(r[0]) for r in out)
for qid, ans, off, flag in out:
    print(f"{qid:<{w}}  程序={ans:<6} 官方={str(off):<5} {flag}")
