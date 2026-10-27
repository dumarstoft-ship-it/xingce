import json, re, sys
p = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_B6.json'
inp = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/B6.json', encoding='utf-8'))
d = json.load(open(p, encoding='utf-8'))
ok = True
assert [m['mat'] for m in d] == [m['mat'] for m in inp], 'mat order mismatch'
for m in d:
    if len(m['q']) != 5:
        ok = False; print('count', m['mat'], len(m['q']))
    if [q['n'] for q in m['q']] != [1, 2, 3, 4, 5]:
        ok = False; print('numbering', m['mat'])
    for q in m['q']:
        j = q['jiexi']
        if q['answer'] not in 'ABCD' or len(q['answer']) != 1:
            ok = False; print('answer', m['mat'], q['n'])
        mm = re.search(r'故正确答案为([A-D])。$', j)
        if not mm or mm.group(1) != q['answer']:
            ok = False; print('ending', m['mat'], q['n'])
        if j.count('$') % 2:
            ok = False; print('unbalanced $', m['mat'], q['n'])
        if any(ord(c) < 32 for c in j):
            ok = False; print('control char', m['mat'], q['n'])
        if q['confidence'] not in ('high', 'medium', 'low'):
            ok = False; print('confidence', m['mat'], q['n'])
        for bad in ('我的计算', '程序', '算得', 'Python'):
            if bad in j:
                ok = False; print('forbidden', bad, m['mat'], q['n'])
        if not j.startswith('本题考查'):
            print('note: does not start with 本题考查', m['mat'], q['n'])
        # math segments should not contain bare %
        for seg in re.findall(r'\$(.*?)\$', j):
            if re.search(r'(?<!\\)%', seg):
                ok = False; print('unescaped % in math', m['mat'], q['n'], seg)
print('OK' if ok else 'FAIL', len(d), 'materials')
for m in d:
    print(m['mat'], ''.join(q['answer'] for q in m['q']), [q['confidence'] for q in m['q']])
