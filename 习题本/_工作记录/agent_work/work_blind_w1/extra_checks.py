# -*- coding: utf-8 -*-
"""补充检查：GD-62 镜像读法敏感性；L07 平行结构题的形式有效性（真值表）。"""
from itertools import permutations, product


def imp(a, b):
    return (not a) or b


# ---------------- GD-62：若“右手边”按序号更小理解（镜像），是否仍有必然选项
def gd62_mirror():
    names = ["教育", "住建", "交通", "农业", "人社", "财政"]
    sols = []
    for perm in permutations(range(1, 7)):
        p = dict(zip(names, perm))
        if p["财政"] != p["人社"] - 1:
            continue
        if not (p["住建"] < p["财政"] - 1):
            continue
        if abs(p["教育"] - p["交通"]) != 2 or abs(p["农业"] - p["财政"]) != 1:
            continue
        sols.append(p)
    opts = {"A": lambda s: s["教育"] == 4, "B": lambda s: s["住建"] == 5,
            "C": lambda s: s["交通"] == 3, "D": lambda s: s["人社"] == 2}
    print("== GD-62 镜像读法 解数", len(sols), {k: all(f(s) for s in sols) for k, f in opts.items()})


# ---------------- 论证形式有效性
def valid(nvars, premises, concl):
    for v in product([False, True], repeat=nvars):
        if all(p(*v) for p in premises) and not concl(*v):
            return False
    return True


def forms():
    print("== GD-61  题干 A->B, B->C ∴ A->C:", valid(3, [lambda a, b, c: imp(a, b), lambda a, b, c: imp(b, c)], lambda a, b, c: imp(a, c)))
    print("   A项 A->B, B->C ∴ 非A->非C:", valid(3, [lambda a, b, c: imp(a, b), lambda a, b, c: imp(b, c)], lambda a, b, c: imp(not a, not c)))
    print("   B项 S->L, P->S ∴ P->L:", valid(3, [lambda s, l, p: imp(s, l), lambda s, l, p: imp(p, s)], lambda s, l, p: imp(p, l)))
    print("   D项 A->C, B->C ∴ B->A:", valid(3, [lambda a, b, c: imp(a, c), lambda a, b, c: imp(b, c)], lambda a, b, c: imp(b, a)))

    print("== GK-115 题干 A->B, B ∴ A:", valid(2, [lambda a, b: imp(a, b), lambda a, b: b], lambda a, b: a))
    print("   A项 A->B->C, A ∴ C:", valid(3, [lambda a, b, c: imp(a, b), lambda a, b, c: imp(b, c), lambda a, b, c: a], lambda a, b, c: c))
    print("   C项 A->B, B ∴ A:", valid(2, [lambda a, b: imp(a, b), lambda a, b: b], lambda a, b: a))

    # GD-57：题干 非A->非B, A ∴ B（否前）
    stem = valid(2, [lambda a, b: imp(not a, not b), lambda a, b: a], lambda a, b: b)
    print("== GD-57  题干 非A->非B, A ∴ B:", stem)
    print("   A项 B->A, B ∴ A:", valid(2, [lambda a, b: imp(b, a), lambda a, b: b], lambda a, b: a))
    print("   B项 非A->非B, 非B ∴ 非A:", valid(2, [lambda a, b: imp(not a, not b), lambda a, b: not b], lambda a, b: not a))
    print("   C项 非A->非B ∴ A->B:", valid(2, [lambda a, b: imp(not a, not b)], lambda a, b: imp(a, b)))
    print("   D项 A->B, A' ∴ B（A'≠A，概念不同；按形式 A->B, A ∴ B）:", valid(2, [lambda a, b: imp(a, b), lambda a, b: a], lambda a, b: b))

    print("== SC1-76 题干 A->B, B->C ∴ A->C:", valid(3, [lambda a, b, c: imp(a, b), lambda a, b, c: imp(b, c)], lambda a, b, c: imp(a, c)))
    print("   C项 H->S, I->S ∴ H->I:", valid(3, [lambda h, s, i: imp(h, s), lambda h, s, i: imp(i, s)], lambda h, s, i: imp(h, i)))
    print("   D项 M->H, H->E ∴ M->E:", valid(3, [lambda m, h, e: imp(m, h), lambda m, h, e: imp(h, e)], lambda m, h, e: imp(m, e)))

    # GD-65：题干 A->(B或C), 非B ∴ A->C
    print("== GD-65  题干 A->(B∨C), ¬B ∴ A->C:", valid(3, [lambda a, b, c: imp(a, b or c), lambda a, b, c: not b], lambda a, b, c: imp(a, c)))
    print("   A项 A->(B∨C), ¬C ∴ B（未交代A）:", valid(3, [lambda a, b, c: imp(a, b or c), lambda a, b, c: not c], lambda a, b, c: b))
    print("   C项 B∨C, B ∴ ¬C:", valid(2, [lambda b, c: b or c, lambda b, c: b], lambda b, c: not c))
    print("   D项 A->(B∨C), A∧¬C ∴ B:", valid(3, [lambda a, b, c: imp(a, b or c), lambda a, b, c: a and not c], lambda a, b, c: b))


if __name__ == "__main__":
    gd62_mirror()
    forms()
