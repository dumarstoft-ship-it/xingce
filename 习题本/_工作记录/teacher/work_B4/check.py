import json, subprocess, collections, os, re
SP = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
bank = json.load(open(SP + '/teacher/bank_B4.json', encoding='utf-8'))
ex = json.load(open(SP + '/teacher/examples.json', encoding='utf-8'))
want = sorted(e['tid'] for e in ex if 'T124' <= e['tid'] <= 'T175')
got = [e['tid'] for e in bank]
assert got == want, (set(want) ^ set(got))
assert len(set(got)) == len(got)
KEYS = ['tid', 'keep', 'db_match', 'module', 'kaofa', 'method', 'source', 'stem', 'options', 'options_added',
        'answer', 'jiexi', 'learn', 'level', 'figure', 'verify', 'issues']
db = {x['id'] for x in json.load(open(SP + '/db/real_raw.json', encoding='utf-8'))}
errs = []
for e in bank:
    if list(e.keys()) != KEYS:
        errs.append((e['tid'], 'keys', list(e.keys())))
    if e['db_match'] is not None and e['db_match'] not in db:
        errs.append((e['tid'], 'db_match not in bank', e['db_match']))
    if not e['keep']:
        continue
    o = e['options']
    if not (isinstance(o, dict) and sorted(o) == ['A', 'B', 'C', 'D'] and all(str(v).strip() for v in o.values())):
        errs.append((e['tid'], 'options', o))
    if len(set(o.values())) != 4:
        errs.append((e['tid'], 'duplicate options'))
    if e['answer'] not in 'ABCD' or len(e['answer']) != 1:
        errs.append((e['tid'], 'answer', e['answer']))
    if not re.fullmatch(r'M(0[1-9]|1[0-4])', e['module'] or ''):
        errs.append((e['tid'], 'module', e['module']))
    if e['level'] not in ('基础', '中等', '难', '很难'):
        errs.append((e['tid'], 'level', e['level']))
    if len(e['jiexi']) > 300 or len(e['kaofa']) > 20 or len(e['method']) > 20:
        errs.append((e['tid'], 'length'))
    if '参考用时' in e['jiexi'] or '樱有尽有' in e['stem'] or '公众号' in e['stem']:
        errs.append((e['tid'], 'forbidden text'))
    f = e['figure']
    if f is not None and not (f['type'] == 'svg' and f['svg'].startswith('<svg') or f['type'] == 'crop_needed'):
        errs.append((e['tid'], 'figure'))
    vp = e['verify']
    if not os.path.isfile(vp):
        errs.append((e['tid'], 'verify missing'))
        continue
    r = subprocess.run(['python3', '-I', vp], capture_output=True, text=True, timeout=120)
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ''
    if r.returncode != 0 or last != e['answer']:
        errs.append((e['tid'], 'verify', r.returncode, last, e['answer'], r.stderr[-300:]))
keep = [e for e in bank if e['keep']]
print('total', len(bank), 'keep', len(keep), 'drop', len(bank) - len(keep), [e['tid'] for e in bank if not e['keep']])
print('modules', sorted(collections.Counter(e['module'] for e in keep).items()))
print('levels', collections.Counter(e['level'] for e in keep))
print('answers', sorted(collections.Counter(e['answer'] for e in keep).items()))
print('db_match', sum(1 for e in keep if e['db_match']), '| options_added', [e['tid'] for e in keep if e['options_added']])
print('figures', [(e['tid'], e['figure']['type']) for e in keep if e['figure']])
print('ERRORS', errs if errs else 'none')
