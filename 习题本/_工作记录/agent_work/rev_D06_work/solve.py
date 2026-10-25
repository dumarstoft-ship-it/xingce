# Independent blind solver for D06 math questions (probability module).
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import comb
import json, re, sys

Q = json.load(open(sys.argv[1]))
res = {}

def parse_opt(s):
    s = s.strip()
    m = re.search(r'\\frac\{(\d+)\}\{(\d+)\}', s)
    if m: return F(int(m.group(1)), int(m.group(2)))
    m = re.search(r'([\d.]+)\s*%', s)
    if m: return F(m.group(1)) / 100
    m = re.search(r'([\d.]+)', s)
    if m: return F(m.group(1))
    return None

# Q1: 6 zongzi, salted x < bean 6-x, P(exactly one salted)=8/15
sols = [x for x in range(0, 7) if x < 6 - x and F(x * (6 - x), comb(6, 2)) == F(8, 15)]
assert len(sols) == 1
x = sols[0]
# brute force over labelled items
items = ['S'] * x + ['B'] * (6 - x)
pairs = list(combinations(range(6), 2))
res['D06-math-1-v01'] = F(sum(1 for a, b in pairs if items[a] == 'B' and items[b] == 'B'), len(pairs))

# Q2: choose 4 of n; P(both not chosen) = 11 * P(both chosen)
def q2(n):
    ppl = range(n)
    tot = nn = yy = 0
    for s in combinations(ppl, 4):
        tot += 1
        a, b = (0 in s), (1 in s)
        nn += (not a and not b)
        yy += (a and b)
    return F(nn, tot), F(yy, tot)
cand = []
for n in range(5, 25):
    pn, py = q2(n)
    if pn == 11 * py:
        cand.append(n)
res['D06-math-1-v02'] = cand

# Q3: 3 type-A, 5 type-B windows; choose 3; both types present
w = ['A'] * 3 + ['B'] * 5
cs = list(combinations(range(8), 3))
res['D06-math-1-v03'] = F(sum(1 for c in cs if len({w[i] for i in c}) == 2), len(cs))

# Q4: 4 people each choose among 6 groups; at least two share
outs = list(product(range(6), repeat=4))
res['D06-math-1-v04'] = F(sum(1 for o in outs if len(set(o)) < 4), len(outs))

# Q5: balls 1..9 choose 2; sum multiple of 3
cs = list(combinations(range(1, 10), 2))
res['D06-math-1-v05'] = F(sum(1 for a, b in cs if (a + b) % 3 == 0), len(cs))

# Q6: two dice, max == 5
outs = list(product(range(1, 7), repeat=2))
res['D06-math-1-v06'] = F(sum(1 for a, b in outs if max(a, b) == 5), len(outs))

# Q7: 7 spots, 3 distinct cars; exactly two adjacent and third not adjacent to them
def q7_ok(pos):
    s = sorted(pos)
    adj = [(s[i + 1] - s[i] == 1) for i in range(2)]
    return sum(adj) == 1  # exactly one adjacent pair => third not adjacent to either
outs = list(permutations(range(7), 3))
res['D06-math-1-v07'] = F(sum(1 for o in outs if q7_ok(o)), len(outs))

# Q8: 9 seats, 3 people, any two at least 2 empty seats between (index diff >= 3)
outs = list(permutations(range(9), 3))
def q8_ok(o):
    s = sorted(o)
    return all(s[i + 1] - s[i] - 1 >= 2 for i in range(2))
res['D06-math-1-v08'] = F(sum(1 for o in outs if q8_ok(o)), len(outs))

# Q9: 10 lamps all on; 3 ops, each picks random 2 distinct lamps, toggles; P(lamp #0 on)
pairs = list(combinations(range(10), 2))
on = tot = 0
allon = 0
for ops in product(pairs, repeat=3):
    cnt = [0] * 10
    for p in ops:
        for i in p: cnt[i] += 1
    tot += 1
    on += (cnt[0] % 2 == 0)
    allon += all(c % 2 == 0 for c in cnt)
res['D06-math-1-v09'] = F(on, tot)
res['_q9_all_on_alt'] = F(allon, tot)

# Q10: 8 people randomly paired into 4 pairs; P(person0 and person1 together)
def pairings(lst):
    if not lst:
        yield []
        return
    a = lst[0]
    for i in range(1, len(lst)):
        b = lst[i]
        rest = lst[1:i] + lst[i + 1:]
        for p in pairings(rest):
            yield [(a, b)] + p
allp = list(pairings(list(range(8))))
res['D06-math-1-v10'] = F(sum(1 for p in allp if (0, 1) in p), len(allp))

# Q11: Wang picks 2 of 5 days, Li 3 of 5, Chen 4 of 5; exactly two on Wednesday (day 2)
days = range(5)
tot = good = 0
for a in combinations(days, 2):
    for b in combinations(days, 3):
        for c in combinations(days, 4):
            tot += 1
            good += ((2 in a) + (2 in b) + (2 in c) == 2)
res['D06-math-1-v11'] = F(good, tot)

# Q12: 12 combos, try without repetition in random order; opens exactly on 3rd attempt
combos = [(d, l) for d in range(1, 5) for l in 'ABC']
n = len(combos)
# enumerate all orderings of first 3 attempts (uniform w/o replacement), correct = combos[0]
tot = good = 0
for seq in permutations(range(n), 3):
    tot += 1
    good += (seq[0] != 0 and seq[1] != 0 and seq[2] == 0)
res['D06-math-1-v12'] = F(good, tot)

# Q13: 9 people (5 Z, 4 D); 3 weeks with replacement; exactly 2 weeks Z
ppl = ['Z'] * 5 + ['D'] * 4
outs = list(product(range(9), repeat=3))
res['D06-math-1-v13'] = F(sum(1 for o in outs if sum(ppl[i] == 'Z' for i in o) == 2), len(outs))

# Q14: p=0.8, 4 trials, at least 3 successes
p = F(4, 5)
tot = F(0)
for o in product([0, 1], repeat=4):
    pr = F(1)
    for v in o: pr *= p if v else (1 - p)
    if sum(o) >= 3: tot += pr
res['D06-math-1-v14'] = tot

# Q15: two experts each 0.5; both pass -> in; none -> out; one -> review r; overall 0.4; solve r
# P = 0.25 + 0.5 r -> linear; solve
pe = F(1, 2)
both = pe * pe; one = 2 * pe * (1 - pe)
r = (F(2, 5) - both) / one
res['D06-math-2-v01'] = r

# Q16: theory p=0.8 with 1 retake; practical p=0.6 with 1 retake; sequential
def pass_with_retake(q):
    tot = F(0)
    for o in product([0, 1], repeat=2):
        pr = F(1)
        for v in o: pr *= q if v else (1 - q)
        if o[0] == 1 or o[1] == 1: tot += pr  # 2nd attempt only matters if first failed
    return tot
res['D06-math-2-v02'] = pass_with_retake(F(4, 5)) * pass_with_retake(F(3, 5))

# Q17: best of three, p=0.6 per game
p = F(3, 5)
tot = F(0)
for o in product([0, 1], repeat=3):  # play all 3 conceptually; winner = majority
    pr = F(1)
    for v in o: pr *= p if v else (1 - p)
    if sum(o) >= 2: tot += pr
res['D06-math-2-v03'] = tot

# Q18: 0.75 p + 0.25 (1-p) = 0.40
res['D06-math-2-v04'] = (F(40, 100) - F(25, 100)) / (F(75, 100) - F(25, 100))

# Q19: ratio 5:3:2, defect 2%,3%,5%
w = [F(5, 10), F(3, 10), F(2, 10)]; d = [F(2, 100), F(3, 100), F(5, 100)]
pd = sum(a * b for a, b in zip(w, d))
res['D06-math-2-v05'] = pd

# Q20: each day metro 0.6 (ontime 0.9), bus 0.4 (ontime 0.6); two days indep; both on time
tot = F(0)
modes = [(F(6, 10), F(9, 10)), (F(4, 10), F(6, 10))]
for m1, m2 in product(modes, repeat=2):
    tot += m1[0] * m1[1] * m2[0] * m2[1]
res['D06-math-2-v06'] = tot

# Q21: Bayes line 3 given defect
res['D06-math-2-v07'] = w[2] * d[2] / pd

# Q22: prevalence 2%, sens 95%, FPR 5%
prev = F(2, 100); se = F(95, 100); fp = F(5, 100)
res['D06-math-2-v08'] = prev * se / (prev * se + (1 - prev) * fp)

# Q23: meeting within 12 min in 60 min window; exact area + grid check
exact = 1 - F(48, 60) ** 2
N = 600
cnt = sum(1 for i in range(N) for j in range(N) if abs((i + 0.5) - (j + 0.5)) * 60 / N <= 12)
res['D06-math-2-v09'] = exact
res['_q23_grid'] = cnt / N / N

# Q24: 20 tickets: 1x200, 3x50, 6x10, rest 0
tickets = [200] + [50] * 3 + [10] * 6 + [0] * 10
res['D06-math-2-v10'] = F(sum(tickets), len(tickets))

# Q25: typhoon 0.2, loss 50; insure premium 6, payout 80% of loss
no_ins = F(2, 10) * 50
ins = 6 + F(2, 10) * 50 * (1 - F(8, 10))
res['D06-math-2-v11'] = (no_ins, ins, no_ins - ins)

# ---- match to options ----
out = {}
for q in Q:
    vid = q['vid']; v = res[vid]; opts = q['options']
    matches = []
    if vid == 'D06-math-1-v02':
        for k, s in opts.items():
            if int(re.search(r'\d+', s).group()) in v: matches.append(k)
    elif vid == 'D06-math-1-v13':
        x = float(v)
        rng = {'A': (0, .30), 'B': (.30, .40), 'C': (.40, .50), 'D': (.50, 1.01)}
        matches = [k for k, (lo, hi) in rng.items() if lo <= x < hi]
    elif vid == 'D06-math-2-v08':
        x = float(v)
        vals = {k: float(parse_opt(s)) for k, s in opts.items()}
        best = min(vals, key=lambda k: abs(vals[k] - x))
        matches = [best]
    elif vid == 'D06-math-2-v11':
        no_ins, ins, diff = v
        better = '投保' if ins < no_ins else '不投保'
        amt = abs(diff)
        for k, s in opts.items():
            m = re.search(r'少\s*([\d.]+)\s*万', s)
            if s.startswith(better + '更划算') and m and F(m.group(1)) == amt:
                matches.append(k)
    else:
        for k, s in opts.items():
            pv = parse_opt(s)
            if pv is not None and abs(float(pv) - float(v)) < 5e-4:
                matches.append(k)
    out[vid] = matches
    vs = v if not isinstance(v, tuple) else tuple(str(t) for t in v)
    print(f"{vid}: computed={vs} ({float(v) if not isinstance(v,(tuple,list)) else ''}) -> options matched {matches}")
print('Q9 alt reading (all lamps on):', res['_q9_all_on_alt'], float(res['_q9_all_on_alt']))
print('Q23 grid check:', res['_q23_grid'])
json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
