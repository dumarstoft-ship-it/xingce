import json, sys
d = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/tasks_in/L03.json'))
R = {r['id']: r for r in d['real']}
n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 900
ids = [a for a in sys.argv[1:] if not a.isdigit()]
for i in ids:
    r = R[i]
    print('=' * 20, i, r['paper'], 'diff', r['difficulty'], 'ans', r['answer_official'], '|', r['kaofa'], '|', r['note'])
    print(r['text'])
    if r.get('stem_text'): print('[STEM]', r['stem_text'])
    j = r.get('jiexi_excerpt') or ''
    print('[JX]', j[:n].replace('\n', ' '))
