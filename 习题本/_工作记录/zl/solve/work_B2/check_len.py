import json, re
d = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_B2.json', encoding='utf-8'))
def visible(s):
    # approximate visible length: strip latex commands and braces/dollars
    t = re.sub(r'\\(frac|times|approx|text|Leftrightarrow|to)', ' ', s)
    t = t.replace('\\%','%')
    t = re.sub(r'[{}$\\]', '', t)
    t = t.replace(' ', '')
    return len(t)
for m in d:
    for q in m['q']:
        print(m['mat'], q['n'], q['answer'], 'raw', len(q['jiexi']), 'vis', visible(q['jiexi']))
