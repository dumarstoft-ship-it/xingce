"""L07 结构相似 形式核对器（bp_L07_work 专用）。

约定
----
* 文字（literal）：'A' 或 '~A'。
* 语句：
    ('imp', [前件...], 后件, *flags)   条件/全称；后件可为文字或 ('and'|'or'|'xor', [...])
         flags: 'dn' = 原句是“不A就不B / 没有A就没有B / 除非A否则不B”这类双否定写法
                       （lit 视角按字面 ~A→~B；std 视角改写为 B→A）
                'w'  = 非必然（往往、大多、通常、较难……）
    ('and'|'or'|'xor', [...])        联言 / 相容选言 / 不相容选言（要么…要么…）
    ('not', 语句)                     负命题（并非……）
    ('some', X, Y) / ('most', X, Y)   有的X是Y / 多数(许多)X是Y；X、Y 为文字
    ('rel', kind, X, Y)               关系命题；kind='T' 可传递（大于、早于、位于上游），
                                      'N' 不可传递（朋友、相邻、认识）
* 论证：dict(rules=[...], facts=[...], concl=..., case=None|'x')
    case = 个案（某人/某地/该企业/我国……），以 ('imp',[case],X) 写出的前提折成事实 X。
    没写 case 时，若结论是单前件条件句、且有前提以同一前件开头，自动把该前件当个案
    （所以“a→b，b→c ⊢ a→c”与“所有b是c，x是b ⊢ x是c”同构——与官方解析的
    “1→2，3→1，因此 3→2”一致）。
* 事实折进结论前件（演绎定理）：规则＋事实 ⊢ 结论  ≡  规则 ⊢ (事实→结论)。
  于是“规则＋个案事实”与“规则 ⊢ 条件句结论”可以直接比较（2025GD-62 型）。
* 结构签名 = 在“原子改名＋单个原子整体取反”下的最小表示；前提视为集合。
  不做逆否等价变换——肯前≠否后、否前≠肯后，与考试口径一致。
  结论前件有两个及以上文字时，允许在等价的几种写法间转换（2023GD-72 C 型改写）。
* 视角（views）：trans ∈ {lit, std} × q ∈ {strict, loose}
    loose：许多/多数 与 有的 视为同一量词；“有的X是Y”不分先后。
  判定标准：正确项在两个 loose 视角下都与题干同签名；
            每个干扰项在全部四个视角下都与题干不同签名。
"""
import itertools

# ---------------------------------------------------------------- helpers
def neg(l):
    return l[1:] if l.startswith('~') else '~' + l

def atom(l):
    return l.lstrip('~')

def is_lit(x):
    return isinstance(x, str)

def is_imp(x):
    return isinstance(x, tuple) and x[0] == 'imp'

def mk_imp(ants, cons, flags=()):
    return ('imp', list(ants), cons) + tuple(flags)

def imp_flags(x):
    return tuple(x[3:]) if is_imp(x) else ()

def atoms_of(x, acc=None):
    if acc is None:
        acc = set()
    if is_lit(x):
        acc.add(atom(x))
        return acc
    h = x[0]
    if h == 'imp':
        for a in x[1]:
            atoms_of(a, acc)
        atoms_of(x[2], acc)
    elif h in ('and', 'or', 'xor'):
        for a in x[1]:
            atoms_of(a, acc)
    elif h == 'not':
        atoms_of(x[1], acc)
    elif h in ('some', 'most'):
        atoms_of(x[1], acc); atoms_of(x[2], acc)
    elif h == 'rel':
        atoms_of(x[2], acc); atoms_of(x[3], acc)
    elif h == 'fact':
        atoms_of(x[1], acc)
    else:
        raise ValueError(h)
    return acc

# ---------------------------------------------------------------- translation views
def translate(x, trans):
    """std: 'dn' 条件句 ~A→~B 改写成 B→A。"""
    if is_lit(x):
        return x
    h = x[0]
    if h == 'imp':
        fl = imp_flags(x)
        ants = [translate(a, trans) for a in x[1]]
        cons = translate(x[2], trans)
        if trans == 'std' and 'dn' in fl and len(ants) == 1 and is_lit(cons):
            rest = tuple(f for f in fl if f != 'dn')
            return mk_imp([neg(cons)], neg(ants[0]), rest)
        return mk_imp(ants, cons, tuple(f for f in fl if f != 'dn'))
    if h in ('and', 'or', 'xor'):
        return (h, [translate(a, trans) for a in x[1]])
    if h == 'not':
        return ('not', translate(x[1], trans))
    return x

def translate_arg(arg, trans):
    out = dict(arg)
    out['rules'] = [translate(r, trans) for r in arg.get('rules', [])]
    out['facts'] = [translate(f, trans) for f in arg.get('facts', [])]
    out['concl'] = translate(arg['concl'], trans)
    return out

# ---------------------------------------------------------------- normalisation (case folding)
def normalize(arg):
    rules = list(arg.get('rules', []))
    facts = list(arg.get('facts', []))
    concl = arg['concl']
    case = arg.get('case')
    explicit = case is not None
    if not explicit and is_imp(concl) and len(concl[1]) == 1:
        cand = concl[1][0]
        if any(is_imp(r) and r[1] == [cand] and is_lit(r[2]) and 'w' not in imp_flags(r) for r in rules):
            case = cand
    if case:
        keep = []
        for r in rules:
            if is_imp(r) and r[1] == [case] and (explicit or (is_lit(r[2]) and 'w' not in imp_flags(r))):
                facts.append(r[2])
            else:
                keep.append(r)
        rules = keep
        if is_imp(concl) and case in concl[1]:
            ant = [a for a in concl[1] if a != case]
            concl = mk_imp(ant, concl[2], imp_flags(concl)) if ant else concl[2]
        elif isinstance(concl, tuple) and concl[0] in ('some', 'most'):
            pass
    if facts:
        lits, others = [], []
        for f in facts:
            if is_lit(f):
                lits.append(f)
            elif f[0] == 'and' and all(is_lit(z) for z in f[1]):
                lits.extend(f[1])
            else:
                others.append(f)
        if lits:
            if is_lit(concl) or concl[0] in ('and', 'or', 'xor'):
                concl = mk_imp(lits, concl)
            elif is_imp(concl):
                concl = mk_imp(lits + list(concl[1]), concl[2], imp_flags(concl))
            else:
                rules = rules + [('fact', f) for f in lits]
        rules = rules + [('fact', f) for f in others]
    return rules, concl

def conj_rotations(concl):
    """(A∧B)→C 的等价改写：(A∧¬C)→¬B、(B∧¬C)→¬A。仅用于两个以上前件、后件为文字的结论。"""
    if not (is_imp(concl) and len(concl[1]) >= 2 and is_lit(concl[2])):
        return [concl]
    fl = imp_flags(concl)
    clause = [neg(a) for a in concl[1]] + [concl[2]]
    outs = []
    for i, c in enumerate(clause):
        ants = [neg(z) for j, z in enumerate(clause) if j != i]
        outs.append(mk_imp(ants, c, fl))
    return outs

# ---------------------------------------------------------------- signature
def ren(x, m):
    if is_lit(x):
        n, f = m[atom(x)]
        return ('~' if (x.startswith('~') ^ f) else '') + n
    h = x[0]
    if h == 'imp':
        return mk_imp([ren(a, m) for a in x[1]], ren(x[2], m), imp_flags(x))
    if h in ('and', 'or', 'xor'):
        return (h, [ren(a, m) for a in x[1]])
    if h == 'not':
        return ('not', ren(x[1], m))
    if h in ('some', 'most'):
        return (h, ren(x[1], m), ren(x[2], m))
    if h == 'rel':
        return ('rel', x[1], ren(x[2], m), ren(x[3], m))
    if h == 'fact':
        return ('fact', ren(x[1], m))
    raise ValueError(h)

def fmt(x, q):
    if is_lit(x):
        return x
    h = x[0]
    if h == 'imp':
        tag = 'imp' + ('w' if 'w' in imp_flags(x) else '')
        return tag + '([' + ','.join(sorted(fmt(a, q) for a in x[1])) + '];' + fmt(x[2], q) + ')'
    if h in ('and', 'or', 'xor'):
        return h + '(' + ','.join(sorted(fmt(a, q) for a in x[1])) + ')'
    if h == 'not':
        return 'not(' + fmt(x[1], q) + ')'
    if h in ('some', 'most'):
        hh = 'some' if (q == 'loose') else h
        a, b = fmt(x[1], q), fmt(x[2], q)
        if hh == 'some' and q == 'loose':
            a, b = sorted([a, b])
        return hh + '(' + a + ';' + b + ')'
    if h == 'rel':
        return 'rel' + x[1] + '(' + fmt(x[2], q) + ';' + fmt(x[3], q) + ')'
    if h == 'fact':
        return 'fact(' + fmt(x[1], q) + ')'
    raise ValueError(h)

def signature(arg, trans='lit', q='loose'):
    a2 = translate_arg(arg, trans)
    rules, concl = normalize(a2)
    alts = conj_rotations(concl)
    acc = set()
    for r in rules:
        atoms_of(r, acc)
    atoms_of(concl, acc)
    al = sorted(acc)
    names = [chr(ord('P') + i) for i in range(len(al))]
    best = None
    for perm in itertools.permutations(names):
        for flips in itertools.product([False, True], repeat=len(al)):
            m = {a: (perm[i], flips[i]) for i, a in enumerate(al)}
            rs = sorted(fmt(ren(r, m), q) for r in rules)
            c = min(fmt(ren(z, m), q) for z in alts)
            rep = '{' + ' , '.join(rs) + '} |- ' + c
            if best is None or rep < best:
                best = rep
    return best

VIEWS = [('lit', 'loose'), ('std', 'loose'), ('lit', 'strict'), ('std', 'strict')]

# ---------------------------------------------------------------- validity
def ev(x, v):
    if is_lit(x):
        return (not v[atom(x)]) if x.startswith('~') else v[x]
    h = x[0]
    if h == 'imp':
        return (not all(ev(a, v) for a in x[1])) or ev(x[2], v)
    if h == 'and':
        return all(ev(a, v) for a in x[1])
    if h == 'or':
        return any(ev(a, v) for a in x[1])
    if h == 'xor':
        return sum(1 for a in x[1] if ev(a, v)) == 1
    if h == 'not':
        return not ev(x[1], v)
    if h == 'fact':
        return ev(x[1], v)
    raise ValueError(h)

def has_quant(x):
    if is_lit(x):
        return False
    if x[0] in ('some', 'most'):
        return True
    if x[0] == 'rel':
        return False
    if x[0] == 'imp':
        return any(has_quant(a) for a in x[1]) or has_quant(x[2])
    if x[0] in ('and', 'or', 'xor'):
        return any(has_quant(a) for a in x[1])
    if x[0] in ('not', 'fact'):
        return has_quant(x[1])
    return False

def has_rel(x):
    if is_lit(x):
        return False
    if x[0] == 'rel':
        return True
    if x[0] == 'fact':
        return has_rel(x[1])
    return False

def valid_prop(arg, trans='lit'):
    rules, concl = normalize(translate_arg(arg, trans))
    if any(has_quant(r) or has_rel(r) for r in rules) or has_quant(concl) or has_rel(concl):
        return None
    acc = set()
    for r in rules:
        atoms_of(r, acc)
    atoms_of(concl, acc)
    al = sorted(acc)
    for bits in itertools.product([False, True], repeat=len(al)):
        v = dict(zip(al, bits))
        if all(ev(r, v) for r in rules) and not ev(concl, v):
            return False
    return True

def valid_quant(arg, k=4):
    """单称/全称/特称 混合的一元谓词论证，在 k 个个体的论域上找反例（存在含义：正项非空）。
    个案 case 当作论域里的一个具名个体（下标 0）。"""
    stmts = list(arg.get('rules', [])) + list(arg.get('facts', []))
    concl = arg['concl']
    case = arg.get('case')
    acc = set()
    for s in stmts:
        atoms_of(s, acc)
    atoms_of(concl, acc)
    if case:
        acc.discard(case)
    terms = sorted(acc)
    types = list(itertools.product([False, True], repeat=len(terms)))

    def mem(ind, lit):
        if case and atom(lit) == case:
            val = ind[1]
        else:
            val = ind[0][terms.index(atom(lit))]
        return (not val) if lit.startswith('~') else val

    def sat(ind, x):
        if is_lit(x):
            return mem(ind, x)
        h = x[0]
        if h == 'and':
            return all(sat(ind, a) for a in x[1])
        if h == 'or':
            return any(sat(ind, a) for a in x[1])
        if h == 'xor':
            return sum(1 for a in x[1] if sat(ind, a)) == 1
        raise ValueError('sat ' + h)

    def holds(st, dom):
        if is_lit(st):  # fact about the case individual
            return sat(dom[0], st) if case else None
        h = st[0]
        if h == 'imp':
            return all(sat(i, st[2]) for i in dom if all(sat(i, a) for a in st[1]))
        if h == 'some':
            return any(sat(i, st[1]) and sat(i, st[2]) for i in dom)
        if h == 'most':
            a = sum(1 for i in dom if sat(i, st[1]) and sat(i, st[2]))
            b = sum(1 for i in dom if sat(i, st[1]) and not sat(i, st[2]))
            return a > b
        if h == 'not':
            return not holds(st[1], dom)
        if h in ('and', 'or', 'xor'):
            return sat(dom[0], st)
        raise ValueError(h)

    for ts in itertools.product(types, repeat=k):
        dom = [(t, j == 0) for j, t in enumerate(ts)]
        if not all(any(t[j] for t in ts) for j in range(len(terms))):
            continue
        if all(holds(s, dom) for s in stmts) and not holds(concl, dom):
            return False
    return True

def valid_rel(arg):
    rs = [r for r in arg.get('rules', []) if isinstance(r, tuple) and r[0] == 'rel']
    c = arg['concl']
    if not (isinstance(c, tuple) and c[0] == 'rel'):
        return None
    kinds = {r[1] for r in rs}
    if kinds != {'T'} or c[1] != 'T':
        return False
    edges = {(r[2], r[3]) for r in rs}
    changed = True
    while changed:
        changed = False
        for (a, b) in list(edges):
            for (c2, d) in list(edges):
                if b == c2 and (a, d) not in edges:
                    edges.add((a, d)); changed = True
    return (c[2], c[3]) in edges

def validity(arg, trans='lit'):
    allst = list(arg.get('rules', [])) + list(arg.get('facts', [])) + [arg['concl']]
    if any(has_rel(s) for s in allst):
        return valid_rel(arg)
    if any(has_quant(s) for s in allst):
        return valid_quant(arg)
    return valid_prop(arg, trans)

# ---------------------------------------------------------------- question check
def check_question(name, stem, options, answer, verbose=True):
    """options: {letter: arg or None(不可翻译/非形式)}；answer: 正确字母。
    返回错误列表；空列表表示：正确项在两个 loose 视角下与题干同构，其余三项在四个视角下都不同构。"""
    errs = []
    lines = []
    s_sig = {v: signature(stem, *v) for v in VIEWS}
    lines.append(f'[{name}] stem lit/loose: {s_sig[VIEWS[0]]}   valid={validity(stem)}')
    if s_sig[VIEWS[0]] != s_sig[VIEWS[1]]:
        lines.append(f'      stem std/loose: {s_sig[VIEWS[1]]}')
    for L in sorted(options):
        opt = options[L]
        if opt is None:
            lines.append(f'   {L}: (非形式/无法翻译) -> 不同构')
            if L == answer:
                errs.append(f'{name}: answer {L} is not formalised')
            continue
        o_sig = {v: signature(opt, *v) for v in VIEWS}
        same = {v: (o_sig[v] == s_sig[v]) for v in VIEWS}
        tag = ''.join('1' if same[v] else '0' for v in VIEWS)
        lines.append(f'   {L}: {o_sig[VIEWS[0]]}   valid={validity(opt)}   same[lit/l,std/l,lit/s,std/s]={tag}')
        if L == answer:
            if not (same[VIEWS[0]] and same[VIEWS[1]]):
                errs.append(f'{name}: answer {L} not isomorphic to stem in loose views ({tag})')
        else:
            if any(same.values()):
                errs.append(f'{name}: distractor {L} isomorphic to stem in some view ({tag})')
    if verbose:
        print('\n'.join(lines))
        print('   ->', 'OK' if not errs else errs)
    return errs
