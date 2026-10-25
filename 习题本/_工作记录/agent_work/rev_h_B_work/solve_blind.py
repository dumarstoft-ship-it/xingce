# Blind independent solver for revh_B (D06 probability, 10 items).
# Every answer is computed by exact enumeration of the sample space (Fractions),
# starting only from the stem data; options are matched afterwards.
from fractions import Fraction as F
from itertools import combinations, product
import json, sys

QFILE = sys.argv[1]
qs = {q["vid"]: q for q in json.load(open(QFILE, encoding="utf-8"))}


def opt_value(s):
    """Parse an option string into a Fraction."""
    s = s.strip().replace("$", "")
    if s.startswith("\\frac"):
        a, b = s[len("\\frac{"):].rstrip("}").split("}{")
        return F(int(a), int(b))
    if s.endswith("%"):
        return F(s[:-1]) / 100
    return F(s)


def match(vid, val):
    hits = [k for k, v in qs[vid]["options"].items() if opt_value(v) == val]
    return hits


res = {}

# ---------- v01: 5 pairs of gloves, draw 4, exactly one pair ----------
gloves = [(s, side) for s in range(5) for side in "LR"]
tot = good = 0
cnt_by_pairs = {}
for c in combinations(gloves, 4):
    tot += 1
    styles = [g[0] for g in c]
    npairs = sum(1 for s in set(styles) if styles.count(s) == 2)
    cnt_by_pairs[npairs] = cnt_by_pairs.get(npairs, 0) + 1
    if npairs == 1:
        good += 1
res["D06-math-h-v01"] = F(good, tot)
print("v01 counts by #pairs", cnt_by_pairs, "total", tot)

# ---------- v02: two lawyers each pick 2 of 5 days; P(share >=1 day) ----------
days = range(5)
subs = list(combinations(days, 2))
tot = good = 0
overlap_dist = {}
for a in subs:
    for b in subs:
        tot += 1
        k = len(set(a) & set(b))
        overlap_dist[k] = overlap_dist.get(k, 0) + 1
        if k >= 1:
            good += 1
res["D06-math-h-v02"] = F(good, tot)
print("v02 overlap dist", overlap_dist, "total", tot)

# ---------- v03: A 2 shots p=.6, B 2 shots p=.5; P(A makes > B makes) ----------
pA, pB = F(3, 5), F(1, 2)
pr_gt = pr_eq = pr_lt = F(0)
for a1, a2, b1, b2 in product([0, 1], repeat=4):
    w = 1
    for x, p in ((a1, pA), (a2, pA), (b1, pB), (b2, pB)):
        w *= p if x else 1 - p
    sa, sb = a1 + a2, b1 + b2
    if sa > sb:
        pr_gt += w
    elif sa == sb:
        pr_eq += w
    else:
        pr_lt += w
res["D06-math-h-v03"] = pr_gt
print("v03 P(>)", pr_gt, "P(=)", pr_eq, "P(<)", pr_lt, "P(>=)", pr_gt + pr_eq)

# ---------- v04: calls until 2nd success (p=.6); P(exactly 4 calls) ----------
p = F(3, 5)
tot4 = F(0)
dist = {}
for n in range(1, 9):
    for seq in product([0, 1], repeat=n):
        # sequence is a complete record iff the 2nd success happens exactly at call n
        if sum(seq) == 2 and seq[-1] == 1:
            w = 1
            for x in seq:
                w *= p if x else 1 - p
            dist[n] = dist.get(n, 0) + w
res["D06-math-h-v04"] = dist[4]
print("v04 P(N=n)", {k: str(v) for k, v in dist.items()}, " P(N<=4)", sum(dist[k] for k in (2, 3, 4)))

# ---------- v05: scheme review tree, Bayes ----------
p_init, p_re, p_fin = F(2, 5), F(3, 10), F(1, 2)
paths = {}  # path -> prob
for init in (1, 0):
    w0 = p_init if init else 1 - p_init
    if init:
        for fin in (1, 0):
            paths[("init", fin)] = w0 * (p_fin if fin else 1 - p_fin)
    else:
        for re in (1, 0):
            w1 = w0 * (p_re if re else 1 - p_re)
            if re:
                for fin in (1, 0):
                    paths[("re", fin)] = w1 * (p_fin if fin else 1 - p_fin)
            else:
                paths[("out",)] = w1
assert sum(paths.values()) == 1
adopted = paths[("init", 1)] + paths[("re", 1)]
res["D06-math-h-v05"] = paths[("re", 1)] / adopted
print("v05 P(adopted)", adopted, " P(re & adopted)", paths[("re", 1)])

# ---------- v06: deuce, p=2/3, need 2-point lead; exact Markov solve ----------
p, q = F(2, 3), F(1, 3)
# states: lead in {-1,0,+1}; absorbing at +-2. x0 = p x1 + q x_-1 ; x1 = p + q x0 ; x_-1 = p x0
# substitute: x0 = p(p + q x0) + q(p x0) = p^2 + 2pq x0  => x0 = p^2/(1-2pq)
x0 = p * p / (1 - 2 * p * q)
res["D06-math-h-v06"] = x0
# brute-force check: enumerate point sequences up to length 40 (truncated series)
def deuce_trunc(nmax):
    tot = F(0)
    # dynamic programming over lead states
    state = {0: F(1)}
    win = F(0)
    for _ in range(nmax):
        new = {}
        for lead, w in state.items():
            for d, pr in ((1, p), (-1, q)):
                nl = lead + d
                if nl == 2:
                    win += w * pr
                elif nl == -2:
                    pass
                else:
                    new[nl] = new.get(nl, 0) + w * pr
        state = new
    return win
print("v06 exact", x0, " truncated(40)=", float(deuce_trunc(40)), " truncated(4)=", deuce_trunc(4))

# ---------- v07: households weighted ----------
households = []
for b in range(40):
    done = b < 32  # 80% of 40 buildings
    households += [done] * 24
for b in range(20):
    done = b < 19  # 95% of 20 buildings
    households += [done] * 72
res["D06-math-h-v07"] = F(sum(households), len(households))
print("v07", sum(households), "/", len(households))

# ---------- v08: move 2 from box A (4S,1H) to box B (2S,3H), draw 1 from B ----------
boxA = ["S"] * 4 + ["H"]
boxB = ["S"] * 2 + ["H"] * 3
num = den = 0
for moved in combinations(range(5), 2):
    newB = boxB + [boxA[i] for i in moved]
    for book in newB:
        den += 1
        num += book == "S"
res["D06-math-h-v08"] = F(num, den)
print("v08", F(num, den))

# ---------- v09: choose 2 of 6; given (A or B) chosen, P(A chosen) ----------
shops = range(6)  # 0 = A, 1 = B
pairs = list(combinations(shops, 2))
cond = [s for s in pairs if 0 in s or 1 in s]
withA = [s for s in cond if 0 in s]
both = [s for s in cond if 0 in s and 1 in s]
res["D06-math-h-v09"] = F(len(withA), len(cond))
print("v09 |cond|", len(cond), "|A|", len(withA), "|both|", len(both))

# ---------- v10: two-stage quiz, backward induction ----------
p1, p2 = F(4, 5), F(3, 10)
ev_stop = F(100)
ev_cont = p2 * 400 + (1 - p2) * 0
best_after_q1 = max(ev_stop, ev_cont)
ev_total = p1 * best_after_q1
res["D06-math-h-v10"] = ev_total
print("v10 after Q1: stop", ev_stop, "continue", ev_cont, "-> overall E", ev_total,
      " (if he always stopped:", p1 * ev_stop, ")")

print()
out = {}
for vid in qs:
    val = res[vid]
    hits = match(vid, val)
    out[vid] = hits
    print(vid, "value", val, "=", float(val), "-> option(s)", hits)
    assert len(hits) == 1, vid
json.dump({k: v[0] for k, v in out.items()},
          open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
