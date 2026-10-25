# D03-math-h-v01: 甲 and 乙 leave gate A at the same time and walk along the embankment towards gate B
# (60 and 75 m/min); at the same moment 丙 leaves gate B for gate A (65 m/min). 丙 meets 乙 first and
# meets 甲 6 minutes later. Find the length AB (metres).
# Method: exact event simulation. For a candidate length S the positions measured from A are
# x甲 = 60t, x乙 = 75t, x丙 = S - 65t (each walker stops at the far gate). A meeting is the first moment two
# positions coincide strictly inside the embankment. Scan every integer S up to 30000 m, keep the S whose
# 丙-乙 meeting comes first and the 丙-甲 meeting exactly 6 minutes later; the solution must be unique and
# exactly one option must satisfy the stem.
from fractions import Fraction as F

V_JIA, V_YI, V_BING, DELAY = 60, 75, 65, 6
OPTIONS = {'A': 3640, 'B': 6250, 'C': 7000, 'D': 7840}


def pos(v, t, S, from_b=False):
    """Position (from A) at time t of a walker with speed v who stops at the far gate."""
    d = min(v * t, S)
    return S - d if from_b else d


def first_meeting(S, v, check=False):
    """First time 丙 and a walker from A (speed v) are at the same point strictly inside AB."""
    # positions are piecewise linear; before anyone stops the gap S - (v + V_BING) t closes linearly,
    # so the coincidence time is where that gap is 0; check it against the stop rule explicitly
    t = F(S, v + V_BING)
    if pos(v, t, S) == pos(V_BING, t, S, from_b=True) and 0 < pos(v, t, S) < S:
        if check:  # no earlier coincidence: 丙 is still strictly ahead on a fine grid before t
            assert all(pos(V_BING, u, S, True) > pos(v, u, S) for u in (t * F(i, 200) for i in range(200)))
        return t
    return None


def fits(S, check=False):
    t_yi, t_jia = first_meeting(S, V_YI, check), first_meeting(S, V_JIA, check)
    return None not in (t_yi, t_jia) and t_yi < t_jia and t_jia - t_yi == DELAY


sols = [S for S in range(1, 30001) if fits(S)]
assert len(sols) == 1, sols
hits = [k for k, v in OPTIONS.items() if fits(v, check=True)]
assert len(hits) == 1 and OPTIONS[hits[0]] == sols[0], hits
S = sols[0]
t_yi = first_meeting(S, V_YI)
# at the 丙-乙 meeting the 甲-乙 gap equals what 甲 and 丙 close in the next 6 minutes
assert pos(V_YI, t_yi, S) - pos(V_JIA, t_yi, S) == (V_JIA + V_BING) * DELAY
# distractors: gap taken as (乙+丙)x6; gap taken as 丙x6 (甲 forgotten); 50 min paired with 甲+丙
assert (V_YI + V_BING) * DELAY / F(V_YI - V_JIA) * (V_YI + V_BING) == OPTIONS['D']
assert V_BING * DELAY / F(V_YI - V_JIA) * (V_YI + V_BING) == OPTIONS['A']
assert (V_JIA + V_BING) * t_yi == OPTIONS['B']
print('AB =', S, 'm; 丙 meets 乙 at', t_yi, 'min')
print(hits[0])
