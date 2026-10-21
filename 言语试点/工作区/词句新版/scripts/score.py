"""对答案：python3 -I score.py <卷名，如 B01>   读 full/answers/卷_<卷名>_s1.json 和 _s2.json
打印两人各对了多少，以及与原文不一致的题（附作答者的理由和疑问）。"""
import json, sys, os
SP = '/tmp/claude-0/-home-user-xingce/c27c4f14-7f89-5a62-8e0a-9c6994ddaec0/scratchpad'
tag = sys.argv[1]
key = json.load(open(f'{SP}/keys/卷_{tag}.key.json'))
subs = []
for n in (1, 2):
    f = f'{SP}/full/answers/卷_{tag}_s{n}.json'
    if os.path.exists(f):
        subs.append(json.load(open(f)))
def pick(v): return v['pick'] if isinstance(v, dict) else v
for i, s in enumerate(subs, 1):
    print(f'作答者{i}：{sum(pick(s.get(k, "")) == a for k, a in key.items())}/{len(key)}')
for k, a in key.items():
    ps = [pick(s.get(k, '')) for s in subs]
    if any(p != a for p in ps):
        print(f'■ {k} 原文 {a}，作答 {ps}')
        for i, s in enumerate(subs, 1):
            v = s.get(k)
            if isinstance(v, dict) and pick(v) != a:
                print(f'    作答者{i}（{v.get("sure","")}）：{v.get("why","")} ｜疑问：{v.get("doubt","")}')
