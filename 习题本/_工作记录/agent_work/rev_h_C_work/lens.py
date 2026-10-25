import json, re
d = json.load(open('review/revh_C_key.json'))
for q in d:
    j = q['jiexi']
    plain = re.sub(r'\$[^$]*\$', 'X', j)
    print(q['vid'], 'len', len(j), 'plain', len(plain), 'dollars', j.count('$'), 'time', q['time_s'], 'diff', q['difficulty'])
