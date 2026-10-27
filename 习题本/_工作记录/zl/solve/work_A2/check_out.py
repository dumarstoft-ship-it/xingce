import json, re
p='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_A2.json'
data=json.load(open(p,encoding='utf-8'))
inp=json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/A2.json',encoding='utf-8'))
assert [d['mat'] for d in data]==[d['mat'] for d in inp], 'mat order mismatch'
ok=True
for d in data:
    qs=d['q']
    if len(qs)!=5 or [q['n'] for q in qs]!=[1,2,3,4,5]:
        print('BAD count', d['mat']); ok=False
    for q in qs:
        if q['answer'] not in 'ABCD' or len(q['answer'])!=1: print('BAD ans', d['mat'], q['n']); ok=False
        m=re.search(r'故正确答案为([A-D])。$', q['jiexi'])
        if not m or m.group(1)!=q['answer']: print('BAD end', d['mat'], q['n']); ok=False
        # math segments: check balanced $ and no CJK inside
        segs=q['jiexi'].split('$')
        if len(segs)%2==0: print('UNBALANCED $', d['mat'], q['n']); ok=False
        for i,s in enumerate(segs):
            if i%2==1:
                if re.search(r'[一-鿿]', s): print('CJK in math', d['mat'], q['n'], s); ok=False
                if re.search(r'(?<!\\)%', s): print('unescaped % in math', d['mat'], q['n'], s); ok=False
        # visible length approx: strip math, count math as rendered roughly
        vis = re.sub(r'\$[^$]*\$', lambda mm: re.sub(r'\\[a-zA-Z]+|[{}\\ ]','',mm.group(0)[1:-1]), q['jiexi'])
        for bad in ['根据我的计算','程序','计算得出','Python']:
            if bad in q['jiexi']: print('BAD word', d['mat'], q['n'], bad); ok=False
        print(d['mat'], q['n'], q['answer'], q['confidence'], 'raw', len(q['jiexi']), 'vis', len(vis))
print('ALL OK' if ok else 'PROBLEMS')
