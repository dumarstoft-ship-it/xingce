from fractions import Fraction as F

def state(d, S):
    """walker that has travelled distance d from end 0 (heading to S first): (pos from 0, dir just after)"""
    k, r = divmod(d, S)
    return (r, 1) if k % 2 == 0 else (S - r, -1)

def meetings(S, sp1, sp2, start2_at_B, horizon):
    """event-based list of (t, pos_from_A, kind) for two bouncing walkers; walker1 starts at A."""
    turns = set([F(0)])
    for sp, off in ((sp1, 0), (sp2, 0)):
        k = 1
        while k * S / sp <= horizon:
            turns.add(k * S / sp); k += 1
    turns.add(horizon)
    ts = sorted(turns)
    out = []
    def st(i, t):
        if i == 1:
            return state(sp1 * t, S)
        p, d = state(sp2 * t, S)
        return (S - p, -d) if start2_at_B else (p, d)
    for a, b in zip(ts, ts[1:]):
        p1, d1 = st(1, a); p2, d2 = st(2, a)
        rel = d1 * sp1 - d2 * sp2
        if rel == 0:
            if p1 == p2: out.append((a, p1, 'coincide'))
            continue
        t = a + (p2 - p1) / rel
        if a <= t <= b:
            if t == 0: continue
            # direction at meeting moment: use mid-interval directions
            kind = 'head-on' if d1 != d2 else 'overtake'
            pos = p1 + d1 * sp1 * (t - a)
            if not out or out[-1][0] != t:
                out.append((t, pos, kind))
    return out

# v01 check: S=900, 70/50 same end
m = meetings(F(900), F(70), F(50), False, F(200))
print('v01', [(float(t), float(p), k) for t, p, k in m[:6]])
# blueprint 3-7-2 original numbers
m = meetings(F(1000), F(60), F(40), False, F(200))
print('bp 3-7-2', [(float(t), float(p), k) for t, p, k in m[:6]])
# v02: scan S
sols = []
sols_any = []
for S2 in range(41*4, 400*4):
    S = F(S2, 4)
    sp1, sp2 = F(40), S - 40
    m = meetings(S, sp1, sp2, True, F(10))
    ho = [x for x in m if x[2] == 'head-on']
    assert ho[0][1] == 40, (S, ho[0])
    if len(ho) >= 2 and ho[1][1] == 60: sols.append(S)
    if len(m) >= 2 and m[1][1] == 60: sols_any.append((S, m[1][2]))
print('v02 S with 2nd head-on at 60:', sols)
print('v02 S with 2nd meeting of any kind at 60:', sols_any)
