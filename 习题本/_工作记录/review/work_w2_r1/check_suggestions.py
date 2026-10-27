# Independent checks of the replacement distractors / variant proposed in the review.
from fractions import Fraction as F
from itertools import product

# ---- Q1 D09: proposed option set {20, 45, 46, 47}
stock = [30, 16, 9, 6, 2]
bad = max(sum(c) for c in product(*[range(s + 1) for s in stock]) if sum(x >= 5 for x in c) < 2)
print("Q1 correct", bad + 1, "| 戊 as 4, no +1:", 30 + 4 * 4, "| 戊 as 4, +1:", 30 + 4 * 4 + 1,
      "| template 4x4+2 then +2:", 4 * 4 + 2 + 2)

# ---- Q5 D10-v04: proposed replacement for 654 (cost at B, no natural error path)
lighter_ok = [6 * 2, 10 * 4, 7 * 5, 20 * 5, 14 * 3]
lighter_forgetC = [6 * 2, 10 * 4, 7 * 5, 17 * 5, 14 * 3]   # C-E segment: A+B+D only, junction C's 3 t forgotten
print("Q5 correct", 2 * sum(lighter_ok), "| forgot C's 3 t on C-E:", 2 * sum(lighter_forgetC),
      "| direct sum at E without C:", 2 * (6 * 11 + 4 * 9 + 7 * 10 + 14 * 3),
      "| forgot x2:", sum(lighter_ok))

# ---- Q6 D12 variant: 丙 46 -> 51
def ranks(pB, pC, need_most):
    out = {}
    for nB in range(1, 1600):
        for nC in range(1, 1600 - nB):
            nD = 1600 - nB - nC
            if need_most and not nD > max(400, nB, nC):
                continue
            x = F(80000 - pB * nB - pC * nC, nD)
            if x <= 0:
                continue
            r = 1 + sum(o > x for o in (40, pB, pC))
            tie = any(o == x for o in (40, pB, pC))
            out[(r, tie)] = out.get((r, tie), 0) + 1
    return out
print("Q6 original (49,46) with 'most':", ranks(49, 46, True))
print("Q6 variant  (49,51) with 'most':", ranks(49, 51, True))
print("Q6 variant  (49,51) w/o  'most':", ranks(49, 51, False))
# error path "丁 has the most orders so its value is close to the overall 48":
x = 48
print("   丁≈48 in variant -> rank", 1 + sum(o > x for o in (40, 49, 51)),
      "| 丁≈48 in original -> rank", 1 + sum(o > x for o in (40, 49, 46)))
