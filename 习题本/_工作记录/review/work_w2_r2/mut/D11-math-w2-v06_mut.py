# D11-math-w2-v06: 58 residents at a Lingnan culture festival, each tried at least one of three booths
#   lion dance (L) 48, Cantonese opera (O) 44, Guangdong embroidery (E) 7
# Question: the minimum number of residents who tried two or more booths.
# Method: enumerate every non-negative filling of the seven regions (no "none" region) that
# reproduces the stem figures, minimise (exactly two + all three), match the options.
P, L, O, E = 58, 48, 40, 7

best, arg = None, None
maximum = None
for t in range(0, E + 1):                        # all three
    for le in range(0, E - t + 1):               # L+E only
        for oe in range(0, E - t - le + 1):      # O+E only
            e = E - t - le - oe                  # E only
            for lo in range(0, min(L, O) + 1):   # L+O only
                l = L - lo - le - t              # L only
                o = O - lo - oe - t              # O only
                if l < 0 or o < 0:
                    continue
                if l + o + e + lo + le + oe + t != P:
                    continue
                two_plus = lo + le + oe + t
                if best is None or two_plus < best:
                    best, arg = two_plus, dict(t=t, lo=lo, le=le, oe=oe, l=l, o=o, e=e)
                maximum = two_plus if maximum is None else max(maximum, two_plus)
assert best is not None

opts = {'A': 21, 'B': 27, 'C': 34, 'D': 41}
hit = [k for k, v in opts.items() if v == best]
assert len(hit) == 1, (best, hit)

# distractors (documentation only)
D = (L + O + E) - P                              # exactly two + 2 * all three
naive = D - D // 2                               # all three = floor(41/2) = 20, ignoring E = 7
exactly_two_only = D - 2 * arg['t']              # reported "exactly two" instead of "two or more"
assert [naive, exactly_two_only, maximum] == [opts['A'], opts['B'], opts['D']], (naive, exactly_two_only, maximum)
assert arg['t'] == E and best == L + O - P       # cap = the smallest set; equals the L/O overlap bound

print('optimum', arg, '-> two or more min', best, '(max', maximum, ')')
print(hit[0])
