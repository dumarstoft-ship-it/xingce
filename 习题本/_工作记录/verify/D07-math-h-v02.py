# D07-math-h-v02: start-up zone = triangle ABC with area 5 km^2. D, E, F lie on the extensions of
# AB (beyond B), BC (beyond C) and CA (beyond A) with BD = 2AB, CE = BC, AF = 4CA. Area of triangle DEF?
# Method: build the points with exact coordinates for many random triangles, rescale to area 5,
# measure DEF by the shoelace formula, check that the result never depends on the shape, match options.
from fractions import Fraction as Fr
import random

S_ABC = 5
K_AB, K_BC, K_CA = 2, 1, 4          # BD = 2AB, CE = 1*BC, AF = 4CA


def area(P, Q, R):
    return abs((Q[0] - P[0]) * (R[1] - P[1]) - (R[0] - P[0]) * (Q[1] - P[1])) / 2


def beyond(P, Q, k):
    """the point X on ray PQ beyond Q with QX = k*PQ"""
    return (Q[0] + k * (Q[0] - P[0]), Q[1] + k * (Q[1] - P[1]))


random.seed(2026)
results = set()
tested = 0
while tested < 300:
    A, B, C = [(Fr(random.randint(-60, 60)), Fr(random.randint(-60, 60))) for _ in range(3)]
    s = area(A, B, C)
    if s == 0:
        continue
    D = beyond(A, B, K_AB)
    E = beyond(B, C, K_BC)
    F = beyond(C, A, K_CA)
    results.add(area(D, E, F) * S_ABC / s)       # rescale so that ABC has area 5
    tested += 1
assert len(results) == 1, results
total = results.pop()

opts = {'A': 40, 'B': 75, 'C': 105, 'D': 110}
hit = [k for k, v in opts.items() if v == total]
assert len(hit) == 1, (total, hit)

# where the distractors come from (documentation only)
only_extensions = S_ABC * (1 + K_AB * K_BC + K_BC * K_CA + K_CA * K_AB)   # both sides = extension parts
forgot_abc = total - S_ABC                                                # outer three blocks only
base_ratio_only = S_ABC * (1 + K_AB + K_BC + K_CA)                        # ignore that the height changes too
assert [base_ratio_only, only_extensions, forgot_abc] == [opts['A'], opts['B'], opts['C']]

print('area of DEF =', total, '(', total / S_ABC, 'times ABC )')
print(hit[0])
