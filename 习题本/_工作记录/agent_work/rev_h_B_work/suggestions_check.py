# Exact enumeration of the deepened versions proposed in the review (so the suggestions are usable).
from fractions import Fraction as F
from itertools import combinations, product
from math import comb

days = range(5)
subs = list(combinations(days, 2))

# --- v02 deepened: 3 lawyers each pick 2 of Mon-Fri; P(every pair of lawyers shares >= 1 day)
tot = good = 0
for a, b, c in product(subs, repeat=3):
    tot += 1
    sa, sb, sc = set(a), set(b), set(c)
    if sa & sb and sa & sc and sb & sc:
        good += 1
ans = F(good, tot)
print("v02-deep  P(all pairs overlap) =", ans, float(ans))
print("   independence trap 0.7^3 =", F(7, 10) ** 3, float(F(7, 10) ** 3))
print("   no add-back 1-3*0.3 =", 1 - 3 * F(3, 10))
print("   complement only (forgot 1-) =", 1 - ans)
# all three pairwise disjoint impossible?
print("   #triples pairwise disjoint =", sum(1 for a, b, c in product(subs, repeat=3)
                                            if not (set(a) & set(b)) and not (set(a) & set(c)) and not (set(b) & set(c))))

# --- v02 alt: Zhang 2 days, Liu 3 days; P(some day both present AND some day nobody)
subs3 = list(combinations(days, 3))
tot = good = 0
for a in subs:
    for b in subs3:
        tot += 1
        both = set(a) & set(b)
        nobody = set(days) - set(a) - set(b)
        good += bool(both) and bool(nobody)
print("v02-alt   P(both-day and empty-day) =", F(good, tot))

# --- v09 deepened: choose 3 of 6; given A or B chosen, P(A and B both chosen)
shops = range(6)
tri = list(combinations(shops, 3))
cond = [s for s in tri if 0 in s or 1 in s]
both = [s for s in cond if 0 in s and 1 in s]
print("v09-deep  |cond| =", len(cond), "|both| =", len(both), "P =", F(len(both), len(cond)))
givenA = [s for s in tri if 0 in s]
print("   trap 'given A chosen' P(B|A) =", F(sum(1 for s in givenA if 1 in s), len(givenA)))
print("   trap unconditional P(both) =", F(sum(1 for s in tri if 0 in s and 1 in s), len(tri)))
print("   trap 'three classes equally likely' = 1/3")
# original-size alternative: choose 2 of 6, P(both | at least one)
pairs = list(combinations(shops, 2))
c2 = [s for s in pairs if 0 in s or 1 in s]
print("v09-alt2  choose 2: P(both | >=1) =", F(sum(1 for s in c2 if 0 in s and 1 in s), len(c2)),
      " vs P(B | A) =", F(1, 5))

# --- v08 deepened: box A 3 sci + 2 hist, box B 2 sci + 3 hist, move 2 from A to B, draw 1 from B
boxA = ["S"] * 3 + ["H"] * 2
boxB = ["S"] * 2 + ["H"] * 3
num = den = 0
case = {}
for moved in combinations(range(5), 2):
    k = sum(boxA[i] == "S" for i in moved)
    case[k] = case.get(k, 0) + 1
    newB = boxB + [boxA[i] for i in moved]
    for book in newB:
        den += 1
        num += book == "S"
print("v08-deep  P(sci) =", F(num, den), " cases (#sci moved -> count of 10):", case)
print("   trick (2 + 2*3/5)/7 =", (2 + 2 * F(3, 5)) / 7)
print("   trap most-likely case (1 sci moved) =", F(3, 7), "; assume 2 sci =", F(4, 7),
      "; ignore =", F(2, 5), "; mean of boxes =", (F(3, 5) + F(2, 5)) / 2)
