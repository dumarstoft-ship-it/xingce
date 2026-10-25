# D03-math-2-v13: A is due west of B. Ship 甲 sails east from A, ship 乙 sails west from B at the same time,
# speed(甲) = 4/3 speed(乙). After they meet, 乙 turns due north (same speed), 甲 keeps sailing east.
# When 甲 reaches B the ships are 75 nautical miles apart. Find AB.
# Method: coordinates (x east, y north), for each option AB compute the exact positions when 甲 reaches B and
# compare the squared distance with 75^2; also scan AB on a fine grid to show the solution is unique.
from fractions import Fraction as F

RATIO, FINAL = F(4, 3), F(75)
OPTIONS = {'A': 100, 'B': 105, 'C': 140, 'D': 175}


def dist2_when_jia_at_B(S, v_yi=F(1)):
    v_jia = RATIO * v_yi
    t_meet = S / (v_jia + v_yi)
    C = v_jia * t_meet                       # x of the meeting point
    t_end = S / v_jia                        # 甲 reaches B
    jia = (S, F(0))
    yi = (C, v_yi * (t_end - t_meet))        # 乙 went north from C
    return (jia[0] - yi[0]) ** 2 + (jia[1] - yi[1]) ** 2


hits = [k for k, v in OPTIONS.items() if dist2_when_jia_at_B(F(v)) == FINAL ** 2]
assert len(hits) == 1, hits
grid = [F(s, 4) for s in range(4, 4 * 400)]
assert [s for s in grid if dist2_when_jia_at_B(s) == FINAL ** 2] == [OPTIONS[hits[0]]]
# distractors: 75 taken as CB; legs added instead of hypotenuse; meeting split reversed (CB = 4/7 AB)
assert 75 * F(7, 3) == OPTIONS['D']
assert FINAL / (1 + F(3, 4)) * F(7, 3) == OPTIONS['A']
assert FINAL / F(5, 4) / F(4, 7) == OPTIONS['B']
print('AB =', OPTIONS[hits[0]])
print(hits[0])
