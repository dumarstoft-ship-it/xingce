import json
import re

OUT = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_B0.json'
INP = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/B0.json'
data = json.load(open(OUT, encoding='utf-8'))
inp = json.load(open(INP, encoding='utf-8'))
ok = True
assert [d['mat'] for d in data] == [d['mat'] for d in inp], 'mat order mismatch'
for d in data:
    qs = d['q']
    if len(qs) != 5 or [q['n'] for q in qs] != [1, 2, 3, 4, 5]:
        print('BAD count', d['mat']); ok = False
    for q in qs:
        a = q['answer']
        if a not in 'ABCD' or len(a) != 1:
            print('BAD answer', d['mat'], q['n']); ok = False
        m = re.search(r'故正确答案为([A-D])。$', q['jiexi'])
        if not m or m.group(1) != a:
            print('BAD ending', d['mat'], q['n']); ok = False
        if q['confidence'] not in ('high', 'medium', 'low'):
            print('BAD conf', d['mat'], q['n']); ok = False
        for bad in ('根据我的计算', '程序', '计算得出', 'Python'):
            if bad in q['jiexi']:
                print('BAD word', bad, d['mat'], q['n']); ok = False
        if q['jiexi'].count('$') % 2:
            print('odd $', d['mat'], q['n']); ok = False
        vis = re.sub(r'\\(frac|times|approx|left|right)', '', q['jiexi'])
        vis = re.sub(r'[{}$\\^]', '', vis)
        print(d['mat'], q['n'], a, q['confidence'], 'len raw', len(q['jiexi']), 'visible~', len(vis), ('PROBLEM: ' + q['problem']) if q['problem'] else '')
print('ALL OK' if ok else 'ERRORS')
print('materials', len(data))
