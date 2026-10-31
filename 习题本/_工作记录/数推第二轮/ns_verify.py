"""数推改编题：每题用设计的规律算出答案，确认四个选项里恰好一个对；再拿一组常见规律去拟合题干（多级等差、等比、
差为等比、商为等差、一阶/二阶线性递推、乘积递推、奇偶交叉），任何一个规律若能完全拟合题干却指向另一个选项，就报“有歧义”。"""
from fractions import Fraction as F
from itertools import product
import json, sys

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

def diffs(s): return [b - a for a, b in zip(s, s[1:])]

def fits(s):
    """predictions of the next term from every simple rule that reproduces all given terms"""
    out = {}
    n = len(s)
    # k-th differences constant (needs at least 2 equal values at that level)
    d, lvl = list(s), 0
    while len(d) >= 3 and lvl < 3:
        d = diffs(d); lvl += 1
        if len(d) >= 2 and len(set(d)) == 1:
            nxt = d[-1]; stack = [s]
            for _ in range(lvl): stack.append(diffs(stack[-1]))
            v = nxt
            for k in range(lvl - 1, -1, -1): v = stack[k][-1] + v
            out[f'{lvl}级差等差'] = v
            break
    # geometric, differences geometric, ratios arithmetic
    if all(x != 0 for x in s[:-1]):
        r = [F(b) / F(a) for a, b in zip(s, s[1:])]
        if len(set(r)) == 1: out['等比'] = s[-1] * r[0]
        rd = diffs(r)
        if len(rd) >= 2 and len(set(rd)) == 1: out['商为等差'] = s[-1] * (r[-1] + rd[0])
    d1 = diffs(s)
    if len(d1) >= 3 and all(x != 0 for x in d1[:-1]):
        q = [F(b) / F(a) for a, b in zip(d1, d1[1:])]
        if len(set(q)) == 1: out['差为等比'] = s[-1] + d1[-1] * q[0]
    if len(d1) >= 3 and all(x in PRIMES for x in d1) and d1 == PRIMES[PRIMES.index(d1[0]):PRIMES.index(d1[0]) + len(d1)]:
        out['差为连续质数'] = s[-1] + PRIMES[PRIMES.index(d1[-1]) + 1]
    # a_n = a_{n-1} * (i + k) + c   and   a_n = p*a_{n-1} + c*(-1)^i   and   a_n = p*a_{n-1} + (r + t*i)
    if n >= 4:
        for k in range(-1, 3):
            cs = {s[i] - s[i - 1] * (i + k) for i in range(1, n)}
            if len(cs) == 1: out[f'×(n+{k})+常数'] = s[-1] * (n + k) + cs.pop()
        for p in range(-4, 5):
            cs = {(s[i] - p * s[i - 1]) * (-1) ** i for i in range(1, n)}
            if len(cs) == 1 and p != 0: out[f'×{p}±交替'] = p * s[-1] + cs.pop() * (-1) ** n
            for t in (-3, -2, -1, 1, 2, 3):
                rs = {s[i] - p * s[i - 1] - t * i for i in range(1, n)}
                if len(rs) == 1 and p not in (0, 1): out[f'×{p}+{t}i修正'] = p * s[-1] + rs.pop() + t * n
    # a_n = p*a_{n-1} + q
    if n >= 4:
        for p in range(-4, 5):
            qs = {s[i] - p * s[i - 1] for i in range(1, n)}
            if len(qs) == 1 and p not in (0, 1): out[f'×{p}+常数'] = p * s[-1] + qs.pop()
    # a_n = p*a_{n-1} + q*a_{n-2} + r
    if n >= 5:
        for p, q in product(range(-3, 4), repeat=2):
            if (p, q) in ((0, 0), (1, 0)): continue
            rs = {s[i] - p * s[i - 1] - q * s[i - 2] for i in range(2, n)}
            if len(rs) == 1: out[f'{p}a+{q}b+常数'] = p * s[-1] + q * s[-2] + rs.pop()
        # a_n = p*a_{n-1} + q*a_{n-2} + (r + t*i): a sum of earlier terms plus an arithmetic correction
        for p, q, t in product(range(-2, 4), range(-2, 4), range(-3, 4)):
            if t == 0 or (p, q) == (0, 0): continue
            rs = {s[i] - p * s[i - 1] - q * s[i - 2] - t * i for i in range(2, n)}
            if len(rs) == 1: out[f'{p}a+{q}b+{t}i修正'] = p * s[-1] + q * s[-2] + rs.pop() + t * n
        for c in range(-5, 6):  # a_n = a_{n-1} * a_{n-2} + c
            if all(s[i] == s[i - 1] * s[i - 2] + c for i in range(2, n)): out[f'积+{c}'] = s[-1] * s[-2] + c
    # odd / even positions (blank is position n+1)
    if n >= 5:
        sub = s[n % 2::2] if False else [s[i] for i in range(n) if (i - n) % 2 == 0]  # same parity as the blank
        if len(sub) >= 3:
            for name, v in fits(sub).items():
                out['隔项·' + name] = v
    return out

def check(q):
    """q: {'no', 'given': list (numbers) or None, 'value': correct value, 'options': {letter: value}}"""
    hit = [k for k, v in q['options'].items() if v == q['value']]
    assert len(hit) == 1, (q['no'], 'options matching the answer', hit)
    amb = {}
    if q.get('given'):
        for name, v in fits(q['given']).items():
            for k, ov in q['options'].items():
                if ov == v and k != hit[0]: amb[name] = k
    return hit[0], amb

if __name__ == '__main__':
    qs = json.load(open(sys.argv[1]))
    bad = 0
    for q in qs:
        q['value'] = F(q['value'])
        q['options'] = {k: F(v) for k, v in q['options'].items()}
        q['given'] = [F(x) for x in q['given']] if q.get('given') else None
        ans, amb = check(q)
        flag = 'AMBIGUOUS ' + str(amb) if amb else ''
        bad += bool(amb)
        print(q['no'], ans, flag)
    print('ambiguous:', bad)
