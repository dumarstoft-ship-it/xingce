import json, re
OUT = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_B1.json'
inp = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/B1.json'))
d = json.load(open(OUT, encoding='utf-8'))
ok = True
assert [m['mat'] for m in d] == [m['mat'] for m in inp], 'mat order mismatch'
def visible(s):
    t = re.sub(r'\\(frac|times|approx|div|text|left|right)', '', s)
    t = t.replace('\\%', '%').replace('$', '').replace('{', '').replace('}', '')
    return t
for m in d:
    if len(m['q']) != 5: ok = False; print('count err', m['mat'])
    for q in m['q']:
        a = q['answer']; j = q['jiexi']
        errs = []
        if a not in 'ABCD' or len(a) != 1: errs.append('answer')
        mm = re.search(r'故正确答案为([A-D])。$', j)
        if not mm or mm.group(1) != a: errs.append('ending')
        if q['confidence'] not in ('high', 'medium', 'low'): errs.append('conf')
        if q['confidence'] == 'low' and not q['problem']: errs.append('low w/o problem')
        for fld in ('jiexi', 'problem'):
            if any(ord(c) < 32 for c in q[fld]): errs.append('ctrl char in ' + fld)
        if j.count('$') % 2: errs.append('odd $')
        # CJK inside math?
        for seg in re.findall(r'\$([^$]*)\$', j):
            if re.search(r'[一-鿿]', seg): errs.append('CJK in math: ' + seg)
            if re.search(r'(?<!\\)%', seg): errs.append('unescaped % in math: ' + seg)
            if seg.count('{') != seg.count('}'): errs.append('brace mismatch: ' + seg)
        for bad in ['根据我的计算', '程序算得', '程序', 'Python', '计算机']:
            if bad in j: errs.append('forbidden word ' + bad)
        vl = len(visible(j))
        comp = ('综合分析' in j[:12])
        lim = 350 if comp else 250
        flag = '' if 80 <= vl <= lim else f' <-- length out of range (limit {lim})'
        print(m['mat'], q['n'], a, q['confidence'], 'raw', len(j), 'visible', vl, flag, errs if errs else '')
        if errs: ok = False
print('ALL OK' if ok else 'ERRORS')
