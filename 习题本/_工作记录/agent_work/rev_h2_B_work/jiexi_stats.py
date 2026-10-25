import json, re, sys
d = json.load(open(sys.argv[1]))
for x in d:
    j = x['jiexi']
    plain = re.sub(r'\$[^$]*\$', 'X', j)
    print(x['vid'], 'len(raw)=', len(j), 'len(math->X)=', len(plain),
          'letter stated:', re.findall(r'选([ABCD])', j), 'time_s', x['time_s'])
    # every number mentioned as an error result should be an option value
    errs = re.findall(r'得(\d+(?:\.\d+)?%?)', j)
    print('    "得N" mentions:', errs, '| options:', list(x['options'].values()))
