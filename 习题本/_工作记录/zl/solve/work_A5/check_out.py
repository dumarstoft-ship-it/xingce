import json, re
OUT = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_A5.json'
INP = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/A5.json'
d = json.load(open(OUT, encoding='utf-8'))
inp = json.load(open(INP, encoding='utf-8'))
assert [m['mat'] for m in d] == [m['mat'] for m in inp], "mat order/ids mismatch"
ok = True
def rendered_len(s):
    # rough visible length: strip latex commands
    t = re.sub(r'\\(frac|times|approx|div|text|left|right)', '', s)
    t = t.replace('$','').replace('{','').replace('}','').replace('\\%','%')
    return len(t)
for m in d:
    if len(m['q']) != 5:
        print("BAD count", m['mat']); ok = False
    for i, qq in enumerate(m['q']):
        if qq['n'] != i+1: print("BAD n", m['mat'], qq['n']); ok=False
        if qq['answer'] not in 'ABCD' or len(qq['answer'])!=1: print("BAD answer", m['mat'], qq['n']); ok=False
        mm = re.search(r'故正确答案为([A-D])。$', qq['jiexi'])
        if not mm or mm.group(1) != qq['answer']:
            print("BAD ending", m['mat'], qq['n']); ok=False
        if qq['confidence'] not in ('high','medium','low'): print("BAD conf", m['mat'], qq['n']); ok=False
        if qq['jiexi'].count('$') % 2: print("odd $", m['mat'], qq['n']); ok=False
        for bad in ['根据我的计算','程序算得','程序','我的计算']:
            if bad in qq['jiexi']: print("forbidden phrase", bad, m['mat'], qq['n']); ok=False
        print(m['mat'], qq['n'], qq['answer'], qq['confidence'], 'raw', len(qq['jiexi']), 'vis', rendered_len(qq['jiexi']))
print("ALL OK" if ok else "PROBLEMS FOUND")
