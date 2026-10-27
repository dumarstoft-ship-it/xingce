import json, re
p = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_B2.json'
d = json.load(open(p, encoding='utf-8'))
inp = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/B2.json', encoding='utf-8'))
ok = True
assert [m['mat'] for m in d] == [m['mat'] for m in inp], "mat order/ids mismatch"
for m in d:
    if len(m['q']) != 5 or [q['n'] for q in m['q']] != [1,2,3,4,5]:
        ok = False; print("bad count", m['mat'])
    for q in m['q']:
        if q['answer'] not in 'ABCD' or len(q['answer']) != 1:
            ok = False; print("bad answer", m['mat'], q['n'])
        mm = re.search(r'故正确答案为([A-D])。$', q['jiexi'])
        if not mm or mm.group(1) != q['answer']:
            ok = False; print("bad ending", m['mat'], q['n'])
        if q['confidence'] not in ('high','low'):
            ok = False; print("bad conf", m['mat'], q['n'])
        if q['jiexi'].count('$') % 2:
            ok = False; print("odd $", m['mat'], q['n'])
        for bad in ['根据我的计算','程序算得','程序','Python','python']:
            if bad in q['jiexi']:
                ok = False; print("forbidden phrase", bad, m['mat'], q['n'])
        # Chinese chars inside math outside \text{}
        for seg in re.findall(r'\$(.*?)\$', q['jiexi']):
            s2 = re.sub(r'\\text\{[^}]*\}', '', seg)
            if re.search(r'[\u4e00-\u9fff]', s2):
                print("CJK in math:", m['mat'], q['n'], seg)
            if re.search(r'(?<!\\)%', seg):
                ok = False; print("unescaped % in math", m['mat'], q['n'], seg)
print("materials", len(d), "ALL OK" if ok else "PROBLEMS")
for m in d:
    print(m['mat'], ''.join(q['answer'] for q in m['q']), [q['confidence'] for q in m['q'] if q['confidence']!='high'])
