"""主旨题对答案：python3 -I zz_score.py <卷名，如 ZP3>   读 zz/keys/卷_<卷名>.key.json 和 zz/answers/卷_<卷名>_s*.json
打印每位作答者对了多少、把握分布，以及选错的题、把握低的题（附理由和疑问）。"""
import json, sys, os, glob, collections
SP = '/tmp/claude-0/-home-user-xingce/c27c4f14-7f89-5a62-8e0a-9c6994ddaec0/scratchpad'
tag = sys.argv[1]
key = json.load(open(f'{SP}/zz/keys/卷_{tag}.key.json'))
for f in sorted(glob.glob(f'{SP}/zz/answers/卷_{tag}_s*.json')):
    s = json.load(open(f))
    ok = sum(s.get(k, {}).get('pick') == a for k, a in key.items())
    print(f'{os.path.basename(f)}：{ok}/{len(key)}，把握', dict(collections.Counter(v.get('sure') for v in s.values())))
    for k, a in key.items():
        v = s.get(k, {})
        if v.get('pick') != a or v.get('sure') == '低':
            print(f"  {'■ 选错' if v.get('pick') != a else '□ 低把握'} {k} 答案 {a}，选 {v.get('pick')}（{v.get('sure')}）：{v.get('why','')} ｜疑问：{v.get('doubt','')}")
