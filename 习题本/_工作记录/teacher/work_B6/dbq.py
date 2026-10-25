import json, sys, re
D = json.load(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/db/real_raw.json'))
mode = sys.argv[1]
if mode == 'id':
    for i in sys.argv[2:]:
        for e in D:
            if e['id'] == i:
                print('=' * 80)
                print(e['id'], e['paper_name'], e['kind'], 'ans=', e['answer_official'])
                print(e['text'])
                print('-- jiexi:', (e['jiexi_raw'] or '')[:800])
elif mode == 'grep':
    pats = sys.argv[2:]
    for e in D:
        t = (e['text'] or '')
        if all(re.search(p, t) for p in pats):
            print('=' * 80)
            print(e['id'], e['paper_name'], e['kind'], 'ans=', e['answer_official'])
            print(t[:500])
