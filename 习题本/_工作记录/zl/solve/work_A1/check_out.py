import json, re
OUT = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_A1.json'
INP = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/A1.json'
data = json.load(open(OUT, encoding='utf-8'))
inp = json.load(open(INP, encoding='utf-8'))
ok = True
assert [d['mat'] for d in data] == [d['mat'] for d in inp], 'mat order mismatch'
cjk = re.compile(r'[一-鿿（）、，。]')
for d in data:
    qs = d['q']
    if len(qs) != 5 or [q['n'] for q in qs] != [1, 2, 3, 4, 5]:
        print('BAD count', d['mat']); ok = False
    for q in qs:
        a = q['answer']; jx = q['jiexi']
        if a not in 'ABCD' or len(a) != 1:
            print('BAD answer', d['mat'], q['n']); ok = False
        m = re.search(r'故正确答案为([A-D])。$', jx)
        if not m or m.group(1) != a:
            print('BAD ending', d['mat'], q['n']); ok = False
        if jx.count('$') % 2:
            print('BAD $ count', d['mat'], q['n']); ok = False
        maths = re.findall(r'\$(.+?)\$', jx)
        for mm in maths:
            if cjk.search(mm):
                print('CJK in math', d['mat'], q['n'], mm); ok = False
        if any(ord(c) < 32 for c in jx):
            print('control char', d['mat'], q['n']); ok = False
        for bad in ['根据我的计算', '程序算得', '程序', '我的计算', 'Python']:
            if bad in jx:
                print('forbidden phrase', bad, d['mat'], q['n']); ok = False
        if q['confidence'] not in ('high', 'medium', 'low'):
            print('BAD confidence', d['mat'], q['n']); ok = False
        # length: raw and approx displayed (strip latex commands)
        disp = re.sub(r'\\frac', '', jx)
        disp = re.sub(r'\\(approx|times|div|text)', 'x', disp)
        disp = disp.replace('\\%', '%').replace('$', '').replace('{', '').replace('}', '')
        print('%s Q%d ans=%s conf=%s raw=%d disp~%d %s' % (d['mat'], q['n'], a, q['confidence'], len(jx), len(disp),
                                                       ('problem: ' + q['problem']) if q['problem'] else ''))
print('ALL OK' if ok else 'ERRORS FOUND', '| materials:', len(data))
