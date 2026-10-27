import json, re
OUT = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_A8.json'
TASK = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/A8.json'
data = json.load(open(OUT, encoding='utf-8'))
task = json.load(open(TASK, encoding='utf-8'))
assert [d['mat'] for d in data] == [t['mat'] for t in task], 'mat order mismatch'
ok = True
def visible_len(s):
    # approximate printed length: drop latex commands/braces/$
    t = re.sub(r'\\(frac|times|approx|text|div|le|ge)', '', s)
    t = re.sub(r'[\\${}]', '', t)
    t = t.replace('\n', '')
    return len(t)
for d in data:
    qs = d['q']
    if len(qs) != 5 or [x['n'] for x in qs] != [1, 2, 3, 4, 5]:
        ok = False; print('bad count', d['mat'])
    for x in qs:
        a = x['answer']; j = x['jiexi']
        if a not in 'ABCD' or len(a) != 1:
            ok = False; print('bad answer', d['mat'], x['n'])
        if not j.endswith('故正确答案为%s。' % a):
            ok = False; print('bad ending', d['mat'], x['n'])
        m = re.findall(r'故正确答案为([A-D])。', j)
        if m != [a]:
            ok = False; print('ending count/letter issue', d['mat'], x['n'], m)
        if j.count('$') % 2:
            ok = False; print('unbalanced $', d['mat'], x['n'])
        if x['confidence'] not in ('high', 'low'):
            ok = False; print('conf', d['mat'], x['n'], x['confidence'])
        for bad in ['程序', '根据我的计算', 'Python', '计算机']:
            if bad in j:
                ok = False; print('forbidden word', bad, d['mat'], x['n'])
        L = visible_len(j)
        comp = j.startswith('本题考查综合分析')
        lim = 350 if comp else 250
        flag = '' if 80 <= L <= lim else '  <-- LENGTH'
        print(d['mat'], x['n'], a, x['confidence'], 'len~', L, 'raw', len(j), flag)
print('ALL OK' if ok else 'PROBLEMS FOUND')
print('answers:', {d['mat']: ''.join(x['answer'] for x in d['q']) for d in data})
print('low:', [(d['mat'], x['n']) for d in data for x in d['q'] if x['confidence'] == 'low'])
