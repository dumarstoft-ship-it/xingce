import json, re
base = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/'
out = json.load(open(base+'out_B8.json', encoding='utf-8'))
task = json.load(open(base+'B8.json', encoding='utf-8'))
assert [m['mat'] for m in out] == [t['mat'] for t in task], "mat order mismatch"
comp = {('MK2701X-M3',5),('MK2717X-M1',5),('MK2739X-M2',5),('MK26ZX-M2',5),('MK2701X-M2',5),('MK2705X-M3',5)}
ok = True
for m in out:
    assert len(m['q']) == 5, m['mat']
    assert [q['n'] for q in m['q']] == [1,2,3,4,5], m['mat']
    for q in m['q']:
        a = q['answer']; j = q['jiexi']
        errs = []
        if a not in 'ABCD' or len(a) != 1: errs.append('bad answer')
        if not j.endswith(f'故正确答案为{a}。'): errs.append('bad ending')
        if j.count('$') % 2: errs.append('unbalanced $')
        if j.count('故正确答案为') != 1: errs.append('multiple endings')
        for bad in ['根据我的计算','程序算得','程序','计算机','Python','python']:
            if bad in j: errs.append('forbidden '+bad)
        # plain % inside math must be escaped
        for seg in re.findall(r'\$(.+?)\$', j):
            if re.search(r'(?<!\\)%', seg): errs.append('unescaped % in math: '+seg)
            if re.search(r'[一-鿿]', seg): errs.append('CJK in math: '+seg)
        lim = 350 if (m['mat'], q['n']) in comp else 250
        L = len(j)
        if L < 80 or L > lim: errs.append(f'length {L} (limit {lim})')
        print(m['mat'], q['n'], a, q['confidence'], L, 'OK' if not errs else errs)
        ok = ok and not errs
print("ALL OK" if ok else "ISSUES FOUND")
print("summary:", {m['mat']: ''.join(q['answer'] for q in m['q']) for m in out})
print("low:", [(m['mat'], q['n'], q['problem']) for m in out for q in m['q'] if q['confidence']=='low'])
print("medium:", [(m['mat'], q['n']) for m in out for q in m['q'] if q['confidence']=='medium'])
