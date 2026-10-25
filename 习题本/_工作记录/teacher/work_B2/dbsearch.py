import json, re, sys
d = json.load(open('db/real_raw.json'))
ex = json.load(open('teacher/examples.json'))
mine = [x for x in ex if 'T038' <= x['tid'] <= 'T081']
def norm(s):
    s = re.sub(r'（[^）]*?(19|20)\d\d[^）]*?）', '', s)
    s = re.sub(r'[\s\W_]+', '', s)
    return s
def grams(s, n=3):
    return set(s[i:i+n] for i in range(len(s)-n+1))
dbg = [(x['id'], x['paper_name'], x['num'], grams(norm(x.get('text') or ''))) for x in d]
for x in mine:
    q = norm(x['question'])
    g = grams(q)
    if not g:
        print(x['tid'], 'EMPTY'); continue
    scores = []
    for (i, pn, num, gg) in dbg:
        if not gg: continue
        s = len(g & gg) / max(1, min(len(g), len(gg)))
        scores.append((s, i, pn, num))
    scores.sort(reverse=True)
    top = scores[:3]
    print(x['tid'], x['source'], 'db=', x['db_match'], '|', ' ; '.join(f'{i}({pn}#{num}) {s:.2f}' for s, i, pn, num in top))
