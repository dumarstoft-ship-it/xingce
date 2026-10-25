# -*- coding: utf-8 -*-
"""综合推理（C01/C02/C03）穷举验证：列出全部满足条件的情形，再逐项判定选项“必然/可能”。"""
from itertools import permutations, product, combinations


def imp(a, b):
    return (not a) or b


def judge(title, sols, opts, mode):
    """mode='must'：选项在所有解中都成立；mode='may'：选项至少在一个解中成立。"""
    print("==", title, f"（解的个数 {len(sols)}）")
    for s in sols:
        print("   sol:", s)
    for k, f in opts.items():
        vals = [f(s) for s in sols]
        flag = all(vals) if mode == "must" else any(vals)
        print(f"   {k}: {'YES' if flag else 'no'}  ({sum(vals)}/{len(vals)})")
    print()


# ---------------------------------------------------------------- 2026GD-62
# 位置 1..6 从左到右；“右手边”= 序号更大。
def q_gd62():
    names = ["教育", "住建", "交通", "农业", "人社", "财政"]
    sols = []
    for perm in permutations(range(1, 7)):
        p = dict(zip(names, perm))
        if p["财政"] != p["人社"] + 1:                 # 财政在人社右边且相邻
            continue
        if not (p["住建"] > p["财政"] + 1):           # 财政在住建左边且不相邻
            continue
        if abs(p["教育"] - p["交通"]) != 2:           # 教育与交通之间隔一个
            continue
        if abs(p["农业"] - p["财政"]) != 1:           # 附加条件：农业与财政相邻
            continue
        sols.append(dict(sorted(p.items(), key=lambda kv: kv[1])))
    opts = {
        "A 教育局从右到左第三位(左起4)": lambda s: s["教育"] == 4,
        "B 住建局从右到左第二位(左起5)": lambda s: s["住建"] == 5,
        "C 交通局从左到右第三位": lambda s: s["交通"] == 3,
        "D 人社局从左到右第二位": lambda s: s["人社"] == 2,
    }
    judge("2026GD-62", sols, opts, "must")


# ---------------------------------------------------------------- 2026ZJA-97
def q_zja97():
    albums = ["A", "B", "C", "D", "E", "F"]   # 甲:A,B 乙:C,D 丙:E,F
    sols = []
    for perm in permutations(range(1, 7)):
        p = dict(zip(albums, perm))
        if abs(p["A"] - p["C"]) == 1 or abs(p["F"] - p["C"]) == 1:
            continue
        ends = sum(1 for x in ("A", "B") if p[x] in (1, 6))
        if ends != 1:
            continue
        if p["C"] != 2 or p["E"] != 4:
            continue
        sols.append("".join(sorted(albums, key=lambda a: p[a])))
    opts = {
        "A B在1号": lambda s: s[0] == "B",
        "B B在5号": lambda s: s[4] == "B",
        "C D在5号": lambda s: s[4] == "D",
        "D D在6号": lambda s: s[5] == "D",
    }
    judge("2026ZJA-97（货架1..6依次）", sols, opts, "may")


# ---------------------------------------------------------------- 2026GK-110
def q_gk110():
    people = ["甲", "乙", "丙", "丁", "戊", "己", "庚"]
    sols = []
    for chosen in combinations(people, 4):
        c = set(chosen)
        x = lambda n: n in c
        if x("甲") and x("丁"):
            continue
        if not imp(x("丙") or x("戊"), x("甲") and not x("己")):
            continue
        if not imp(x("乙") or x("庚"), x("丁") and not x("甲")):
            continue
        sols.append(chosen)
    opts = {
        "A 乙、庚": lambda s: "乙" in s and "庚" in s,
        "B 丙、丁": lambda s: "丙" in s and "丁" in s,
        "C 己、戊": lambda s: "己" in s and "戊" in s,
        "D 甲、乙": lambda s: "甲" in s and "乙" in s,
    }
    judge("2026GK-110", sols, opts, "must")


# ---------------------------------------------------------------- 2026ZJA-98
def q_zja98():
    people = ["琪琪", "依依", "冰冰", "鑫鑫", "磊磊", "静静"]
    sols = []
    for prizes in set(permutations([1, 2, 2, 3, 3, 3])):
        g = dict(zip(people, prizes))
        # (1) 除非琪琪二等，否则冰冰一等：非(琪琪=2) -> 冰冰=1
        if not imp(g["琪琪"] != 2, g["冰冰"] == 1):
            continue
        # (2) 只有 鑫鑫=3 且 静静=2，才 (琪琪=2 或 依依=2)
        if not imp(g["琪琪"] == 2 or g["依依"] == 2, g["鑫鑫"] == 3 and g["静静"] == 2):
            continue
        # (3) 鑫鑫=3 -> 冰冰=2 且 依依!=3
        if not imp(g["鑫鑫"] == 3, g["冰冰"] == 2 and g["依依"] != 3):
            continue
        sols.append(g)
    opts = {
        "A 冰冰未获一等奖": lambda s: s["冰冰"] != 1,
        "B 琪琪获二等奖": lambda s: s["琪琪"] == 2,
        "C 鑫鑫未获一等奖": lambda s: s["鑫鑫"] != 1,
        "D 磊磊获三等奖": lambda s: s["磊磊"] == 3,
    }
    judge("2026ZJA-98", sols, opts, "must")


# ---------------------------------------------------------------- 2026CQ-100
# 截图中条件(2)有“****”遮挡，按“如果……，那么只有丁去S值班点”理解（S 恰为{丁}）；
# 另附“丁去S”宽松读法作敏感性检查。
def q_cq100():
    people = ["甲", "乙", "丙", "丁", "戊", "己", "庚"]
    spots = "PQRS"

    def solve(strict):
        sols = []
        for assign in product(spots, repeat=7):
            a = dict(zip(people, assign))
            cnt = {s: assign.count(s) for s in spots}
            if any(cnt[s] < 1 or cnt[s] > 3 for s in spots):
                continue
            if cnt["Q"] != 3:
                continue
            if cnt["R"] != cnt["P"]:                              # (1)
                continue
            inQ = sum(1 for n in ("甲", "乙", "丙") if a[n] == "Q")
            S = {n for n in people if a[n] == "S"}
            cons2 = (S == {"丁"}) if strict else ("丁" in S)
            if not imp(inQ <= 2, cons2):                          # (2)
                continue
            # (3) 只有 乙和庚去S，丁或戊才不去S：(丁不去S 或 戊不去S) -> (乙去S 且 庚去S)
            if not imp(a["丁"] != "S" or a["戊"] != "S", a["乙"] == "S" and a["庚"] == "S"):
                continue
            sols.append("".join(a[n] for n in people))
        return sols

    opts = {
        "A 乙Q、戊S": lambda s: s[1] == "Q" and s[4] == "S",
        "B 甲Q、丁P": lambda s: s[0] == "Q" and s[3] == "P",
        "C 己P、庚R": lambda s: s[5] == "P" and s[6] == "R",
        "D 丙P、戊S": lambda s: s[2] == "P" and s[4] == "S",
    }
    judge("2026CQ-100 严格读法（只有丁去S = S恰为{丁}）（解按 甲乙丙丁戊己庚 顺序列地点）",
          solve(True), opts, "must")
    loose = solve(False)
    print("   [敏感性] 宽松读法（丁去S）解的个数:", len(loose))
    for k, f in opts.items():
        print("     ", k, "必然" if all(f(s) for s in loose) else "不必然")
    print()


# ---------------------------------------------------------------- 2026GD-63
# 收入用 1..4 的整数表示（允许并列）；“相当”= 相等；“都不是最高的”= 各自严格低于最高值。
def q_gd63(require_jia_not_da=True, xiangdang_equal=True):
    villages = ["甲", "乙", "丙", "丁"]
    awards = ["文旅", "非遗", "生态", "数字"]
    sols = []
    for perm in permutations(awards):
        aw = dict(zip(villages, perm))
        who = {v: k for k, v in aw.items()}
        if require_jia_not_da and aw["甲"] == "数字":
            continue
        for inc_vals in product(range(1, 5), repeat=4):
            inc = dict(zip(villages, inc_vals))
            top = max(inc_vals)
            if not inc[who["文旅"]] > inc["丙"]:            # ①
                continue
            if xiangdang_equal and inc["甲"] != inc[who["数字"]]:   # ② 相当
                continue
            if inc["甲"] == top or inc[who["数字"]] == top:   # ② 都不是最高
                continue
            if not inc[who["生态"]] > inc["丁"]:            # ③
                continue
            if not inc["丙"] > inc[who["非遗"]]:            # ④
                continue
            key = tuple(aw[v] for v in villages)
            sols.append((key, inc_vals))
    # 去重：同一获奖分配下记录可能的收入顺序
    by_award = {}
    for key, inc_vals in sols:
        by_award.setdefault(key, set()).add(inc_vals)
    summary = []
    for key, incs in by_award.items():
        # 甲是否在所有收入实现里都“位列第二”（严格只有一个更高、其余都不高于它）
        summary.append({"甲乙丙丁": key, "收入样例": sorted(incs)[0], "n_inc": len(incs)})

    def jia_second_always(key):
        for inc_vals in by_award[key]:
            inc = dict(zip(villages, inc_vals))
            higher = sum(1 for v in villages if inc[v] > inc["甲"])
            if higher != 1:
                return False
        return True

    opts = {
        "A 甲收入第二": lambda s: jia_second_always(s["甲乙丙丁"]),
        "B 乙=文旅": lambda s: s["甲乙丙丁"][1] == "文旅",
        "C 丙=数字": lambda s: s["甲乙丙丁"][2] == "数字",
        "D 丁=非遗": lambda s: s["甲乙丙丁"][3] == "非遗",
    }
    tag = f"甲≠数字:{require_jia_not_da} 相当=相等:{xiangdang_equal}"
    judge("2026GD-63 " + tag, summary, opts, "must")


if __name__ == "__main__":
    q_gd62()
    q_zja97()
    q_gk110()
    q_zja98()
    q_cq100()
    q_gd63(True, True)
    q_gd63(False, True)    # 敏感性：允许甲本身就是数字农业示范村
    q_gd63(True, False)    # 敏感性：“相当”不作相等约束
