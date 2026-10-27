import json, re
d = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_A7.json', encoding='utf-8'))
bad = 0; nseg = 0
for m in d:
    for q in m['q']:
        segs = re.findall(r'\$([^$]*)\$', q['jiexi'])
        nseg += len(segs)
        for s in segs:
            if s.count('{') != s.count('}') or re.search(r'[一-鿿]', s):
                print('CHECK', m['mat'], q['n'], s); bad += 1
            for cmd in re.findall(r'\\([A-Za-z]+)', s):
                if cmd not in ('frac', 'approx', 'times', 'div'):
                    print('CMD', cmd, m['mat'], q['n'])
print('segments', nseg, 'issues', bad)
