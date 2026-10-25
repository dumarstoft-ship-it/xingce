# D03-math-2-v04: 500 m loop, same direction; 乙 starts 100 m AHEAD of 甲 and is 1.25 times as fast.
# How far has 乙 run when he catches 甲 for the 2nd time?
# Method: integer simulation (甲 4 m, 乙 5 m per time unit, i.e. ratio 1.25), positions mod 500; record the
# instants when they are at the same point (乙 coming from behind since he is faster).
L = 500
OPTIONS = {'A': 3000, 'B': 3600, 'C': 4000, 'D': 4500}
v_jia, v_yi = 4, 5
assert v_yi / v_jia == 1.25
x_jia0, x_yi0 = 0, 100

catches, t = [], 0
while len(catches) < 2:
    t += 1
    if (x_jia0 + v_jia * t) % L == (x_yi0 + v_yi * t) % L:
        catches.append(t)
d_yi = v_yi * catches[1]
hits = [k for k, v in OPTIONS.items() if v == d_yi]
assert len(hits) == 1, (d_yi, hits)
# distractors: treating 乙 as 100 m behind (gain 100+500); gain 400 each time; 甲's distance
assert 5 * (100 + 500) == OPTIONS['A'] and v_jia * catches[1] == OPTIONS['B'] and 5 * (400 + 400) == OPTIONS['C']
print('catch times', catches, '乙 distance', d_yi)
print(hits[0])
