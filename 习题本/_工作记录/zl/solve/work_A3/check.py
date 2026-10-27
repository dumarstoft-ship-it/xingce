import json, re
inp = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/A3.json', encoding='utf-8'))
out = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_A3.json', encoding='utf-8'))
assert [m['mat'] for m in inp] == [m['mat'] for m in out], "mat ids/order mismatch"
errs = []
for m in out:
    if len(m['q']) != 5: errs.append((m['mat'], 'count', len(m['q'])))
    for i, q in enumerate(m['q']):
        if q['n'] != i+1: errs.append((m['mat'], q['n'], 'n'))
        if q['answer'] not in 'ABCD' or len(q['answer']) != 1: errs.append((m['mat'], q['n'], 'answer'))
        if not q['jiexi'].endswith(f"故正确答案为{q['answer']}。"): errs.append((m['mat'], q['n'], 'ending'))
        if q['jiexi'].count('故正确答案为') != 1: errs.append((m['mat'], q['n'], 'multiple endings'))
        if q['jiexi'].count('$') % 2: errs.append((m['mat'], q['n'], 'odd $'))
        for seg in re.findall(r'\$(.*?)\$', q['jiexi']):
            if re.search(r'[一-鿿]', seg): errs.append((m['mat'], q['n'], 'CJK in math', seg))
            if re.search(r'(?<!\\)%', seg): errs.append((m['mat'], q['n'], 'unescaped % in math', seg))
            if seg.count('{') != seg.count('}'): errs.append((m['mat'], q['n'], 'brace', seg))
        if q['confidence'] not in ('high','medium','low'): errs.append((m['mat'], q['n'], 'conf'))
        for bad in ['根据我的计算', '程序算得', '程序', '计算机']:
            if bad in q['jiexi']: errs.append((m['mat'], q['n'], 'banned', bad))
print("mats:", len(out), " errors:", errs if errs else "none")
print("answers:", {m['mat']: ''.join(q['answer'] for q in m['q']) for m in out})
print("non-high:", [(m['mat'], q['n'], q['confidence']) for m in out for q in m['q'] if q['confidence'] != 'high'])
