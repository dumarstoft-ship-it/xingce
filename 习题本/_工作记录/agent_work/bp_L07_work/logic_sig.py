"""L07 结构相似 formal checker.

Exam convention used here (与粉笔/华图解析一致):
  * 翻译统一用标准方向：如果A就B / A必须B / 所有A是B -> A>B；
    只有A才B / 除非A否则不B / 不A就不B / 没有A就没有B / B离不开A / A是B的必要条件 -> B>A。
  * 个案（某人/某地/该企业/历史……）当作 case：'case>X' 型前提折成事实 X，结论 'case>Y' 折成 Y。
  * 事实全部并入结论前件：rules |- (facts & ant) > cons   （演绎定理，保证"规则+事实"与"规则 |- 条件句"可比）。
  * 结构签名 = 在"原子改名 + 单个原子整体取反"下的最小表示；前提视为集合（顺序无关）。
  * 量词：有的/许多/多数/部分 统一记 some（签名用），most 只在有效性检验里区分。

Literal: 'A' or '~A'.  Statements:
  ('imp', [lits], cons)   cons = lit | ('or',[lits]) | ('and',[lits])
  ('or', [lits])          disjunctive fact / rule without antecedent
  ('some', X, Y) ('most', X, Y)   quantified (terms may be literals)
Argument dict: rules, facts (list of lits or ('or',..)/('and',..)), concl (stmt or lit), case (atom or None)
"""
import itertools

def neg(l):
    return l[1:] if l.startswith('~') else '~' + l

def atom(l):
    return l.lstrip('~')

def atoms_of(x, acc):
    if isinstance(x, str):
        acc.add(atom(x)); return acc
    for y in x[1:]:
        if isinstance(y, list):
            for z in y: atoms_of(z, acc)
        else:
            atoms_of(y, acc)
    return acc

def normalize(arg):
    rules = [r for r in arg.get('rules', [])]
    facts = list(arg.get('facts', []))
    concl = arg['concl']
    case = arg.get('case')
    explicit = case is not None
    if case is None and not isinstance(concl, str) and concl[0] == 'imp' and len(concl[1]) == 1:
        case = concl[1][0]          # auto-case: subject of a categorical conclusion
    folded = False
    if case:
        keep = []
        for r in rules:
            if r[0] == 'imp' and r[1] == [case] and (explicit or isinstance(r[2], str)):
                facts.append(r[2]); folded = True
            else:
                keep.append(r)
        rules = keep
        if (explicit or folded) and not isinstance(concl, str) and concl[0] == 'imp' and case in concl[1]:
            ant = [x for x in concl[1] if x != case]
            concl = ('imp', ant, concl[2]) if ant else concl[2]
    if facts:
        flat = []
        for f in facts:
            if isinstance(f, str): flat.append(f)
            elif f[0] == 'and': flat.extend(f[1])
            else: flat.append(f)
        if isinstance(concl, str) or concl[0] in ('or', 'and'):
            concl = ('imp', flat, concl)
        elif concl[0] == 'imp':
            concl = ('imp', flat + list(concl[1]), concl[2])
        else:
            rules = rules + [('fact', f) for f in flat]
    return rules, concl

def unify_q(x):
    if isinstance(x, str): return x
    out = ['some' if x[0] == 'most' else x[0]]
    for y in x[1:]:
        out.append([unify_q(z) for z in y] if isinstance(y, list) else unify_q(y))
    return tuple(out)

def ren(x, m):
    """apply mapping m: atom -> (newatom, flip)."""
    if isinstance(x, str):
        a = atom(x); n, f = m[a]
        neg_ = x.startswith('~') ^ f
        return ('~' if neg_ else '') + n
    head = x[0]
    out = [head]
    for y in x[1:]:
        if isinstance(y, list):
            out.append(sorted(ren(z, m) if isinstance(z, str) else s(ren(z, m)) for z in y))
        else:
            out.append(ren(y, m))
    return tuple(out)

def s(x):
    if isinstance(x, str): return x
    parts = []
    for y in x[1:]:
        if isinstance(y, list): parts.append('[' + ','.join(sorted(s(z) for z in y)) + ']')
        else: parts.append(s(y))
    return x[0] + '(' + ';'.join(parts) + ')'

def signature(arg):
    rules, concl = normalize(arg)
    rules = [unify_q(r) for r in rules]; concl = unify_q(concl)
    acc = set()
    for r in rules: atoms_of(r, acc)
    atoms_of(concl, acc)
    al = sorted(acc)
    names = [chr(ord('P') + i) for i in range(len(al))]
    best = None
    for perm in itertools.permutations(names):
        for flips in itertools.product([False, True], repeat=len(al)):
            m = {a: (perm[i], flips[i]) for i, a in enumerate(al)}
            rs = sorted(s(ren(r, m)) for r in rules)
            c = s(ren(concl, m))
            rep = '{' + ' , '.join(rs) + '} |- ' + c
            if best is None or rep < best: best = rep
    return best

# ---------------- propositional validity (after normalization) ----------------
def ev(x, v):
    if isinstance(x, str):
        return (not v[atom(x)]) if x.startswith('~') else v[x]
    h = x[0]
    if h == 'imp':
        return (not all(ev(a, v) for a in x[1])) or ev(x[2], v)
    if h == 'or':
        return any(ev(a, v) for a in x[1])
    if h == 'and':
        return all(ev(a, v) for a in x[1])
    if h == 'fact':
        return ev(x[1], v)
    raise ValueError(h)

def valid_prop(arg):
    rules, concl = normalize(arg)
    acc = set()
    for r in rules: atoms_of(r, acc)
    atoms_of(concl, acc)
    al = sorted(acc)
    for bits in itertools.product([False, True], repeat=len(al)):
        v = dict(zip(al, bits))
        if all(ev(r, v) for r in rules) and not ev(concl, v):
            return False
    return True

# ---------------- quantified syllogism validity (domain brute force) ----------------
def valid_quant(arg, k=3):
    stmts = list(arg.get('rules', [])) + [arg['concl']]
    acc = set()
    for st in stmts: atoms_of(st, acc)
    terms = sorted(acc)
    types = list(itertools.product([False, True], repeat=len(terms)))
    def mem(ind, lit):
        val = ind[terms.index(atom(lit))]
        return (not val) if lit.startswith('~') else val
    def holds(st, dom):
        h = st[0]
        if h == 'imp':  # all X are Y (single-literal antecedent and consequent)
            X = st[1][0]; Y = st[2]
            return all(mem(i, Y) for i in dom if mem(i, X))
        if h == 'some':
            return any(mem(i, st[1]) and mem(i, st[2]) for i in dom)
        if h == 'most':
            a = sum(1 for i in dom if mem(i, st[1]) and mem(i, st[2]))
            b = sum(1 for i in dom if mem(i, st[1]) and not mem(i, st[2]))
            return a > b
        raise ValueError(h)
    for dom in itertools.product(types, repeat=k):
        # existential import: every positive term non-empty
        if not all(any(i[j] for i in dom) for j in range(len(terms))):
            continue
        if all(holds(st, dom) for st in arg['rules']) and not holds(arg['concl'], dom):
            return False
    return True

def check_question(name, stem, options, answer, verbose=True, quant=False):
    """Return list of errors. answer = letter whose signature must equal the stem's; all others must differ."""
    errs = []
    s0 = signature(stem)
    v0 = valid_quant(stem) if quant else valid_prop(stem)
    lines = [f'[{name}] stem: {s0}  valid={v0}']
    hits = []
    for L, opt in options.items():
        if opt is None:
            lines.append(f'   {L}: (informal / not formalizable) -> differs')
            continue
        q = opt.get('quant', quant)
        sg = signature(opt)
        vv = valid_quant(opt) if q else valid_prop(opt)
        same = (sg == s0)
        if same: hits.append(L)
        lines.append(f'   {L}: {sg}  valid={vv}  {"== STEM" if same else ""}')
    if hits != [answer]:
        errs.append(f'{name}: expected only {answer} to match stem, got {hits}')
    if verbose:
        print('\n'.join(lines))
        print('   ->', 'OK' if not errs else errs)
    return errs
