"""数推改编题：每题用设计的规律算出答案，确认四个选项里恰好一个对；再拿一组常见规律去拟合题干（多级等差、等比、
差为等比、商为等差、一阶/二阶线性递推、乘积递推（含修正、三项）、平方递推、数字和递推、幂次组合（aⁿ ± n^k、nⁿ ± n、
2ⁿ + 3ⁿ 等）、对差/商再套一层规律、奇偶交叉），任何一个规律若能完全拟合题干却指向另一个选项，就报“有歧义”。
分组题另做公式搜索：c = α·ab + β·a + γ·b + δ·a² + ε·b² + ζ（小整数系数），能拟合所有完整组却指向别的选项的，列出来人工判断。
最后报两类“不找规律也能选”的捷径：数位题的选项众数、按趋势外推最接近的选项。"""
from fractions import Fraction as F
from itertools import product
import json, sys

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

def diffs(s): return [b - a for a, b in zip(s, s[1:])]

def dsum(x): return sum(map(int, str(int(x))))
def dprod(x):
    r = 1
    for c in str(int(x)): r *= int(c)
    return r

def fits(s, depth=0):
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
            rs = {s[i] - p * s[i - 1] - q * s[i - 2] for i in range(1 if q == 0 else 2, n)}
            if len(rs) == 1: out[f'{p}a+{q}b+常数'] = p * s[-1] + q * s[-2] + rs.pop()
        # a_n = p*a_{n-1} + q*a_{n-2} + (r + t*i): a sum of earlier terms plus an arithmetic correction
        for p, q, t in product(range(-2, 4), range(-2, 4), range(-3, 4)):
            if t == 0 or (p, q) == (0, 0): continue
            rs = {s[i] - p * s[i - 1] - q * s[i - 2] - t * i for i in range(1 if q == 0 else 2, n)}
            if len(rs) == 1: out[f'{p}a+{q}b+{t}i修正'] = p * s[-1] + q * s[-2] + rs.pop() + t * n
        for c in range(-5, 6):  # a_n = a_{n-1} * a_{n-2} + c
            if all(s[i] == s[i - 1] * s[i - 2] + c for i in range(2, n)): out[f'积+{c}'] = s[-1] * s[-2] + c
        for p, q, c in product(range(-2, 3), range(-2, 3), range(-3, 4)):  # a_n = ab + p·a + q·b + c, e.g. (b − 1)·a
            if (p, q, c) != (0, 0, 0) and all(s[i] == s[i - 1] * s[i - 2] + p * s[i - 1] + q * s[i - 2] + c for i in range(2, n)):
                out[f'积{p:+}a{q:+}b{c:+}'] = s[-1] * s[-2] + p * s[-1] + q * s[-2] + c
        for p, c in product(range(-2, 3), range(-3, 4)):  # a_n = a_{n-1}² + p·a_{n-2} + c
            if all(s[i] == s[i - 1] ** 2 + p * s[i - 2] + c for i in range(2, n)): out[f'平方{p:+}b{c:+}'] = s[-1] ** 2 + p * s[-2] + c
    if n >= 5:  # three-term: a + b·c, a·b + c, a + b + c with corrections
        for c in range(-3, 4):
            if all(s[i] == s[i - 1] + s[i - 2] * s[i - 3] + c for i in range(3, n)): out[f'a+bc{c:+}'] = s[-1] + s[-2] * s[-3] + c
            if all(s[i] == s[i - 1] * s[i - 2] + s[i - 3] + c for i in range(3, n)): out[f'ab+c{c:+}'] = s[-1] * s[-2] + s[-3] + c
            if all(s[i] == s[i - 1] + s[i - 2] + s[i - 3] + c for i in range(3, n)): out[f'三项和{c:+}'] = s[-1] + s[-2] + s[-3] + c
    # digit sums / products of the previous term
    if n >= 4 and all(x.denominator == 1 and x > 0 for x in s):
        for c in range(-2, 3):
            if all(s[i] == s[i - 1] + dsum(s[i - 1]) + c for i in range(1, n)): out[f'+数字和{c:+}'] = s[-1] + dsum(s[-1]) + c
            if all(s[i] == s[i - 1] + dprod(s[i - 1]) + c for i in range(1, n)): out[f'+数字积{c:+}'] = s[-1] + dprod(s[-1]) + c
    # power combinations, index starting at 0 or 1: α·xⁿ + β·n^k + γ, n^k + β·n^j + γ, nⁿ + β·n + γ, xⁿ + yⁿ + γ, n^k ± m alternating
    if n >= 4:
        for o in (0, 1):
            idx = [i + o for i in range(n)]; nx = n + o
            for x, k, a, b, g in product((2, 3), (1, 2, 3), (1, -1), (1, -1, 0), range(-3, 4)):
                if all(s[i] == a * x ** m + b * m ** k + g for i, m in enumerate(idx)): out[f'{a}·{x}ⁿ{b:+}·n^{k}{g:+}'] = a * x ** nx + b * nx ** k + g
            for k, j, b, g in product((2, 3), (0, 1, 2), (1, -1), range(-3, 4)):
                if all(s[i] == m ** k + b * m ** j + g for i, m in enumerate(idx)): out[f'n^{k}{b:+}n^{j}{g:+}'] = nx ** k + b * nx ** j + g
            for b, g in product((1, -1, 0), range(-3, 4)):
                if all(s[i] == F(m) ** m + b * m + g for i, m in enumerate(idx)): out[f'nⁿ{b:+}n{g:+}'] = F(nx) ** nx + b * nx + g
            for x, y, g in product((1, 2, 3), (2, 3, 4, 5), range(-2, 3)):
                if x < y and all(s[i] == x ** m + y ** m + g for i, m in enumerate(idx)): out[f'{x}ⁿ+{y}ⁿ{g:+}'] = x ** nx + y ** nx + g
            for k, mm, sg, lin in product((2, 3), (1, 2, 3), (1, -1), (0, 1)):
                corr = lambda m: sg * (-1) ** m * (m if lin else mm)
                if all(s[i] == m ** k + corr(m) for i, m in enumerate(idx)): out[f'n^{k}±交替{"n" if lin else mm}'] = nx ** k + corr(nx)
    # one more layer: a rule on the differences or on the ratios
    if depth == 0:
        d = diffs(s)
        if len(d) >= 4:
            for name, nv in fits(d, 1).items(): out['差·' + name] = s[-1] + nv
        if n >= 5 and all(x != 0 for x in s):
            r = [F(b) / F(a) for a, b in zip(s, s[1:])]
            for name, nv in fits(r, 1).items(): out['商·' + name] = s[-1] * nv
    # odd / even positions (blank is position n+1)
    if n >= 5:
        sub = s[n % 2::2] if False else [s[i] for i in range(n) if (i - n) % 2 == 0]  # same parity as the blank
        if len(sub) >= 3:
            for name, v in fits(sub, depth + 1).items():
                out['隔项·' + name] = v
    return out

def group_search(groups, last, options, value):
    """formulas c = α·ab + β·a + γ·b + δ·a² + ε·b² + ζ (small integers, at most 3 non-zero terms) that fit every complete group
    but give another option for the last group"""
    found = []
    for al, be, ga, de, ep in product((-1, 0, 1, 2), range(-3, 4), range(-3, 4), (-1, 0, 1), (-1, 0, 1)):
        zs = {c - (al * a * b + be * a + ga * b + de * a * a + ep * b * b) for a, b, c in groups}
        if len(zs) != 1: continue
        ze = zs.pop()
        if sum(1 for t in (al, be, ga, de, ep, ze) if t) > 3 or abs(ze) > 12: continue
        a, b = last
        v = al * a * b + be * a + ga * b + de * a * a + ep * b * b + ze
        for k, ov in options.items():
            if ov == v and v != value: found.append((f'{al}ab{be:+}a{ga:+}b{de:+}a²{ep:+}b²{ze:+}', k))
    return found

def shortcuts(q):
    """answers that can be picked without the rule: per-digit majority of the options (digit questions),
    and the option nearest to a plain trend extrapolation of the given terms"""
    notes = []
    opts = q['options']
    if all(v.denominator == 1 and v >= 1000 for v in opts.values()):
        strs = {k: str(int(v)) for k, v in opts.items()}
        if len(set(map(len, strs.values()))) == 1:
            from collections import Counter
            maj = ''.join(Counter(sv[i] for sv in strs.values()).most_common(1)[0][0] for i in range(len(next(iter(strs.values())))))
            cnts = [Counter(sv[i] for sv in strs.values()).most_common(2) for i in range(len(maj))]
            unique = all(len(c) == 1 or c[0][1] > c[1][1] for c in cnts)
            if unique and maj == str(int(q['value'])): notes.append('选项逐位众数就是答案')
    g = q.get('given')
    if g and len(g) >= 4:
        d = diffs(g)
        preds = {'线性': g[-1] + d[-1], '二级': g[-1] + d[-1] + (d[-1] - d[-2])}
        if all(x != 0 for x in g[-3:]): preds['等比'] = g[-1] * g[-1] / g[-2]
        near = {}
        for name, pv in preds.items():
            ranked = sorted(opts.items(), key=lambda kv: abs(kv[1] - pv))
            a, b = abs(ranked[0][1] - pv), abs(ranked[1][1] - pv)
            if ranked[0][1] == q['value'] and (b == 0 or a / b < 0.5): near[name] = round(float(pv), 3)
        if near: notes.append('按趋势外推最接近答案：' + str(near))
    return notes

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
        extra = []
        if q.get('groups'):
            full, last = q['groups']
            gs = group_search([tuple(map(F, t)) for t in full], tuple(map(F, last)), q['options'], q['value'])
            if gs: extra.append('分组公式另有指向：' + str(gs))
        extra += shortcuts(q)
        print(q['no'], ans, flag, '；'.join(extra))
    print('ambiguous:', bad)
