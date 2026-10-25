import json, re
d = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/review/revh_D_key.json'))
for q in d:
    j = q['jiexi']
    plain = re.sub(r'\$[^$]*\$', 'X', j)
    print(q['vid'][-3:], 'raw', len(j), 'plain', len(plain), '| 卡点 prefix', j.startswith('卡点'), '| time_s', q['time_s'], '| diff', q['difficulty'])
