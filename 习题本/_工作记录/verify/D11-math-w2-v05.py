# D11-math-w2-v05: 126 overseas buyers at a trade fair
#   attended the on-site matchmaking session: 88; visited factories: 79
#   attended neither: at most 16
# Question: the minimum number of buyers who took part in exactly one of the two activities.
# Method: enumerate the four regions (both, session only, factory only, neither) over all
# non-negative integers that match the stem, take the minimum of "exactly one", match the options.
N, S, F, NEITHER_MAX = 126, 88, 79, 16

best, arg = None, None
for both in range(0, min(S, F) + 1):
    s_only, f_only = S - both, F - both
    neither = N - (s_only + f_only + both)
    if neither < 0 or neither > NEITHER_MAX:
        continue
    one = s_only + f_only
    if best is None or one < best:
        best, arg = one, (both, s_only, f_only, neither)
assert best is not None

opts = {'A': 9, 'B': 53, 'C': 69, 'D': 85}
hit = [k for k, v in opts.items() if v == best]
assert len(hit) == 1, (best, hit)

# distractors (documentation only)
both_min_set = S + F - 2 * min(S, F)          # "both" pushed to min(88,79): neither would be 38 > 16
assert N - (S + F - min(S, F)) > NEITHER_MAX
forget_neither = N - arg[0]                   # 126 - 57: the 16 "neither" not subtracted
maximum = S + F - 2 * (S + F - N)             # the largest value (neither = 0)
assert [both_min_set, forget_neither, maximum] == [opts['A'], opts['C'], opts['D']]
assert all(v % 2 for v in opts.values())      # exactly-one is always odd here; parity must not eliminate options

print('both, session only, factory only, neither =', arg, '-> exactly one min', best)
print(hit[0])
