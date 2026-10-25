# -*- coding: utf-8 -*-
"""Independent re-verification engine for the L02 blueprint (written from scratch in this run; it does not
reuse tfengine.py). Worlds are plain dicts; statements and options are Python callables.

check(tag, worlds, stmts, count, ask, opts, expect)
  worlds : iterable of dicts
  stmts  : list of callables w -> bool
  count  : callable (n_true, n_total) -> bool  (the truth-count restriction given in the stem)
  ask    : 'must'   一定为真 / 可以推出 / 必然正确
           'never'  一定为假 / 不可能为真 / 必然错误
           'may'    可能为真
           'undet'  真假无法确定
  opts   : {'A': callable (w, T) -> bool, ...}   T = tuple of statement truth values
  expect : the intended letter
Returns True iff exactly the intended letter satisfies the asked criterion.
"""
import itertools

RESULTS = []


def bools(names):
    for vals in itertools.product([False, True], repeat=len(names)):
        yield dict(zip(names, vals))


def choose_one(items, key='x'):
    for it in items:
        yield {key: it}


def subsets_of_size(items, k, key='S'):
    for c in itertools.combinations(items, k):
        yield {key: frozenset(c)}


def valid_worlds(worlds, stmts, count):
    out = []
    for w in worlds:
        T = tuple(bool(s(w)) for s in stmts)
        if count(sum(T), len(T)):
            out.append((w, T))
    return out


def judge(valid, opts, ask):
    good = []
    for lab, f in opts.items():
        vals = [bool(f(w, T)) for w, T in valid]
        if not vals:
            continue
        if ask == 'must' and all(vals):
            good.append(lab)
        elif ask == 'never' and not any(vals):
            good.append(lab)
        elif ask == 'may' and any(vals):
            good.append(lab)
        elif ask == 'undet' and any(vals) and not all(vals):
            good.append(lab)
    return good


def check(tag, worlds, stmts, count, ask, opts, expect, show=False, note=''):
    valid = valid_worlds(list(worlds), stmts, count)
    good = judge(valid, opts, ask)
    ok = good == [expect]
    RESULTS.append((tag, ok))
    print(f"{'OK ' if ok else 'BAD'} {tag}: hits={good} expect={expect} | valid={len(valid)} {note}")
    if show or not ok:
        for w, T in valid[:12]:
            print('       ', w, ''.join('T' if t else 'F' for t in T))
    return ok


def record(tag, ok, msg=''):
    RESULTS.append((tag, bool(ok)))
    print(f"{'OK ' if ok else 'BAD'} {tag}: {msg}")
    return ok


# truth-count helpers
def exactly_true(k):
    return lambda n, tot: n == k


def exactly_false(k):
    return lambda n, tot: tot - n == k


def at_most_false(k):
    return lambda n, tot: tot - n <= k


def at_most_true(k):
    return lambda n, tot: n <= k


def more_true_than_false():
    return lambda n, tot: n > tot - n


def summary():
    bad = [t for t, ok in RESULTS if not ok]
    print('-' * 60)
    print(f'{len(RESULTS)} checks, {len(RESULTS) - len(bad)} OK, {len(bad)} BAD', bad if bad else '')
    return not bad
