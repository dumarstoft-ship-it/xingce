# D11-math-w2-v04: 80 farm households; machines: drone (U), tractor (T), rotary tiller (R)
#   households WITHOUT a tractor all have NO rotary tiller
#   among households with a rotary tiller, one half also have a drone
#   among households with a tractor, 1/3 have a rotary tiller
#   drone only: 14; drone + tractor but no tiller: 10; none of the three: 18
# Question: households with a drone.
# Method: enumerate all eight regions (non-negative integers, total 80), keep the fillings that satisfy
# every stem sentence literally, collect the number of drone owners, require uniqueness, match options.
from fractions import Fraction as Fr

N, U_ONLY, UT_ONLY, NONE = 80, 14, 10, 12
HALF, THIRD = Fr(1, 2), Fr(1, 3)

drone_vals = set()
rest = N - U_ONLY - UT_ONLY - NONE            # t_only + r_only + ur_only + tr_only + utr
for t in range(rest + 1):                     # tractor only
    for r in range(rest - t + 1):             # tiller only
        for ur in range(rest - t - r + 1):    # drone + tiller, no tractor
            for tr in range(rest - t - r - ur + 1):     # tractor + tiller, no drone
                utr = rest - t - r - ur - tr  # all three
                # "without a tractor -> no tiller": regions (tiller only) and (drone+tiller only) are empty
                if r + ur != 0:
                    continue
                tiller = r + ur + tr + utr
                tractor = t + UT_ONLY + tr + utr
                if tiller == 0 or tiller * HALF != ur + utr:
                    continue
                if tractor * THIRD != tiller:
                    continue
                drone_vals.add(U_ONLY + UT_ONLY + ur + utr)
assert len(drone_vals) == 1, drone_vals
drone = drone_vals.pop()

opts = {'A': 24, 'B': 32, 'C': 35, 'D': 40}
hit = [k for k, v in opts.items() if v == drone]
assert len(hit) == 1, (drone, hit)

# distractors (documentation only)
tractor = N - U_ONLY - NONE
forget_triple = U_ONLY + UT_ONLY                              # drone owners without the all-three cell
tractor_wrong = N - U_ONLY                                    # forget the 18 "none" outside the tractor set
forget_none = U_ONLY + UT_ONLY + tractor_wrong * THIRD * HALF
third_as_cell = U_ONLY + UT_ONLY + tractor * THIRD            # 1/3 read as "tractor+tiller only", then all-three = same
assert [forget_triple, forget_none, third_as_cell] == [opts['A'], opts['C'], opts['D']], (forget_triple, forget_none, third_as_cell)

print('tractor', tractor, 'drone', drone)
print(hit[0])
