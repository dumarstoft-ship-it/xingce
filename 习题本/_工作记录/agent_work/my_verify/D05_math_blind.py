# Blind brute-force solver for D05 math (M06 permutation & combination) review.
# Every question is enumerated directly from the stem data; no expected answers are used.
import itertools as it
import json
import sys

QFILE = sys.argv[1]
qs = {q["vid"]: q for q in json.load(open(QFILE, encoding="utf-8"))}
results = {}


def pick(vid, value):
    """Map a computed number to the option letter(s) whose text equals it."""
    opts = qs[vid]["options"]
    hits = [k for k, v in opts.items() if str(v).strip() == str(value)]
    results[vid] = (value, hits)


def adjacent(a, b):
    return abs(a - b) == 1


# ---------------- 1-v01: meat = veg + 2, C(meat,2)*C(veg,2) = 90 -> meat?
vid = "D05-math-1-v01"
sols = []
for letter, txt in qs[vid]["options"].items():
    m = int(txt)
    v = m - 2
    cnt = sum(1 for _ in it.combinations(range(m), 2)) * sum(1 for _ in it.combinations(range(max(v, 0)), 2))
    if cnt == 90:
        sols.append(m)
pick(vid, sols[0] if len(sols) == 1 else ("MULTI/NONE", sols))

# ---------------- 1-v02: 5 men 4 women; track: 2 men ordered roles; basketball 1M+1W; diving 2W (same work)
vid = "D05-math-1-v02"
men = ["M%d" % i for i in range(5)]
women = ["W%d" % i for i in range(4)]
people = men + women
# label: 0 none, 1 check-in (track), 2 timing (track), 3 basketball, 4 diving
cnt = 0
for labels in it.product(range(5), repeat=9):
    lab = dict(zip(people, labels))
    if sum(1 for p in men if lab[p] == 1) != 1 or sum(1 for p in women if lab[p] == 1) != 0:
        continue
    if sum(1 for p in men if lab[p] == 2) != 1 or sum(1 for p in women if lab[p] == 2) != 0:
        continue
    if sum(1 for p in men if lab[p] == 3) != 1 or sum(1 for p in women if lab[p] == 3) != 1:
        continue
    if sum(1 for p in women if lab[p] == 4) != 2 or sum(1 for p in men if lab[p] == 4) != 0:
        continue
    cnt += 1
pick(vid, cnt)

# ---------------- 1-v03: GZ->SZ: 3 HSR or 2 intercity; SZ->HK via port A or B; intercity cannot reach port A; + 2 direct buses
vid = "D05-math-1-v03"
routes = set()
for leg in ["H1", "H2", "H3", "I1", "I2"]:
    for port in ["A", "B"]:
        if leg.startswith("I") and port == "A":
            continue
        routes.add((leg, port))
routes |= {("BUS1",), ("BUS2",)}
pick(vid, len(routes))

# ---------------- 1-v04: 3M 3W choose 4, women >= 2, captain among chosen men
vid = "D05-math-1-v04"
M = ["m1", "m2", "m3"]
W = ["w1", "w2", "w3"]
cnt = 0
for team in it.combinations(M + W, 4):
    w = [p for p in team if p in W]
    m = [p for p in team if p in M]
    if len(w) < 2:
        continue
    cnt += len(m)  # choose captain from chosen men
pick(vid, cnt)

# ---------------- 1-v05: 8 runners; ranks 1-4 lanes 3-6, ranks 5-6 lanes 7-8, ranks 7-8 lanes 1-2; jia, yi (in top 4) not adjacent
vid = "D05-math-1-v05"
runners = ["jia", "yi", "r3", "r4", "r5", "r6", "r7", "r8"]
zone = {"jia": {3, 4, 5, 6}, "yi": {3, 4, 5, 6}, "r3": {3, 4, 5, 6}, "r4": {3, 4, 5, 6},
        "r5": {7, 8}, "r6": {7, 8}, "r7": {1, 2}, "r8": {1, 2}}
cnt = 0
for lanes in it.permutations(range(1, 9)):
    asg = dict(zip(runners, lanes))
    if any(asg[r] not in zone[r] for r in runners):
        continue
    if adjacent(asg["jia"], asg["yi"]):
        continue
    cnt += 1
pick(vid, cnt)

# ---------------- 1-v06: 6 male 3 female doctors choose 3, males <= 2
vid = "D05-math-1-v06"
docs = ["M"] * 6 + ["F"] * 3
cnt = sum(1 for c in it.combinations(range(9), 3) if sum(docs[i] == "M" for i in c) <= 2)
pick(vid, cnt)

# ---------------- 1-v07: 3-char code from {1..5, X, Y, Z}, must contain both digit and letter
vid = "D05-math-1-v07"
chars = list("12345XYZ")
cnt = sum(1 for code in it.product(chars, repeat=3)
          if any(ch.isdigit() for ch in code) and any(ch.isalpha() for ch in code))
pick(vid, cnt)

# ---------------- 1-v08: n men + 4 women choose 3, mixed gender, total 70 -> n?
vid = "D05-math-1-v08"
sols = []
for letter, txt in qs[vid]["options"].items():
    n = int(txt)
    pool = ["M"] * n + ["F"] * 4
    c = sum(1 for s in it.combinations(range(n + 4), 3) if len({pool[i] for i in s}) == 2)
    if c == 70:
        sols.append(n)
pick(vid, sols[0] if len(sols) == 1 else ("MULTI/NONE", sols))

# ---------------- 1-v09: GD 4, HK 3, MO 2; choose 4 with all three regions present
vid = "D05-math-1-v09"
firms = ["GD"] * 4 + ["HK"] * 3 + ["MO"] * 2
cnt = sum(1 for s in it.combinations(range(9), 4) if len({firms[i] for i in s}) == 3)
pick(vid, cnt)

# ---------------- 1-v10: 6 booths in a row; jia not leftmost, yi not rightmost
vid = "D05-math-1-v10"
cnt = 0
for perm in it.permutations(["jia", "yi", "c", "d", "e", "f"]):
    if perm[0] == "jia" or perm[-1] == "yi":
        continue
    cnt += 1
pick(vid, cnt)

# ---------------- 1-v11: departments of sizes 2,3,3; each dept consecutive; first speaker from the 2-person dept
vid = "D05-math-1-v11"
dept = {"a1": "A", "a2": "A", "b1": "B", "b2": "B", "b3": "B", "c1": "C", "c2": "C", "c3": "C"}
cnt = 0
for perm in it.permutations(list(dept)):
    seq = [dept[p] for p in perm]
    if seq[0] != "A":
        continue
    # contiguity: number of blocks equals number of departments
    blocks = 1 + sum(1 for i in range(1, 8) if seq[i] != seq[i - 1])
    if blocks != 3:
        continue
    cnt += 1
pick(vid, cnt)

# ---------------- 1-v12: 7 seats; leader in seat 4; 2 deputies on seats 3 and 5 (either way round);
# other 4 (incl. jia, yi) on remaining seats; jia & yi adjacent
vid = "D05-math-1-v12"
cnt = 0
cnt_fixed_deputies = 0
for perm in it.permutations(["L", "D1", "D2", "jia", "yi", "p", "q"]):
    seat = {p: i + 1 for i, p in enumerate(perm)}
    if seat["L"] != 4 or {seat["D1"], seat["D2"]} != {3, 5}:
        continue
    if not adjacent(seat["jia"], seat["yi"]):
        continue
    cnt += 1
    if seat["D1"] == 3:
        cnt_fixed_deputies += 1
pick(vid, cnt)
results[vid] = results[vid] + ({"if_deputies_fixed": cnt_fixed_deputies},)

# ---------------- 1-v13: 6 distinct cars: P1,P2 power; C dining; K1..K3 passenger
# power cars adjacent and at one end; dining car not adjacent to any power car; front-to-back order matters
vid = "D05-math-1-v13"
cnt = 0
for perm in it.permutations(["P1", "P2", "C", "K1", "K2", "K3"]):
    pos = {c: i for i, c in enumerate(perm)}
    if not adjacent(pos["P1"], pos["P2"]):
        continue
    if not ({pos["P1"], pos["P2"]} == {0, 1} or {pos["P1"], pos["P2"]} == {4, 5}):
        continue
    if adjacent(pos["C"], pos["P1"]) or adjacent(pos["C"], pos["P2"]):
        continue
    cnt += 1
pick(vid, cnt)

# ---------------- 1-v14: 5 people in a row; among jia, yi, bing exactly two adjacent and third adjacent to neither
vid = "D05-math-1-v14"
cnt = 0
for perm in it.permutations(["jia", "yi", "bing", "ding", "wu"]):
    pos = {p: i for i, p in enumerate(perm)}
    trio = ["jia", "yi", "bing"]
    adj_pairs = [(a, b) for a, b in it.combinations(trio, 2) if adjacent(pos[a], pos[b])]
    if len(adj_pairs) != 1:
        continue
    a, b = adj_pairs[0]
    third = [t for t in trio if t not in (a, b)][0]
    if adjacent(pos[third], pos[a]) or adjacent(pos[third], pos[b]):
        continue
    cnt += 1
pick(vid, cnt)

# ---------------- 1-v15: 3 distinct activities on 3 distinct days of Mon..Sun, any two at least one day apart
vid = "D05-math-1-v15"
cnt = 0
for days in it.permutations(range(1, 8), 3):  # days[i] = day of activity i
    if all(abs(x - y) >= 2 for x, y in it.combinations(days, 2)):
        cnt += 1
pick(vid, cnt)

# ---------------- 1-v16: choose 3 days of Mon..Sun, pairwise non-adjacent, Sunday included
vid = "D05-math-1-v16"
cnt = sum(1 for s in it.combinations(range(1, 8), 3)
          if 7 in s and all(abs(x - y) >= 2 for x, y in it.combinations(s, 2)))
pick(vid, cnt)

# ---------------- 1-v17: 10 lamps, switch off 3, not first/last, no two adjacent
vid = "D05-math-1-v17"
cnt = sum(1 for s in it.combinations(range(1, 11), 3)
          if 1 not in s and 10 not in s and all(abs(x - y) >= 2 for x, y in it.combinations(s, 2)))
pick(vid, cnt)

# ---------------- 1-v18: 4 men (incl. jia), 3 women, alternate genders, jia not first
vid = "D05-math-1-v18"
sex = {"jia": "M", "m2": "M", "m3": "M", "m4": "M", "w1": "F", "w2": "F", "w3": "F"}
cnt = 0
for perm in it.permutations(list(sex)):
    if any(sex[perm[i]] == sex[perm[i + 1]] for i in range(6)):
        continue
    if perm[0] == "jia":
        continue
    cnt += 1
pick(vid, cnt)

# ---------------- 1-v19: 4 days from Oct 1..15, at least 2 empty days between consecutive inspections
vid = "D05-math-1-v19"
cnt = sum(1 for s in it.combinations(range(1, 16), 4)
          if all(s[i + 1] - s[i] - 1 >= 2 for i in range(3)))
pick(vid, cnt)

# ---------------- 1-v20: 3 distinct firms rent units 1..12, pairwise number difference >= 3
vid = "D05-math-1-v20"
cnt = sum(1 for s in it.permutations(range(1, 13), 3)
          if all(abs(x - y) >= 3 for x, y in it.combinations(s, 2)))
pick(vid, cnt)

# ---------------- 2-v01: 6 awardees, jia before yi before bing
vid = "D05-math-2-v01"
cnt = 0
for perm in it.permutations(["jia", "yi", "bing", "d", "e", "f"]):
    pos = {p: i for i, p in enumerate(perm)}
    if pos["jia"] < pos["yi"] < pos["bing"]:
        cnt += 1
pick(vid, cnt)

# ---------------- 2-v02: 5 original programs keep order; insert 2 distinct new programs anywhere
vid = "D05-math-2-v02"
cnt = 0
for perm in it.permutations(["O1", "O2", "O3", "O4", "O5", "N1", "N2"]):
    olds = [p for p in perm if p.startswith("O")]
    if olds == ["O1", "O2", "O3", "O4", "O5"]:
        cnt += 1
pick(vid, cnt)

# ---------------- 2-v03: flags RRR YY B, all used in a column; top and bottom not red
vid = "D05-math-2-v03"
sigs = set()
for perm in it.permutations("RRRYYB"):
    if perm[0] != "R" and perm[-1] != "R":
        sigs.add(perm)
pick(vid, len(sigs))

# ---------------- 2-v04: lattice A(0,0) -> B(4,3), E/N steps, avoid P(2,1)
vid = "D05-math-2-v04"
paths = set()
for steps in it.permutations("EEEENNN"):
    paths.add(steps)
cnt = 0
for steps in paths:
    x = y = 0
    ok = True
    for s in steps:
        if s == "E":
            x += 1
        else:
            y += 1
        if (x, y) == (2, 1):
            ok = False
            break
    if ok:
        cnt += 1
pick(vid, cnt)

# ---------------- 2-v05: 6 experts to towns A,B,C; each town >= 1, all three counts distinct
vid = "D05-math-2-v05"
cnt = 0
for f in it.product(range(3), repeat=6):
    sizes = [f.count(t) for t in range(3)]
    if min(sizes) >= 1 and len(set(sizes)) == 3:
        cnt += 1
pick(vid, cnt)

# ---------------- 2-v06: 6 people to 3 distinct streets, 2 each, jia & yi same street
vid = "D05-math-2-v06"
cnt = 0
for f in it.product(range(3), repeat=6):  # person 0 = jia, 1 = yi
    if all(f.count(t) == 2 for t in range(3)) and f[0] == f[1]:
        cnt += 1
pick(vid, cnt)

# ---------------- 2-v07: 5 volunteers to 3 distinct stations, each >= 1
vid = "D05-math-2-v07"
cnt = sum(1 for f in it.product(range(3), repeat=5) if len(set(f)) == 3)
pick(vid, cnt)

# ---------------- 2-v08: 8 teams paired into 4 unordered matches; GZ (0) and SZ (1) not paired


def matchings(items):
    if not items:
        yield []
        return
    a = items[0]
    for i in range(1, len(items)):
        b = items[i]
        rest = items[1:i] + items[i + 1:]
        for m in matchings(rest):
            yield [(a, b)] + m


vid = "D05-math-2-v08"
cnt = sum(1 for m in matchings(list(range(8))) if (0, 1) not in m)
pick(vid, cnt)

# ---------------- 2-v09: 12 identical AEDs to 3 communities, each >= 2
vid = "D05-math-2-v09"
cnt = sum(1 for a in range(13) for b in range(13) for c in range(13)
          if a + b + c == 12 and min(a, b, c) >= 2)
pick(vid, cnt)

# ---------------- 2-v10: rose + bougainvillea + jasmine = 10, each >= 1, rose even
vid = "D05-math-2-v10"
cnt = sum(1 for r in range(11) for s in range(11) for t in range(11)
          if r + s + t == 10 and min(r, s, t) >= 1 and r % 2 == 0)
pick(vid, cnt)

# ---------------- 2-v11: 10 quotas to 4 towns, each 1..4
vid = "D05-math-2-v11"
cnt = sum(1 for x in it.product(range(1, 5), repeat=4) if sum(x) == 10)
pick(vid, cnt)

# ---------------- report
bad = 0
for vid in qs:
    r = results.get(vid)
    if r is None:
        print(vid, "NOT SOLVED")
        bad += 1
        continue
    value, hits = r[0], r[1]
    extra = r[2] if len(r) > 2 else ""
    status = "OK" if len(hits) == 1 else "PROBLEM"
    if status != "OK":
        bad += 1
    print(f"{vid}: value={value} option={hits} {status} {extra}")
print("questions:", len(qs), "solved:", len(results), "problems:", bad)
