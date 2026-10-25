import json, re, sys
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
for f in sys.argv[1:]:
    a = json.load(open(S + '/gen/' + f))
    for v in a:
        j = v['jiexi']
        plain = re.sub(r'\$[^$]*\$', 'X', j)
        print(f, v['vid'], 'len', len(j), 'nomath', len(plain), '| stem end:', v['stem'][-14:])
