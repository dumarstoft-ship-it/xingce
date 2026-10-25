# T195（2020北京乡镇）个人票10元/张，团体票60元/张（可供10人），58人最少付多少元。
PEOPLE, SINGLE, GROUP, GROUP_SIZE = 58, 10, 60, 10
OPTS = {'A': 350, 'B': 360, 'C': 380, 'D': 390}
best = min(GROUP * g + SINGLE * s
           for g in range(PEOPLE // GROUP_SIZE + 2)
           for s in range(PEOPLE + 1)
           if g * GROUP_SIZE + s >= PEOPLE)
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1, (best, hits)
print('min cost =', best)
print(hits[0])
