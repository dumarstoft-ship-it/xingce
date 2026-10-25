# D03-math-2-v05: karts start together at the start line, same direction; 甲 36 s/lap, 乙 84 s/lap.
# Count how many times 甲 catches 乙 from the start until both are first back at the start line together
# (start not counted, that final moment counted).
# Method: track length 2520 units -> integer speeds 70 and 30 units/s; step 1 s, detect the first time both are
# at the start line, and count catches as the number of times the unwrapped lead of 甲 reaches a multiple of L.
L = 2520
v1, v2 = L // 36, L // 84
assert v1 * 36 == L and v2 * 84 == L
OPTIONS = {'A': 3, 'B': 4, 'C': 5, 'D': 7}

t, catches = 0, 0
while True:
    t += 1
    lead_prev, lead = (v1 - v2) * (t - 1), (v1 - v2) * t
    catches += lead // L - lead_prev // L        # each new full lap of lead = one catch
    if (v1 * t) % L == 0 and (v2 * t) % L == 0:  # both at the start line
        break
hits = [k for k, v in OPTIONS.items() if v == catches]
assert len(hits) == 1, (catches, hits)
assert catches - 1 == OPTIONS['A'] and catches + 1 == OPTIONS['C'] and v1 * t // L == OPTIONS['D']
print('both back at start at t =', t, 's; laps', v1 * t // L, v2 * t // L, '; catches', catches)
print(hits[0])
