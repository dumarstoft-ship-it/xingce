# D11-math-w2-v02: 74 firms in an industrial park, three support policies
#   R&D subsidy 38, rent reduction 34, talent subsidy 28
#   "got both X and Y" (pairwise, includes firms that got all three): R&D+rent 17, R&D+talent 12, rent+talent 8
#   6 firms got none
# Question: firms that got exactly two of the three.
# Method: brute force over the seven Venn regions (each >= 0) that reproduce every stem figure,
# collect the "exactly two" value of every consistent filling, require it to be unique, match the options.
from itertools import product

N, NONE = 74, 8
SET = {'R': 38, 'T': 34, 'H': 28}                       # R&D, renT, talent(H)
PAIR = {('R', 'T'): 17, ('R', 'H'): 12, ('T', 'H'): 8}  # pairwise counts incl. the triple region

vals = set()
for t in range(0, 29):                                   # all three
    for rt, rh, th in product(range(0, 18), range(0, 13), range(0, 9)):   # exactly-two regions
        if rt + t != PAIR[('R', 'T')] or rh + t != PAIR[('R', 'H')] or th + t != PAIR[('T', 'H')]:
            continue
        r = SET['R'] - rt - rh - t                       # only R&D
        tt = SET['T'] - rt - th - t                      # only rent
        h = SET['H'] - rh - th - t                       # only talent
        if min(r, tt, h) < 0:
            continue
        if r + tt + h + rt + rh + th + t + NONE != N:
            continue
        vals.add((rt + rh + th, t))
assert len(vals) == 1, vals
exactly_two, triple = vals.pop()

opts = {'A': 22, 'B': 27, 'C': 32, 'D': 37}
hit = [k for k, v in opts.items() if v == exactly_two]
assert len(hit) == 1, (exactly_two, hit)

# distractors (documentation only): subtract the triple 2 times / 1 time / not at all
P = sum(PAIR.values())
assert [P - 2 * triple, P - triple, P] == [opts['B'], opts['C'], opts['D']]
# reading the pairwise figures as "exactly these two" makes the data impossible (negative triple)
S = sum(SET.values())
assert (S - P - (N - NONE)) < 0

print('triple', triple, 'exactly two', exactly_two)
print(hit[0])
