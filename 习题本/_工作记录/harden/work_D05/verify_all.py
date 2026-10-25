"""Brute-force checks for every question planned for D05 (kept, added, and new-variant numbers)."""
from itertools import permutations, combinations, product
from math import comb, factorial

res = {}

# ---------- 考法一 ----------
# T117 numbered round table: 6 seats (1-6, opposite pairs i, i+3), Zhang opposite Wu
people = "张王李赵周吴"
cnt = 0
for p in permutations(range(6)):  # p[k] = seat of person k
    z, w = p[0], p[5]
    if (z - w) % 6 == 3:
        cnt += 1
res["T117"] = (cnt, 144)

# 2022SD-45 clock 10:00:00 - 10:30:00 all six digits distinct
cnt = 0
for m in range(0, 31):
    for s in range(0, 60):
        if m == 30 and s > 0:
            continue
        d = "10" + f"{m:02d}" + f"{s:02d}"
        if len(set(d)) == 6:
            cnt += 1
res["2022SD-45"] = (cnt, 90)

# 2023HB-65: 10 domestic, 4 foreign, pick 3 ordered, both kinds, alternate
cnt = 0
items = [("D", i) for i in range(10)] + [("F", i) for i in range(4)]
for seq in permutations(items, 3):
    kinds = [x[0] for x in seq]
    if len(set(kinds)) < 2:
        continue
    if kinds[0] != kinds[1] and kinds[1] != kinds[2]:
        cnt += 1
res["2023HB-65"] = (cnt, 480)

# 2023GK-69: 10 households (3 special), k packs of 150 (k<=5), priority rule
cnt = 0
for k in range(0, 11):
    if 150 * k + 100 * (10 - k) > 1250:
        continue
    for S in combinations(range(10), k):  # households 0,1,2 special
        sp = sum(1 for x in S if x < 3)
        if sp == min(k, 3):
            cnt += 1
res["2023GK-69"] = (cnt, 36)

# 2020ZJB-16: 4 distinct digits from 1-9 forming a number divisible by 75
cnt = 0
for p in permutations(range(1, 10), 4):
    n = p[0] * 1000 + p[1] * 100 + p[2] * 10 + p[3]
    if n % 75 == 0:
        cnt += 1
res["2020ZJB-16"] = (cnt, "D: >25 (26)")

# 2023ZJA-61: courses 甲乙丙丁戊 into semesters 1-4, each semester >=1,
# 甲 alone, 乙丙 not in 1 or 4, 丁 after 戊 and 甲
cnt = 0
for a in product(range(1, 5), repeat=5):
    jia, yi, bing, ding, wu = a
    if set(a) != {1, 2, 3, 4}:
        continue
    if list(a).count(jia) != 1:
        continue
    if yi in (1, 4) or bing in (1, 4):
        continue
    if not (ding > wu and ding > jia):
        continue
    cnt += 1
res["2023ZJA-61"] = (cnt, 8)

# 2025GD-42: 3 soft-only S, 2 hard-only H, 2 both B; teams 甲, 乙 each with exactly 2 soft-capable, 2 hard-capable
staff = ["S1", "S2", "S3", "H1", "H2", "B1", "B2"]
cnt = 0
for assign in product(range(3), repeat=7):  # 0 = not sent, 1 = 甲, 2 = 乙
    ok = True
    for t in (1, 2):
        mem = [staff[i] for i in range(7) if assign[i] == t]
        soft = sum(1 for m in mem if m[0] in "SB")
        hard = sum(1 for m in mem if m[0] in "HB")
        if soft != 2 or hard != 2:
            ok = False
    if ok:
        cnt += 1
res["2025GD-42"] = (cnt, 30)

# 2023JSA-60: 4 days, 2 of 5 categories per day, each shown >=1, never on consecutive days, 玉(2) 国(4) not day1
cnt = 0
pairs = list(combinations(range(5), 2))
for days in product(pairs, repeat=4):
    if 2 in days[0] or 4 in days[0]:
        continue
    if set().union(*map(set, days)) != set(range(5)):
        continue
    if any(set(days[i]) & set(days[i + 1]) for i in range(3)):
        continue
    cnt += 1
res["2023JSA-60"] = (cnt, 72)

# ---------- 考法二 ----------
# 2022ZJA-64: 2 rows x 4 spots, 4 distinct cars, not all in one row, 甲乙 same row
cnt = 0
for p in permutations(range(8), 4):
    rows = [x // 4 for x in p]
    if len(set(rows)) == 1:
        continue
    if rows[0] != rows[1]:
        continue
    cnt += 1
res["2022ZJA-64"] = (cnt, 672)

# 1-v09: 4 GD, 3 HK, 2 MO choose 4 with all three
cnt = 0
firms = ["G"] * 4 + ["H"] * 3 + ["M"] * 2
for S in combinations(range(9), 4):
    if len({firms[i] for i in S}) == 3:
        cnt += 1
res["D05-math-1-v09"] = (cnt, 72)

# 2024HB-66: 4 students, 4 bases, at least 3 distinct bases chosen
cnt = sum(1 for a in product(range(4), repeat=4) if len(set(a)) >= 3)
res["2024HB-66"] = (cnt, 168)

# NV1 idea: 3x4 lattice triangles
pts = [(r, c) for r in range(3) for c in range(4)]
def col(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) == 0
tri = sum(1 for a, b, c in combinations(pts, 3) if not col(a, b, c))
res["NV1 3x4 lattice"] = (tri, 200)
pts4 = [(r, c) for r in range(4) for c in range(4)]
tri4 = sum(1 for a, b, c in combinations(pts4, 3) if not col(a, b, c))
res["NV1 4x4 lattice"] = (tri4, 516)

# 2024HB-72: 5 astronauts into 3 modules (0=天和), each >=1, 甲 not in 天和
cnt = 0
for a in product(range(3), repeat=5):
    if set(a) != {0, 1, 2}:
        continue
    if a[0] == 0:
        continue
    cnt += 1
res["2024HB-72"] = (cnt, 100)

# ---------- 考法三 ----------
# 2025JSA-64: songs S1,S2 at both ends; dance D & acro A adjacent; skit K & magic M not adjacent
cnt = 0
for p in permutations(["S1", "S2", "D", "A", "K", "M"]):
    if {p[0], p[5]} != {"S1", "S2"}:
        continue
    if abs(p.index("D") - p.index("A")) != 1:
        continue
    if abs(p.index("K") - p.index("M")) == 1:
        continue
    cnt += 1
res["2025JSA-64"] = (cnt, 8)

# 1-v12: 7 seats, leader seat 3 (0-index), deputies seats 2 and 4, 甲乙 adjacent among remaining
cnt = 0
for p in permutations(range(7)):  # p[k] seat of person k: 0 leader,1,2 deputies,3 甲,4 乙,5,6 others
    if p[0] != 3 or {p[1], p[2]} != {2, 4}:
        continue
    if abs(p[3] - p[4]) != 1:
        continue
    cnt += 1
res["D05-math-1-v12"] = (cnt, 16)

# 2026ZJA-51: 2x3 formation; 张王 front-back adjacent (same column), 李吴 left-right adjacent (same row, adjacent col)
cnt = 0
for p in permutations(range(6)):  # cell = r*3+c
    z, w, l, wu = p[0], p[1], p[2], p[3]
    if not (z % 3 == w % 3 and z // 3 != w // 3):
        continue
    if not (l // 3 == wu // 3 and abs(l % 3 - wu % 3) == 1):
        continue
    cnt += 1
res["2026ZJA-51"] = (cnt, 32)

# 1-v14: 5 people, exactly two of 甲乙丙 adjacent and the third adjacent to neither
cnt = 0
for p in permutations(range(5)):
    pos = [p.index(i) for i in range(3)]
    adj = [(i, j) for i, j in combinations(range(3), 2) if abs(pos[i] - pos[j]) == 1]
    if len(adj) == 1:
        cnt += 1
res["D05-math-1-v14"] = (cnt, 72)

# T113: choose 3 of 8 jets, 2 of 3 AEW, 1 of 2 ASW; order of 6: jets consecutive, AEW not adjacent
order_cnt = 0
for p in permutations(["J1", "J2", "J3", "E1", "E2", "R"]):
    js = sorted(p.index(x) for x in ("J1", "J2", "J3"))
    if js[2] - js[0] != 2:
        continue
    if abs(p.index("E1") - p.index("E2")) == 1:
        continue
    order_cnt += 1
res["T113"] = (comb(8, 3) * comb(3, 2) * 2 * order_cnt, 24192)

# ---------- 考法四 ----------
# 2023GK-68: 5 shops, restaurants R1,R2 (1 or 2 adjacent shops), fruit F1,F2 (1 shop), all rented,
# same-type tenants separated by at least one shop
cnt = 0
for sizes in product([1, 2], repeat=2):
    units = [("R1", sizes[0]), ("R2", sizes[1]), ("F1", 1), ("F2", 1)]
    if sum(s for _, s in units) != 5:
        continue
    for p in permutations(units):
        types = [u[0][0] for u in p]
        if any(types[i] == types[i + 1] for i in range(3)):
            continue
        cnt += 1
res["2023GK-68"] = (cnt, 16)

# 1-v20: 3 distinct firms, plots 1-12, pairwise diff >=3
cnt = sum(1 for p in permutations(range(1, 13), 3) if all(abs(a - b) >= 3 for a, b in combinations(p, 2)))
res["D05-math-1-v20"] = (cnt, 336)

# T004: 10 lamps, no two consecutive off
cnt = sum(1 for a in product([0, 1], repeat=10) if not any(a[i] == 0 and a[i + 1] == 0 for i in range(9)))
res["T004"] = (cnt, 144)

# 2023ZJA-70: permutations of 12 with |new-old|<=1, excluding identity -> count via DP (brute force n=12 too big) ; brute small n and DP
def count_adj(n):
    f = [1, 1]
    for i in range(2, n + 1):
        f.append(f[-1] + f[-2])
    return f[n]
small_ok = all(
    sum(1 for p in permutations(range(n)) if all(abs(p[i] - i) <= 1 for i in range(n))) == count_adj(n)
    for n in range(1, 8)
)
res["2023ZJA-70"] = (count_adj(12) - 1, 232, "small-n brute ok" if small_ok else "MISMATCH")

# 2021JSA-58: courses a..f, conflicts from combos, 6 consecutive days within Jan 4-10
combos = ["af", "df", "ace", "bcf"]
conf = set()
for cmb in combos:
    for x, y in combinations(cmb, 2):
        conf.add(frozenset((x, y)))
orders = sum(1 for p in permutations("abcdef") if not any(frozenset((p[i], p[i + 1])) in conf for i in range(5)))
res["2021JSA-58"] = (orders * 2, 4)

# T118: 8 seated around a round table -> 8 gaps; 3 distinct newcomers; no two newcomers adjacent (distinct gaps),
# each seated person adjacent to at most one newcomer (chosen gaps not cyclically adjacent)
cnt = 0
for g in permutations(range(8), 3):
    s = sorted(g)
    ok = True
    for x, y in combinations(s, 2):
        if (y - x) % 8 in (1, 7):
            ok = False
    if ok:
        cnt += 1
res["T118"] = (cnt, 96)

# 2022JSA-65 / T112: 3 companies x 2 staff, same-company not adjacent
cnt = 0
for p in permutations(range(6)):
    comp = [x // 2 for x in p]
    if any(comp[i] == comp[i + 1] for i in range(5)):
        continue
    cnt += 1
res["2022JSA-65"] = (cnt, 240)

# ---------- 考法十四 ----------
# 2021SD-45: 5 identical cones, 9 schemes, pairwise not identical -> multiset of 5 distinct schemes
res["2021SD-45"] = (comb(9, 5), 126)

# 2-v02: 5 fixed programs + 2 distinct new
cnt = 0
for p in permutations(["o1", "o2", "o3", "o4", "o5", "n1", "n2"]):
    olds = [x for x in p if x[0] == "o"]
    if olds == ["o1", "o2", "o3", "o4", "o5"]:
        cnt += 1
res["D05-math-2-v02"] = (cnt, 42)

# 2-v04: grid 4E 3N avoid (2,1)
cnt = 0
for S in combinations(range(7), 3):  # positions of N moves
    x = y = 0
    bad = False
    for i in range(7):
        if i in S:
            y += 1
        else:
            x += 1
        if (x, y) == (2, 1):
            bad = True
    if not bad:
        cnt += 1
res["D05-math-2-v04"] = (cnt, 17)

# 2025GK-72: 5 T/F, score after each >=1
cnt = 0
for a in product([1, -1], repeat=5):
    s = 0
    ok = True
    for x in a:
        s += x
        if s < 1:
            ok = False
    if ok:
        cnt += 1
res["2025GK-72"] = (cnt, 6)

# T115 / T116
def visits(cond):
    c = 0
    for p in permutations("甲乙丙丁戊己"):
        if abs(p.index("甲") - p.index("乙")) != 1:
            continue
        if p.index("己") not in (0, 5):
            continue
        if not cond(p):
            continue
        c += 1
    return c
res["T115"] = (visits(lambda p: p.index("戊") < p.index("丙") < p.index("丁")), 16)
res["T116"] = (visits(lambda p: p.index("丁") < p.index("丙") and p.index("戊") < p.index("丙")), 32)

# T114: 7 days, 6 cadres, each >=1 day, 甲乙丙 exactly 1 day each, 甲 before 乙
cnt = 0
for a in product(range(6), repeat=7):  # a[d] = cadre on day d; 0 甲,1 乙,2 丙
    if set(a) != set(range(6)):
        continue
    if a.count(0) != 1 or a.count(1) != 1 or a.count(2) != 1:
        continue
    if a.index(0) > a.index(1):
        continue
    cnt += 1
res["T114"] = (cnt, 3780)

# 2024ZJA-70 / T003: compositions of 10 into parts 1..3
f = [1, 1, 2]
for n in range(3, 11):
    f.append(f[n - 1] + f[n - 2] + f[n - 3])
res["2024ZJA-70"] = (f[10], 274)

# ---------- 考法五 ----------
# 2-v07: 5 volunteers onto 3 stations, each >=1
res["D05-math-2-v07"] = (sum(1 for a in product(range(3), repeat=5) if set(a) == {0, 1, 2}), 150)

# 2-v08: 8 teams perfect matchings with team0, team1 not paired
def matchings(lst):
    if not lst:
        yield []
        return
    a = lst[0]
    for i in range(1, len(lst)):
        b = lst[i]
        rest = lst[1:i] + lst[i + 1:]
        for m in matchings(rest):
            yield [(a, b)] + m
res["D05-math-2-v08"] = (sum(1 for m in matchings(list(range(8))) if (0, 1) not in m), 90)

# 2025HB-66: 6 workers to A(>=2),B(>=1),C(>=1)
cnt = 0
for a in product(range(3), repeat=6):
    if a.count(0) >= 2 and a.count(1) >= 1 and a.count(2) >= 1:
        cnt += 1
res["2025HB-66"] = (cnt, 360)

# 2022GK-69 / T111: 甲乙丙 env; 丁戊己 tourism; 甲丁戊 media; split into 2 unlabeled groups of 3, each with env, tour, media
env, tour, media = set("甲乙丙"), set("丁戊己"), set("甲丁戊")
allp = set("甲乙丙丁戊己")
cnt = 0
for g in combinations(sorted(allp), 3):
    if "甲" not in g:
        continue  # fix 甲's group to avoid double count
    G1, G2 = set(g), allp - set(g)
    if all(G & env and G & tour and G & media for G in (G1, G2)):
        cnt += 1
res["2022GK-69"] = (cnt, 8)

# 2021SC2-48: 6 experts: AB1,AB2 (agri+livestock), A (agri only), B (livestock only), F1,F2 (fishery only)
# 2 per county; 丙 needs no fishery but agri & livestock; 甲,乙 need all three
skills = {"AB1": "AB", "AB2": "AB", "A": "A", "B": "B", "F1": "F", "F2": "F"}
names = list(skills)
cnt = 0
for assign in product(range(3), repeat=6):  # 0 甲, 1 乙, 2 丙
    if any(assign.count(k) != 2 for k in range(3)):
        continue
    ok = True
    for k in range(3):
        sk = set("".join(skills[names[i]] for i in range(6) if assign[i] == k))
        if k in (0, 1):
            if not {"A", "B", "F"} <= sk:
                ok = False
        else:
            if "F" in sk or not {"A", "B"} <= sk:
                ok = False
    if ok:
        cnt += 1
res["2021SC2-48"] = (cnt, 4)

# 2024GK-68: teams 1..6 into projects 甲/乙, each >=2, each with a leader that is not the min-numbered in its project
cnt = 0
for a in product(range(2), repeat=6):
    sizes = [a.count(0), a.count(1)]
    if min(sizes) < 2:
        continue
    ways = 1
    for k in range(2):
        mem = [i for i in range(6) if a[i] == k]
        ways *= len(mem) - 1
    cnt += ways
res["2024GK-68"] = (cnt, 170)

# NV2 idea: 8 people into 4 pairs; 2 pairs to A (interchangeable), 1 to B, 1 to C; 甲乙 not together
total = 0
bad = 0
for m in matchings(list(range(8))):
    # assign the 4 pairs to A,A,B,C: choose which pair goes to B and which to C -> 4*3 = 12
    total += 12
    if (0, 1) in m:
        bad += 12
res["NV2 idea"] = ((total, total - bad), (1260, 1080))

# ---------- 考法七 ----------
# 2-v10
cnt = sum(1 for x in range(1, 11) for y in range(1, 11) if x % 2 == 0 and 10 - x - y >= 1 and y >= 1)
res["D05-math-2-v10"] = (cnt, 16)
# T120: 15 docs to 3 people, 3..10 each
res["T120"] = (sum(1 for x in range(3, 11) for y in range(3, 11) if 3 <= 15 - x - y <= 10), 28)
# 2-v11: 10 among 4 towns, 1..4 each
res["D05-math-2-v11"] = (sum(1 for a in product(range(1, 5), repeat=4) if sum(a) == 10), 44)
# NV3 idea: up to 10 identical quotas to 3 communities, each >=2, need not all be used
res["NV3 idea"] = (sum(1 for a in product(range(2, 11), repeat=3) if sum(a) <= 10), 35)
# 2025GK-77
cnt = 0
for a1, b1 in product(range(1, 6), repeat=2):
    c1 = 5 - a1 - b1
    if c1 < 1:
        continue
    for a2, b2 in product(range(1, 6), repeat=2):
        c2 = 5 - a2 - b2
        if c2 < 1:
            continue
        A, B, C = a1 + a2, b1 + b2, c1 + c2
        if A > B and A > C and b1 > b2:
            cnt += 1
res["2025GK-77"] = (cnt, 3)

for k, v in res.items():
    flag = "OK" if (len(v) >= 2 and (v[0] == v[1] or isinstance(v[1], str))) else "CHECK"
    print(f"{k:22s} {v}  {flag}")
