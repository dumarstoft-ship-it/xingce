"""跨篇撞题扫描：python3 -I dup_scan.py <data.json> <M*.json ...>
南方日报评论常整句沿用省委提法，同一句话会出现在不同文章里。这里找出不同文章中、挖空所在句子几乎相同的题，
以及正确项相同、选项有两项以上重合的题。"""
import json, sys, re, difflib, itertools
data = {a['id']: a for a in json.load(open(sys.argv[1]))}
def ptext(a, p): return ''.join(x.get('t', x.get('m', '')) for x in data[a]['paras'][p - 1])
rows = []
for f in sys.argv[2:]:
    name = f.split('/')[-1]
    for art in json.load(open(f))['articles']:
        aid = art['id']
        for q in art['questions']:
            t = ptext(aid, q['p']); b0 = q['blanks'][0]
            k = t.index(b0.get('pre', '') + b0['s']) + len(b0.get('pre', ''))
            st = max(t.rfind(c, 0, k) for c in '。！？；') + 1
            ends = [t.find(c, k) for c in '。！？；' if t.find(c, k) >= 0]
            en = min(ends) if ends else len(t)
            ans = q['options']['ABCD'.index(q['answer'])]
            rows.append((name, aid, data[aid]['title'], t[st:en], ans, set(q['options'])))
seen = set()
for x, y in itertools.combinations(rows, 2):
    if x[1] == y[1]: continue
    r = difflib.SequenceMatcher(None, x[3], y[3]).ratio()
    same_ans = x[4] == y[4] and len(x[5] & y[5]) >= 2
    if r > 0.75 or same_ans:
        print(f"撞题？{x[0]}《{x[2]}》／{y[0]}《{y[2]}》 句子相似度 {r:.2f}，正确项 {x[4]}／{y[4]}")
        print('   ', x[3][:70]); print('   ', y[3][:70])
print('扫描完毕')
