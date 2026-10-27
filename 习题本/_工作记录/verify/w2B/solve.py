"""Independent brute-force checks for selfsolve week2 (solver B)."""
from itertools import permutations, product, combinations


def implies(p, q):
    return (not p) or q


print("=" * 60)
print("2026ZJA-96  升级提星 -> 设施完备 且 通过考核；违反 = 升星 且 非(设施且考核)")
cases = {
    "(1)": dict(star=True, fac=True, exam=False),   # 升星但未通过考核（设施未提及，取任意）
    "(1')": dict(star=True, fac=False, exam=False),
    "(2)": dict(star=True, fac=False, exam=True),   # 升星但没有基本设施
    "(2')": dict(star=True, fac=False, exam=False),
    "(3)": dict(star=False, fac=True, exam=True),
}
for k, v in cases.items():
    violated = v["star"] and not (v["fac"] and v["exam"])
    print(k, v, "违反要求" if violated else "未违反")

print("=" * 60)
print("2026GD-51  P:集约 Q:减少 S:减少缓慢 N:负面影响；P->Q, (Q and S)->not N")
# 变量: P, Q, S(减少很缓慢；快=Q and not S), N
opts = {
    "A": lambda P, Q, S, N: implies(not Q, not P),
    "B": lambda P, Q, S, N: implies(not P, not Q),
    "C": lambda P, Q, S, N: implies(Q, P),
    "D": lambda P, Q, S, N: implies(Q and not S, N),
}
for name, f in opts.items():
    ok = all(f(P, Q, S, N)
             for P, Q, S, N in product([0, 1], repeat=4)
             if implies(P, Q) and implies(Q and S, not N))
    print(name, "必然成立" if ok else "不必然")

print("=" * 60)
print("2018GK-115 圆桌座椅（两种左右约定 x 是否要求'未按顺序'）")
people = ["甲", "乙", "丙", "丁", "戊"]
for right in (+1, -1):
    left = -right
    for need_not_in_order in (False, True):
        answers = set()
        sols = []
        # 位置 0..4 环形；label[pos] = 座椅编号
        for labels in permutations([1, 2, 3, 4, 5]):
            pos = {lab: i for i, lab in enumerate(labels)}
            for seat in permutations(range(5)):
                s = dict(zip(people, seat))  # 人 -> 位置
                if s["甲"] != (pos[1] + 2 * right) % 5:
                    continue
                if s["乙"] != (pos[5] + 2 * left) % 5:
                    continue
                if s["丙"] != (pos[3] + 1 * left) % 5:
                    continue
                if s["丁"] != (pos[2] + 1 * left) % 5:
                    continue
                if labels[s["丙"]] != 1:   # 假设：丙坐1号
                    continue
                chair = {p: labels[s[p]] for p in people}
                if need_not_in_order and any(chair[p] == i + 1 for i, p in enumerate(people)):
                    continue
                answers.add(chair["甲"])
                sols.append(tuple(chair[p] for p in people))
        print(f"right={right:+d} 要求未按顺序={need_not_in_order}: 甲的座椅 = {sorted(answers)}; "
              f"人->椅(甲乙丙丁戊) = {sorted(set(sols))}")

print("=" * 60)
print("2026GK-110 7人选4人发言")
names = ["甲", "乙", "丙", "丁", "戊", "己", "庚"]
sols = []
for combo in combinations(names, 4):
    S = set(combo)
    c1 = not ("甲" in S and "丁" in S)
    c2 = implies("丙" in S or "戊" in S, "甲" in S and "己" not in S)
    c3 = implies("乙" in S or "庚" in S, "丁" in S and "甲" not in S)
    if c1 and c2 and c3:
        sols.append(combo)
print("可行方案:", sols)
opt = {"A": {"乙", "庚"}, "B": {"丙", "丁"}, "C": {"己", "戊"}, "D": {"甲", "乙"}}
for k, need in opt.items():
    print(k, all(need <= set(s) for s in sols) and len(sols) > 0)

print("=" * 60)
print("2026ZJA-98 6人获奖：一等1人 二等2人 三等3人")
P = ["琪琪", "依依", "冰冰", "鑫鑫", "磊磊", "静静"]
sols = []
for prizes in set(permutations([1, 2, 2, 3, 3, 3])):
    g = dict(zip(P, prizes))
    c1 = implies(g["琪琪"] != 2, g["冰冰"] == 1)
    c2 = implies(g["琪琪"] == 2 or g["依依"] == 2, g["鑫鑫"] == 3 and g["静静"] == 2)
    c3 = implies(g["鑫鑫"] == 3, g["冰冰"] == 2 and g["依依"] != 3)
    if c1 and c2 and c3:
        sols.append(g)
for s in sols:
    print(s)
checks = {
    "A 冰冰未获一等奖": lambda g: g["冰冰"] != 1,
    "B 琪琪获二等奖": lambda g: g["琪琪"] == 2,
    "C 鑫鑫未获一等奖": lambda g: g["鑫鑫"] != 1,
    "D 磊磊获三等奖": lambda g: g["磊磊"] == 3,
}
for k, f in checks.items():
    print(k, "一定为真" if sols and all(f(g) for g in sols) else "不一定")

print("=" * 60)
print("2026GD-57 / 2022SC1-76 论证形式的有效性（真值表）")


def valid(premises, conclusion, nvars):
    for vals in product([0, 1], repeat=nvars):
        if all(p(*vals) for p in premises) and not conclusion(*vals):
            return False
    return True


# GD-57: 题干 ¬A→¬B, A ⊢ B
forms57 = {
    "题干 ¬A→¬B, A ⊢ B": ([lambda a, b: implies(not a, not b), lambda a, b: a], lambda a, b: b),
    "A项 B→A(只有A才B), B ⊢ A": ([lambda a, b: implies(b, a), lambda a, b: b], lambda a, b: a),
    "B项 ¬A→¬B, ¬B ⊢ ¬A": ([lambda a, b: implies(not a, not b), lambda a, b: not b], lambda a, b: not a),
    "C项 ¬A→¬B ⊢ A→B": ([lambda a, b: implies(not a, not b)], lambda a, b: implies(a, b)),
    "D项 A→B, A ⊢ B（若把'禁止过度开采'等同于'合理开采'）": ([lambda a, b: implies(a, b), lambda a, b: a], lambda a, b: b),
}
for k, (prem, concl) in forms57.items():
    print(k, "有效" if valid(prem, concl, 2) else "无效")

# SC1-76: 题干 A→B, B→C ⊢ A→C
forms76 = {
    "题干 A→B, B→C ⊢ A→C": ([lambda a, b, c: implies(a, b), lambda a, b, c: implies(b, c)], lambda a, b, c: implies(a, c)),
    "C项 H→S, R→S ⊢ H→R": ([lambda h, s, r: implies(h, s), lambda h, s, r: implies(r, s)], lambda h, s, r: implies(h, r)),
    "D项 M→N, N→E ⊢ M→E": ([lambda m, n, e: implies(m, n), lambda m, n, e: implies(n, e)], lambda m, n, e: implies(m, e)),
}
for k, (prem, concl) in forms76.items():
    print(k, "有效" if valid(prem, concl, 3) else "无效")
