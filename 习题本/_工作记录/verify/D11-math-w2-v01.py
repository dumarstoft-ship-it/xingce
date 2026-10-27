# D11-math-w2-v01: government service hall, one day.
#   reserved online: 1/5 of them must hand in missing materials
#   not reserved:    2/5 of them must hand in missing materials
#   (people who must hand in materials) = (people who reserved) - 16
#   neither reserved nor need to hand in materials: 30 people
# Question: total number of people that day.
# Method: brute force over the 2x2 table (reserved / not reserved) x (hand in / not), keep every
# integer filling that satisfies all stem conditions, require a unique total, then match the options.
from fractions import Fraction as Fr

R_RES, R_NOT = Fr(1, 5), Fr(2, 5)      # share needing materials, among reserved / among not reserved
LESS, NEITHER = 16, 30

sols = set()
for res in range(1, 400):                 # people who reserved
    for nres in range(1, 400):            # people who did not reserve
        res_hand, nres_hand = R_RES * res, R_NOT * nres
        if res_hand.denominator != 1 or nres_hand.denominator != 1:
            continue
        res_hand, nres_hand = int(res_hand), int(nres_hand)
        neither = nres - nres_hand        # not reserved and no materials needed
        hand = res_hand + nres_hand       # everyone who must hand in materials
        if neither == NEITHER and hand == res - LESS:
            sols.add((res, nres, res + nres))
assert len(sols) == 1, sols
res, nres, total = sols.pop()

opts = {'A': 65, 'B': 77, 'C': 86, 'D': 95}
hit = [k for k, v in opts.items() if v == total]
assert len(hit) == 1, (total, hit)

# where the distractors come from (documentation only; the answer above does not use these)
# (1) read the 30 people as the whole "not reserved" row: hand-in among them 2/5*30 = 12
nh = R_NOT * NEITHER
r1 = (nh + LESS) / (1 - R_RES)
wrong_row = r1 + NEITHER                  # total = reserved + 30
wrong_base = r1 + NEITHER + nh            # 2/5 taken of the 30, then row = 30 + 12
# (2) count materials only in the "not reserved" row (forget reserved & hand-in cell)
forget_cell = (R_NOT * nres + LESS) + nres
assert [wrong_row, wrong_base, forget_cell] == [opts['A'], opts['B'], opts['C']], (wrong_row, wrong_base, forget_cell)

print('reserved', res, 'not reserved', nres, 'total', total)
print(hit[0])
