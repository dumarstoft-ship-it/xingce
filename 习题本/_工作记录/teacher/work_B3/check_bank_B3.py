# 按任务要求自检 bank_B3.json
import json, subprocess, sys, os, collections
SP = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
bank = json.load(open(os.path.join(SP, 'teacher', 'bank_B3.json'), encoding='utf-8'))
ex = {x['tid']: x for x in json.load(open(os.path.join(SP, 'teacher', 'examples.json'), encoding='utf-8'))}
db = {x['id'] for x in json.load(open(os.path.join(SP, 'db', 'real_raw.json'), encoding='utf-8'))}
want = ['T%03d' % i for i in range(82, 124)]
errs = []
tids = [e['tid'] for e in bank]
if tids != want:
    errs.append('tid list mismatch: missing %s extra %s' % (sorted(set(want) - set(tids)), sorted(set(tids) - set(want))))
FIELDS = ['tid', 'keep', 'db_match', 'module', 'kaofa', 'method', 'source', 'stem', 'options', 'options_added',
          'answer', 'jiexi', 'learn', 'level', 'figure', 'verify', 'issues']
mods = {'M%02d' % i for i in range(1, 15)}
for e in bank:
    t = e['tid']
    if sorted(e) != sorted(FIELDS):
        errs.append(t + ' fields ' + str(sorted(set(FIELDS) ^ set(e))))
    if e['db_match'] is not None and e['db_match'] not in db:
        errs.append(t + ' db_match not in db')
    if not e['keep']:
        if not e['issues']:
            errs.append(t + ' dropped without reason')
        continue
    o = e['options']
    if not isinstance(o, dict) or sorted(o) != ['A', 'B', 'C', 'D'] or not all(str(v).strip() for v in o.values()):
        errs.append(t + ' options incomplete')
    if len(set(o.values())) != 4:
        errs.append(t + ' duplicate options')
    if e['answer'] not in ('A', 'B', 'C', 'D'):
        errs.append(t + ' bad answer')
    if e['module'] not in mods:
        errs.append(t + ' bad module')
    if e['level'] not in ('基础', '中等', '难', '很难'):
        errs.append(t + ' bad level')
    for fld, lim in (('kaofa', 20), ('method', 20), ('jiexi', 300)):
        if not e[fld] or len(e[fld]) > lim:
            errs.append('%s %s length %d' % (t, fld, len(e[fld])))
    if not e['stem'] or not e['learn']:
        errs.append(t + ' empty stem/learn')
    if e['figure'] is not None and e['figure'].get('type') not in ('svg', 'crop_needed'):
        errs.append(t + ' bad figure type')
    # 原题有选项的，选项文字应与截图一致（这里用提取文本粗查答案选项的数字）
    if ex[t]['has_options'] and e['options_added']:
        errs.append(t + ' options_added but original has options')
    v = e['verify']
    if not v or not os.path.isfile(v):
        errs.append(t + ' verify script missing')
        continue
    r = subprocess.run([sys.executable, '-I', v], capture_output=True, text=True, timeout=300)
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ''
    if r.returncode != 0 or last != e['answer']:
        errs.append('%s verify rc=%d last=%r answer=%s %s' % (t, r.returncode, last, e['answer'], r.stderr[-300:]))
kept = [e for e in bank if e['keep']]
print('entries', len(bank), 'kept', len(kept), 'dropped', len(bank) - len(kept))
print('modules', dict(sorted(collections.Counter(e['module'] for e in kept).items())))
print('levels', dict(collections.Counter(e['level'] for e in kept)))
print('answers', dict(sorted(collections.Counter(e['answer'] for e in kept).items())))
print('db_match', {e['tid']: e['db_match'] for e in bank if e['db_match']})
print('ERRORS:', errs if errs else 'none')
