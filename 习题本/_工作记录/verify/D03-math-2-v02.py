# D03-math-2-v02: trucks 甲 (from A) and 乙 (from B) start together towards each other, turn back instantly at the
# far end, constant speeds. 1st head-on meeting 40 km from A, 2nd head-on meeting 60 km from A. Find AB.
# Method: for every candidate AB = S (scan on a 0.25 km grid, plus every option), the speed ratio is fixed by the
# first meeting (甲:乙 = 40:(S-40)); simulate the bouncing motion event by event and keep the S whose 2nd
# head-on meeting is 60 km from A.
from fractions import Fraction as F

OPTIONS = {'A': 60, 'B': 70, 'C': 90, 'D': 120}
FIRST, SECOND = F(40), F(60)


def state(d, S):
    k, r = divmod(d, S)
    return (r, 1) if k % 2 == 0 else (S - r, -1)


def meetings(S, v1, v2, horizon):
    def st1(t):
        return state(v1 * t, S)

    def st2(t):                       # 乙 starts at B heading to A
        p, d = state(v2 * t, S)
        return S - p, -d
    ev = {F(0), horizon}
    for v in (v1, v2):
        k = 1
        while k * S / v <= horizon:
            ev.add(k * S / v)
            k += 1
    ts = sorted(ev)
    out = []
    for a, b in zip(ts, ts[1:]):
        (p1, d1), (p2, d2) = st1(a), st2(a)
        rel = d1 * v1 - d2 * v2
        if rel == 0:
            continue
        t = a + (p2 - p1) / rel
        if a <= t <= b and t > 0 and (not out or out[-1][0] != t):
            out.append((t, p1 + d1 * v1 * (t - a), 'head-on' if d1 != d2 else 'overtake'))
    return out


def second_head_on_ok(S):
    v1, v2 = FIRST, S - FIRST          # time unit = time of the first meeting
    m = meetings(S, v1, v2, F(10))
    ho = [x for x in m if x[2] == 'head-on']
    assert ho[0][1] == FIRST
    return len(ho) >= 2 and ho[1][1] == SECOND


cands = sorted({F(x, 4) for x in range(41 * 4, 400 * 4)} | {F(v) for v in OPTIONS.values() if v > FIRST})
sols = [S for S in cands if second_head_on_ok(S)]
assert sols == [90], sols
hits = [k for k, v in OPTIONS.items() if v > FIRST and second_head_on_ok(F(v))]
assert len(hits) == 1 and OPTIONS[hits[0]] == sols[0], hits
# note: if overtaking also counted as "meeting", S = 240 would fit too -> the stem must say 迎面
alt = [S for S in (F(90), F(240)) if (lambda m: len(m) >= 2 and m[1][1] == SECOND)(meetings(S, FIRST, S - FIRST, F(10)))]
print('S =', sols, '| any-kind 2nd meeting at 60 km for S in', alt)
print(hits[0])
