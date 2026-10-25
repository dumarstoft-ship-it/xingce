"""Brute-force engine for truth-teller puzzles.
solve(worlds, stmts, ok_count, options, mode)
  worlds : iterable of world dicts
  stmts  : list of functions world->bool
  ok_count: function(n_true, n_total)->bool  (truth-count constraint)
  options: dict label->function(world)->bool  (or ->value for mode 'value')
  mode   : 'must_true' | 'must_false' | 'may_true'
Returns valid worlds and the option labels that satisfy the mode."""
import itertools

def bools(names):
    for vals in itertools.product([False, True], repeat=len(names)):
        yield dict(zip(names, vals))

def solve(worlds, stmts, ok_count, options, mode='must_true', extra=None):
    valid = []
    for w in worlds:
        if extra and not extra(w):
            continue
        t = sum(1 for s in stmts if s(w))
        if ok_count(t, len(stmts)):
            valid.append(w)
    res = []
    for lab, f in options.items():
        vals = [f(w) for w in valid]
        if mode == 'must_true' and valid and all(vals):
            res.append(lab)
        elif mode == 'must_false' and valid and not any(vals):
            res.append(lab)
        elif mode == 'may_true' and any(vals):
            res.append(lab)
    return valid, res

def exactly(k):
    return lambda t, n: t == k

def false_exactly(k):
    return lambda t, n: n - t == k

def false_at_most(k):
    return lambda t, n: n - t <= k

def report(name, valid, res, expect):
    flag = 'OK ' if res == expect else 'BAD'
    print(f'{flag} {name}: answer={res} expect={expect} | valid worlds={len(valid)}')
    if res != expect:
        for w in valid[:12]:
            print('     ', w)
