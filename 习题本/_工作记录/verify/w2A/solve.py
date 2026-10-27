from itertools import product, permutations, combinations

imp = lambda p, q: (not p) or q

print("=== 2026ZJA-96 ===")
# rule: upgrade -> (facility and exam). Violation = upgrade and not(facility and exam)
def violates(up, fac, ex):
    return not imp(up, fac and ex)
cases = {"(1)": dict(up=True, ex=False), "(2)": dict(up=True, fac=False), "(3)": dict(up=False, fac=True, ex=True)}
for k, fixed in cases.items():
    res = set()
    for up, fac, ex in product([True, False], repeat=3):
        v = dict(up=up, fac=fac, ex=ex)
        if all(v[x] == fixed[x] for x in fixed):
            res.add(violates(up, fac, ex))
    print(k, "always violates" if res == {True} else ("never" if res == {False} else "sometimes"), res)

print("=== 2026GD-51 ===")
# J: 集约, R: 减少, S: 减少缓慢 (S -> R), N: 负面影响
# premises: J -> R ; S -> not N ; S implies R (slow decrease is a decrease)
opts = {
 "A": lambda J,R,S,F,N: imp(not R, not J),
 "B": lambda J,R,S,F,N: imp(not J, not R),
 "C": lambda J,R,S,F,N: imp(R, J),
 "D": lambda J,R,S,F,N: imp(R and F, N),
}
for k, f in opts.items():
    ok = True
    for J,R,S,F,N in product([True,False], repeat=5):
        # F: decrease fast ; S: decrease slow; they are exclusive, both need R
        if (S or F) and not R: continue
        if S and F: continue
        if not (imp(J, R) and imp(S, not N)): continue
        if not f(J,R,S,F,N): ok = False; break
    print(k, "valid" if ok else "invalid")

print("=== 2018GK-115 ===")
# positions 0..4 around table; step +d is 'right' direction
for d in (+1, -1):
    for need_disorder in (True, False):
        answers = set(); sols = []
        for chairs in permutations([1,2,3,4,5]):  # chairs[pos] = chair label
            pos = {c: i for i, c in enumerate(chairs)}
            for people in permutations(["甲","乙","丙","丁","戊"]):  # people[pos]
                ppos = {p: i for i, p in enumerate(people)}
                R = lambda c, k: (pos[c] + d*k) % 5   # k-th chair to the right
                L = lambda c, k: (pos[c] - d*k) % 5
                if ppos["甲"] != R(1, 2): continue
                if ppos["乙"] != L(5, 2): continue
                if ppos["丙"] != L(3, 1): continue
                if ppos["丁"] != L(2, 1): continue
                seat = {p: chairs[ppos[p]] for p in ppos}
                if need_disorder and any(seat[p] == n for p, n in zip(["甲","乙","丙","丁","戊"], [1,2,3,4,5])):
                    continue
                if seat["丙"] != 1: continue
                answers.add(seat["甲"]); sols.append(tuple(sorted(seat.items())))
        print(f"right={'+1' if d==1 else '-1'} disorder={need_disorder}: 甲 chair set={answers}, distinct seatings={set(sols)}")

print("=== 2026GK-110 ===")
names = "甲乙丙丁戊己庚"
sols = []
for S in combinations(names, 4):
    s = set(S); x = lambda n: n in s
    c1 = not (x("甲") and x("丁"))
    c2 = imp(x("丙") or x("戊"), x("甲") and not x("己"))
    c3 = imp(x("乙") or x("庚"), x("丁") and not x("甲"))
    if c1 and c2 and c3: sols.append(S)
print("solutions:", sols)
opt = {"A": "乙庚", "B": "丙丁", "C": "己戊", "D": "甲乙"}
for k, v in opt.items():
    print(k, all(all(n in S for n in v) for S in sols))

print("=== 2026ZJA-98 ===")
P = ["琪琪","依依","冰冰","鑫鑫","磊磊","静静"]
sols = []
for a in product([1,2,3], repeat=6):
    if (a.count(1), a.count(2), a.count(3)) != (1, 2, 3): continue
    g = dict(zip(P, a))
    c1 = imp(g["琪琪"] != 2, g["冰冰"] == 1)
    c2 = imp(g["琪琪"] == 2 or g["依依"] == 2, g["鑫鑫"] == 3 and g["静静"] == 2)
    c3 = imp(g["鑫鑫"] == 3, g["冰冰"] == 2 and g["依依"] != 3)
    if c1 and c2 and c3: sols.append(g)
for g in sols: print(g)
chk = {"A": lambda g: g["冰冰"] != 1, "B": lambda g: g["琪琪"] == 2,
       "C": lambda g: g["鑫鑫"] != 1, "D": lambda g: g["磊磊"] == 3}
for k, f in chk.items():
    print(k, "always" if all(f(g) for g in sols) else "not necessarily")

print("=== 2026GD-57 / 2022SC1-76: propositional form check ===")
# validity of each argument form: premises -> conclusion over all valuations
def valid(prem, concl, n):
    return all(imp(all(p(*v) for p in prem), concl(*v)) for v in product([True,False], repeat=n))
# 57 stem: ¬A→¬B, A ⊢ B
stem57 = ([lambda A,B: imp(not A, not B), lambda A,B: A], lambda A,B: B)
o57 = {
 "A (只有A才B, B ⊢ A)": ([lambda A,B: imp(B, A), lambda A,B: B], lambda A,B: A),
 "B (¬A→¬B, ¬B ⊢ ¬A)": ([lambda A,B: imp(not A, not B), lambda A,B: not B], lambda A,B: not A),
 "C (¬A→¬B ⊢ A→B)": ([lambda A,B: imp(not A, not B)], lambda A,B: imp(A, B)),
 "D (A→B, A ⊢ B, if 禁止过度开采≈合理开采)": ([lambda A,B: imp(A, B), lambda A,B: A], lambda A,B: B),
}
print("stem57 valid?", valid(*stem57, 2))
for k, v in o57.items(): print(k, "valid?", valid(*v, 2))
# stem57 is equivalent to C: (¬A→¬B ∧ A → B) is a tautology iff (¬A→¬B) → (A→B) is: check the sets of counter-models
cm_stem = [v for v in product([True,False], repeat=2) if imp(not v[0], not v[1]) and v[0] and not v[1]]
cm_C = [v for v in product([True,False], repeat=2) if imp(not v[0], not v[1]) and not imp(v[0], v[1])]
print("countermodels stem57:", cm_stem, " countermodels C:", cm_C)
# 76 stem: A→B, B→C ⊢ A→C
print("76 stem valid?", valid([lambda A,B,C: imp(A,B), lambda A,B,C: imp(B,C)], lambda A,B,C: imp(A,C), 3))
print("76 opt C (C→A, B→A ⊢ C→B) valid?", valid([lambda A,B,C: imp(C,A), lambda A,B,C: imp(B,A)], lambda A,B,C: imp(C,B), 3))
print("76 opt D (A→B, B→C ⊢ A→C) valid?", valid([lambda A,B,C: imp(A,B), lambda A,B,C: imp(B,C)], lambda A,B,C: imp(A,C), 3))
