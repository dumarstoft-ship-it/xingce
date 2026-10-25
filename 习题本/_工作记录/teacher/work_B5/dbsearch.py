import json, re, sys
d = json.load(open(sys.argv[1]))
sel = json.load(open(sys.argv[2]))
db = [x for x in d if x['section'] == '数量关系']
def norm(s):
    s = re.sub(r'[\s\W_]+', '', s or '')
    return s
def grams(s, n=3):
    return set(s[i:i+n] for i in range(len(s)-n+1))
dbg = [(x['id'], grams(norm(x['text']))) for x in db]
for x in sel:
    q = norm(x['question'])
    g = grams(q)
    if not g:
        continue
    scores = sorted(((len(g & h) / max(1, min(len(g), len(h))), i) for i, h in dbg), reverse=True)[:3]
    print(x['tid'], x['db_match'], [(i, round(s, 2)) for s, i in scores])
