import json, re, sys
for f in sys.argv[1:]:
    d = json.load(open(f))
    for v in d:
        j = v['jiexi']
        plain = re.sub(r'\$[^$]*\$', 'X', j)
        print(f.split('/')[-1], v['vid'], 'raw', len(j), 'plain', len(plain), 'diff', v['difficulty'], 't', v['time_s'], v['direction'], v['answer'])
