# usage: python3 -I save.py <entries.json>  -- merges entries into check_r5.json (by id), ordered as batch_r5.json
import json, sys, os
T='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/tu/'
OUT=T+'check_r5.json'
batch=json.load(open(T+'batch_r5.json'))
order=[x['id'] for x in batch]
cur={}
if os.path.exists(OUT):
    for e in json.load(open(OUT)):
        cur[e['id']]=e
new=json.load(open(sys.argv[1]))
keys=["id","type","q_ok","q_problem","j_ok","j_problem","jiexi_answer","note"]
for e in new:
    assert e['id'] in order, e['id']
    assert set(e)==set(keys), (e['id'], set(e)^set(keys))
    cur[e['id']]={k:e[k] for k in keys}
res=[cur[i] for i in order if i in cur]
tmp=OUT+'.tmp'
json.dump(res, open(tmp,'w'), ensure_ascii=False, indent=1)
os.replace(tmp, OUT)
print('saved', len(res), 'of', len(order), 'missing:', [i for i in order if i not in cur])
