import json, re

OUT = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_A4.json'
INP = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/A4.json'
data = json.load(open(OUT, encoding='utf-8'))
inp = json.load(open(INP, encoding='utf-8'))
errs = []
if [d['mat'] for d in data] != [d['mat'] for d in inp]:
    errs.append('mat list mismatch')
comp_kw = ('综合分析',)
for d in data:
    qs = d['q']
    if len(qs) != 5:
        errs.append('%s: %d questions' % (d['mat'], len(qs)))
    if [x['n'] for x in qs] != [1, 2, 3, 4, 5]:
        errs.append('%s: numbering' % d['mat'])
    for x in qs:
        tag = '%s Q%d' % (d['mat'], x['n'])
        a = x['answer']
        if a not in ('A', 'B', 'C', 'D'):
            errs.append(tag + ' bad answer')
        jx = x['jiexi']
        m = re.search(r'故正确答案为([A-D])。$', jx)
        if not m:
            errs.append(tag + ' bad ending')
        elif m.group(1) != a:
            errs.append(tag + ' ending/answer mismatch')
        if jx.count('故正确答案为') != 1:
            errs.append(tag + ' multiple endings')
        if jx.count('$') % 2:
            errs.append(tag + ' unbalanced $')
        for seg in re.findall(r'\$(.*?)\$', jx):
            if re.search(r'(?<!\\)%', seg):
                errs.append(tag + ' unescaped % in math: ' + seg)
            if re.search(r'[\u4e00-\u9fff]', re.sub(r'\\text\{[^}]*\}', '', seg)):
                errs.append(tag + ' CJK outside \\text in math: ' + seg)
            if re.search(r'[×≈÷]', seg):
                errs.append(tag + ' unicode op in math: ' + seg)
        for bad in ('根据我的计算', '程序算得', '程序', '我的计算'):
            if bad in jx:
                errs.append(tag + ' forbidden phrase ' + bad)
        if x['confidence'] not in ('high', 'medium', 'low'):
            errs.append(tag + ' bad confidence')
        # visible length: strip latex commands roughly
        vis = re.sub(r'\\(frac|times|approx|text|div|left|right)', '', jx)
        vis = re.sub(r'[\$\{\}\\^]', '', vis)
        limit = 350 if jx.startswith('本题考查综合分析') else 250
        print('%-16s ans=%s conf=%-6s len=%d (raw %d)%s' % (tag, a, x['confidence'], len(vis), len(jx),
              '  <-- over %d' % limit if len(vis) > limit else ''))
print('ERRORS:' if errs else 'ALL CHECKS PASSED', *errs, sep='\n')
print('answers:', {d['mat']: ''.join(x['answer'] for x in d['q']) for d in data})
print('low:', [(d['mat'], x['n']) for d in data for x in d['q'] if x['confidence'] == 'low'])
