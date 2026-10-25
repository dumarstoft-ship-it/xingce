# 汇总 entries_a/b/c，按规定字段顺序写出 bank_B5.json
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from entries_a import E as EA
from entries_b import E as EB
from entries_c import E as EC

VERIFY_DIR = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/verify'
KEYS = ['tid', 'keep', 'db_match', 'module', 'kaofa', 'method', 'source', 'stem', 'options', 'options_added',
        'answer', 'jiexi', 'learn', 'level', 'figure', 'verify', 'issues']
out = []
for e in EA + EB + EC:
    keep = e.get('keep', True)
    if keep:
        rec = {'tid': e['tid'], 'keep': True, 'db_match': e.get('db_match'), 'module': e['module'],
               'kaofa': e['kaofa'], 'method': e['method'], 'source': e.get('source', ''), 'stem': e['stem'],
               'options': e['options'], 'options_added': e.get('options_added', False), 'answer': e['answer'],
               'jiexi': e['jiexi'], 'learn': e['learn'], 'level': e['level'], 'figure': e.get('figure'),
               'verify': f"{VERIFY_DIR}/teacher_{e['tid']}.py", 'issues': e.get('issues', '')}
    else:
        rec = {'tid': e['tid'], 'keep': False, 'db_match': None, 'module': None, 'kaofa': '', 'method': '',
               'source': e.get('source', ''), 'stem': '', 'options': {}, 'options_added': False, 'answer': None,
               'jiexi': '', 'learn': '', 'level': None, 'figure': None, 'verify': None, 'issues': e.get('issues', '')}
    out.append({k: rec[k] for k in KEYS})
json.dump(out, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('wrote', len(out), 'entries')
