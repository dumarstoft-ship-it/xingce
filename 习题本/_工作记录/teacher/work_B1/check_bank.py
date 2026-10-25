# 检查 teacher/bank_B1.json：JSON 可读、tid 齐全、选项/答案合法、验算脚本输出与答案一致，以及字段约束
import json, re, subprocess, sys
import xml.etree.ElementTree as ET

BASE = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
data = json.load(open(BASE + '/teacher/bank_B1.json', encoding='utf-8'))
ex = {x['tid']: x for x in json.load(open(BASE + '/teacher/examples.json', encoding='utf-8'))}

want = ['T%03d' % i for i in range(1, 38)]
got = [x['tid'] for x in data]
assert got == want, (set(want) ^ set(got))
KEYS = ['tid', 'keep', 'db_match', 'module', 'kaofa', 'method', 'source', 'stem', 'options', 'options_added',
        'answer', 'jiexi', 'learn', 'level', 'figure', 'verify', 'issues']
MODULES = {'M%02d' % i for i in range(1, 15)}
LEVELS = {'基础', '中等', '难', '很难'}
BAD = ['公众号', '樱有尽有', '参考用时']

def shown_len(s):
    """去掉 $ 与常见 LaTeX 命令后的显示长度（近似）"""
    s = re.sub(r'\\(frac|dfrac)\{([^}]*)\}\{([^}]*)\}', r'\2/\3', s)
    s = re.sub(r'\\[a-zA-Z]+', '', s)
    return len(s.replace('$', '').replace('{', '').replace('}', ''))

errors = []
for x in data:
    t = x['tid']
    if list(x.keys()) != KEYS:
        errors.append((t, 'keys', list(x.keys())))
    if not x['keep']:
        continue
    o = x['options']
    if sorted(o) != ['A', 'B', 'C', 'D'] or any(not str(v).strip() for v in o.values()):
        errors.append((t, 'options', o))
    if len(set(o.values())) != 4:
        errors.append((t, 'duplicate options'))
    if x['answer'] not in 'ABCD' or len(x['answer']) != 1:
        errors.append((t, 'answer', x['answer']))
    if x['module'] not in MODULES:
        errors.append((t, 'module', x['module']))
    if x['level'] not in LEVELS:
        errors.append((t, 'level', x['level']))
    for f in ('kaofa', 'method'):
        if not x[f] or len(x[f]) > 20:
            errors.append((t, f, len(x[f])))
    if shown_len(x['jiexi']) > 300:
        errors.append((t, 'jiexi too long', shown_len(x['jiexi'])))
    blob = x['stem'] + json.dumps(o, ensure_ascii=False) + x['jiexi'] + x['learn']
    for b in BAD:
        if b in blob:
            errors.append((t, 'bad word', b))
    if re.match(r'^\s*[（(]\s*\d{4}', x['stem']):
        errors.append((t, 'source prefix left in stem'))
    if x['stem'].count('$') % 2 or x['jiexi'].count('$') % 2:
        errors.append((t, 'unbalanced $'))
    fig = x['figure']
    if fig is not None:
        if fig.get('type') == 'svg':
            root = ET.fromstring(fig['svg'])
            texts = [el.text or '' for el in root.iter() if el.tag.endswith('text')]
            if any(re.search(r'\d', s) for s in texts):
                errors.append((t, 'figure has digits (answer leak?)', texts))
        elif fig.get('type') != 'crop_needed':
            errors.append((t, 'figure type', fig.get('type')))
    if x['db_match'] is not None and x['db_match'] != ex[t]['db_match']:
        print('note: db_match changed', t, ex[t]['db_match'], '->', x['db_match'])
    # 验算脚本
    r = subprocess.run([sys.executable, '-I', x['verify']], capture_output=True, text=True, timeout=300)
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ''
    if r.returncode != 0 or last != x['answer']:
        errors.append((t, 'verify', r.returncode, last, x['answer'], r.stderr[-300:]))

for x in data:
    if ex[x['tid']]['db_match'] != x['db_match']:
        print('db_match differs from program:', x['tid'], ex[x['tid']]['db_match'], '->', x['db_match'])

keep = [x for x in data if x['keep']]
from collections import Counter
print('keep', len(keep), 'drop', len(data) - len(keep))
print('answers', sorted(Counter(x['answer'] for x in keep).items()))
print('modules', sorted(Counter(x['module'] for x in keep).items()))
print('levels', sorted(Counter(x['level'] for x in keep).items()))
print('options_added', sum(x['options_added'] for x in keep))
print('max jiexi len', max((shown_len(x['jiexi']), x['tid']) for x in keep))
print('ERRORS:', len(errors))
for e in errors:
    print('  ', e)
sys.exit(1 if errors else 0)
