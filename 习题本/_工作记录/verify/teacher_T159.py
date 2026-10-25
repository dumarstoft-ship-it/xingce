# teacher T159（2021四川下）3月x日(x≤10)与4月y日(y≥20)都是星期五，x+y=32，求y
OPTS = {'A': 24, 'B': 25, 'C': 26, 'D': 27}
MARCH = 31
sols = [(x, y) for x in range(1, 11) for y in range(20, 31)
        if x + y == 32 and ((MARCH - x) + y) % 7 == 0]
print(sols)
assert len(sols) == 1
hits = [k for k, v in OPTS.items() if v == sols[0][1]]
assert len(hits) == 1, hits
print(hits[0])
