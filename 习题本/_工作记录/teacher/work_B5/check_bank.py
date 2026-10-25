# 按任务要求检查 bank_B5.json：JSON可读、tid齐全、选项与答案、验算脚本输出一致，以及若干格式约束
import json, os, re, subprocess, sys, collections
bank_path, ex_path, db_path = sys.argv[1:4]
bank = json.load(open(bank_path))
ex = json.load(open(ex_path))
db_ids = {x['id'] for x in json.load(open(db_path))}
want = [x['tid'] for x in ex if 'T176' <= x['tid'] <= 'T227']
have = [b['tid'] for b in bank]
errs = []
missing = [t for t in want if t not in have]
extra = [t for t in have if t not in want]
dups = [t for t, c in collections.Counter(have).items() if c > 1]
if missing: errs.append(f'missing tids {missing}')
if dups: errs.append(f'duplicate tids {dups}')
KEYS = ['tid', 'keep', 'db_match', 'module', 'kaofa', 'method', 'source', 'stem', 'options', 'options_added',
        'answer', 'jiexi', 'learn', 'level', 'figure', 'verify', 'issues']
WATERMARK = ['公众号', '樱有尽有', '参考用时']
NOTE = ['做题方法', '中间计算', '统计模型', '集合构造', '得票必胜', '取物必胜', '排队问题', '余数理论', '报数问题', '老师']
mods = collections.Counter()
for b in bank:
    t = b['tid']
    if list(b.keys()) != KEYS: errs.append(f'{t}: key order/set {list(b.keys())}')
    if not b['keep']:
        continue
    mods[b['module']] += 1
    if not re.fullmatch(r'M(0[1-9]|1[0-4])', b['module'] or ''): errs.append(f'{t}: module {b["module"]}')
    if sorted(b['options']) != ['A', 'B', 'C', 'D'] or not all(str(v).strip() for v in b['options'].values()):
        errs.append(f'{t}: options {b["options"]}')
    if b['answer'] not in 'ABCD' or len(b['answer']) != 1: errs.append(f'{t}: answer {b["answer"]}')
    if len(set(b['options'].values())) != 4: errs.append(f'{t}: duplicate option text')
    if len(b['kaofa']) > 20 or len(b['method']) > 20: errs.append(f'{t}: kaofa/method too long')
    if len(b['jiexi']) > 300: errs.append(f'{t}: jiexi {len(b["jiexi"])} chars')
    if b['level'] not in ('基础', '中等', '难', '很难'): errs.append(f'{t}: level {b["level"]}')
    if b['db_match'] is not None and b['db_match'] not in db_ids: errs.append(f'{t}: db_match {b["db_match"]} not in db')
    if not isinstance(b['options_added'], bool): errs.append(f'{t}: options_added not bool')
    q = b['stem'] + ''.join(b['options'].values())
    for w in WATERMARK:
        if w in q + b['jiexi'] + b['learn']: errs.append(f'{t}: contains watermark {w}')
    for w in NOTE:
        if w in q: errs.append(f'{t}: stem/options contain note word {w}')
    if b['stem'].count('$') % 2 or b['jiexi'].count('$') % 2: errs.append(f'{t}: unbalanced $')
    f = b['figure']
    if f is not None:
        if f.get('type') == 'svg':
            s = f.get('svg', '')
            if not (s.startswith('<svg') and s.endswith('</svg>')): errs.append(f'{t}: bad svg')
        elif f.get('type') != 'crop_needed':
            errs.append(f'{t}: bad figure type')
    v = b['verify']
    if not v or not os.path.exists(v):
        errs.append(f'{t}: verify missing {v}')
        continue
    r = subprocess.run([sys.executable, v], capture_output=True, text=True, timeout=600)
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ''
    if r.returncode != 0 or last != b['answer']:
        errs.append(f'{t}: verify rc={r.returncode} out={last!r} ans={b["answer"]} err={r.stderr[-200:]}')
keep = [b for b in bank if b['keep']]
print('entries', len(bank), 'keep', len(keep), 'drop', len(bank) - len(keep), 'extra tids', extra)
print('modules', dict(sorted(mods.items())))
print('levels', dict(collections.Counter(b['level'] for b in keep)))
print('answers', dict(sorted(collections.Counter(b['answer'] for b in keep).items())))
print('ERRORS' if errs else 'ALL CHECKS PASSED')
for e in errs: print(' -', e)
