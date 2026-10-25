# Proposed rewrite of D01-math-1-v07 so it no longer duplicates the
# "work backwards from the final remainder" skeleton of 2-v06 / 2-v01.
# New condition: the 2nd payment equals exactly half of the contract total.
# Stem: 首期付总额的1/3少20万元；第二期付首期后余款的3/5多6万元；第二期付款额恰好占合同总额的一半；其余为尾款。求合同总额。
from fractions import Fraction as F

OPTS = {'A': 60, 'B': 120, 'C': 180, 'D': 260}

def pays(T, first_minus=20, plus2=6, keep_20_in_rest=True, scale_20=True):
    first = T / 3 - first_minus
    rest1 = T - first if keep_20_in_rest else T * F(2, 3)
    if scale_20:
        second = rest1 * F(3, 5) + plus2
    else:  # forgot to multiply the 20 inside the remainder by 3/5
        second = T * F(2, 5) + first_minus + plus2
    tail = T - first - second
    return first, second, tail

def solve(check_positive=True, **kw):
    out = []
    for t10 in range(1, 100001):                 # 0.1万元 steps
        T = F(t10, 10)
        f, s, t = pays(T, **kw)
        if check_positive and not (f > 0 and s > 0 and t > 0):
            continue
        if s == T / 2:
            out.append(T)
    return out

sol = solve()
assert sol == [180], sol
hits = [k for k, v in OPTS.items() if v == sol[0]]
assert hits == ['C']
print('payments', [str(x) for x in pays(F(180))])        # 40, 90, 50

# distractor error paths (each must give exactly one option value)
assert solve(False, scale_20=False) == [260]            # 20万元 not multiplied by 3/5: (20+6)/(1/10)
assert solve(False, keep_20_in_rest=False) == [60]      # remainder taken as 2T/3 only: 6/(1/10)
assert solve(False, plus2=0) == [120]                  # forgot the extra 6万元: 12/(1/10)
assert solve(False, plus2=-6) == [60]                   # sign slip on '多6' also lands on 60
# old answer-type distractor (3/5 of the total) has no positive solution -> not usable, fine
print('rewrite OK: unique answer C=180; distractors 260/60/120 traced')

# Alternative wording: "第二期比首期多付50万元" (also verified)
def solve_alt(**kw):
    out = []
    for t10 in range(1, 100001):
        T = F(t10, 10)
        f, s, t = pays(T, **kw)
        if f > 0 and s > 0 and t > 0 and s - f == 50:
            out.append(T)
    return out
assert solve_alt() == [180]
print('alt (second - first = 50): T =', solve_alt(), '| forgot 3/5 on 20 ->', solve_alt(scale_20=False),
      '| remainder 2T/3 ->', solve_alt(keep_20_in_rest=False), '| forgot +6 ->', solve_alt(plus2=0))
