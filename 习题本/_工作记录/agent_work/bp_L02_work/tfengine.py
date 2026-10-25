"""Truth-teller puzzle engine for the L02 blueprint (independent re-implementation).

A spec is a dict:
  dom    : ('bool', [names])            -> every name True/False independently
           ('one',  [names])            -> exactly one name is 'x'
           ('k',    [names], k)         -> set S of exactly k names
           ('perm', [names], [slots])   -> injective assignment of slots to names (pos[name]); names
                                           without a slot get None (e.g. 5 teams, 3 prizes)
           ('custom', [world dicts])
  stmts  : list of (speaker, python-expression)      evaluated in the world namespace
  count  : ('true'|'false', op, k)   op in == <= >=   constraint on #true / #false statements
  ask    : must_true | must_false | may_true | undetermined
  opts   : {'A': expr, ...}   expressions may use T[i] (truth value of statement i, 0-based),
                              NT (#true statements) and the world names
  ans    : expected letter
Namespace for bool: each name -> bool; for one: x -> chosen name; for k: S -> frozenset;
for perm: pos -> dict name->slot or None, at -> dict slot->name.
"""
import itertools

def worlds(dom):
    kind = dom[0]
    if kind == 'bool':
        for vals in itertools.product([False, True], repeat=len(dom[1])):
            yield dict(zip(dom[1], vals))
    elif kind == 'one':
        for x in dom[1]:
            yield {'x': x}
    elif kind == 'k':
        for c in itertools.combinations(dom[1], dom[2]):
            yield {'S': frozenset(c)}
    elif kind == 'perm':
        names, slots = dom[1], dom[2]
        for p in itertools.permutations(names, len(slots)):
            at = dict(zip(slots, p))
            pos = {n: None for n in names}
            for s, n in at.items():
                pos[n] = s
            yield {'pos': pos, 'at': at}
    elif kind == 'custom':
        for w in dom[1]:
            yield dict(w)
    else:
        raise ValueError(kind)

OPS = {'==': lambda a, b: a == b, '<=': lambda a, b: a <= b, '>=': lambda a, b: a >= b}

def ev(expr, ns):
    return bool(eval(expr, {'any': any, 'all': all, 'sum': sum, 'len': len}, ns))

def solve(spec):
    valid = []
    for w in worlds(spec['dom']):
        ns = dict(w)
        T = [ev(e, ns) for _, e in spec['stmts']]
        nt = sum(T)
        side, op, k = spec['count']
        n = nt if side == 'true' else len(T) - nt
        if OPS[op](n, k):
            ns['T'] = T
            ns['NT'] = nt
            valid.append(ns)
    res = {}
    for lab, e in spec['opts'].items():
        vals = [ev(e, ns) for ns in valid]
        res[lab] = vals
    ask = spec['ask']
    good = []
    for lab, vals in res.items():
        if not valid:
            continue
        if ask == 'must_true' and all(vals): good.append(lab)
        elif ask == 'must_false' and not any(vals): good.append(lab)
        elif ask == 'may_true' and any(vals): good.append(lab)
        elif ask == 'undetermined' and any(vals) and not all(vals): good.append(lab)
    return valid, good

def check(name, spec, verbose=False):
    valid, good = solve(spec)
    ok = good == [spec['ans']]
    print(f"{'OK ' if ok else 'BAD'} {name}: answer={good} expect={spec['ans']} | valid worlds={len(valid)}")
    if (not ok) or verbose:
        for ns in valid[:10]:
            print('      ', {k: v for k, v in ns.items() if k not in ('T',)}, 'T=', ns['T'])
    return ok

def identity(people, types, says, allowed=None):
    """people: list; types: iterable of tuples of 'H'/'L'/'R'; says: {speaker: f(a)->bool}.
    H must say true, L must say false, R unconstrained. Returns list of consistent assignments."""
    out = []
    for tp in types:
        a = dict(zip(people, tp))
        if allowed and not allowed(a):
            continue
        ok = True
        for spk, f in says.items():
            v = f(a)
            if (a[spk] == 'H' and not v) or (a[spk] == 'L' and v):
                ok = False
        if ok:
            out.append(a)
    return out

def fixed_points(n, f, extra=(None,)):
    """truth vectors t of n self-referential statements with t == f(t, w)."""
    out = []
    for w in extra:
        for t in itertools.product([False, True], repeat=n):
            if list(t) == list(f(t, w)):
                out.append((t, w))
    return out
