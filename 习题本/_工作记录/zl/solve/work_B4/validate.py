import json, re
OUT = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_B4.json'
IN = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/B4.json'
d = json.load(open(OUT, encoding='utf-8')); inp = json.load(open(IN, encoding='utf-8'))
assert [m['mat'] for m in d] == [m['mat'] for m in inp], 'mat order mismatch'
ok = True
for m in d:
    assert len(m['q']) == 5, m['mat']
    assert [x['n'] for x in m['q']] == [1,2,3,4,5]
    for x in m['q']:
        a = x['answer']; j = x['jiexi']
        if a not in 'ABCD' or len(a) != 1: print('BAD answer', m['mat'], x['n']); ok = False
        if not j.endswith('故正确答案为%s。' % a): print('BAD ending', m['mat'], x['n']); ok = False
        if j.count('故正确答案为') != 1: print('multiple endings', m['mat'], x['n']); ok = False
        if x['confidence'] not in ('high','medium','low'): print('BAD conf'); ok = False
        if j.count('$') % 2: print('odd $', m['mat'], x['n']); ok = False
        maths = re.findall(r'\$(.+?)\$', j)
        for s in maths:
            if re.search(r'(?<!\\)%', s): print('unescaped % in math', m['mat'], x['n'], s); ok = False
            if re.search(r'[\u2212\u00d7\u00f7]', s): print('unicode op in math', m['mat'], x['n'], s); ok = False
            if re.search(r'[\u4e00-\u9fff]', re.sub(r'\\text\{[^}]*\}', '', s)): print('CJK outside \\text in math', m['mat'], x['n'], s); ok = False
        for bad in ['根据我的计算', '程序', '计算得出', 'Python', '代码']:
            if bad in j: print('forbidden phrase', bad, m['mat'], x['n']); ok = False
        # displayed length approx: strip latex commands
        disp = re.sub(r'\$(.+?)\$', lambda mm: re.sub(r'\\(frac|times|approx|left|right|text|div)', '', mm.group(1)).replace('{','').replace('}','').replace('\\',''), j)
        comp = x['n'] == 5 and ('综合分析' in j)
        lim = 350 if comp else 250
        flag = '' if 80 <= len(disp) <= lim else '  <-- LENGTH'
        print(m['mat'], x['n'], a, x['confidence'], 'raw', len(j), 'disp', len(disp), 'lim', lim, flag)
print('ALL OK' if ok else 'PROBLEMS FOUND')
print('summary', len(d), 'materials;', sum(len(m['q']) for m in d), 'questions')
print('answers', {m['mat']: ''.join(x['answer'] for x in m['q']) for m in d})
