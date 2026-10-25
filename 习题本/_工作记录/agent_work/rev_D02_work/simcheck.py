import json, re, sys
qs = json.load(open(sys.argv[1], encoding='utf-8'))
db = json.load(open(sys.argv[2], encoding='utf-8'))
def grams(s, n=3):
    s = re.sub(r'\s+', '', s)
    return {s[i:i+n] for i in range(len(s)-n+1)}
dbg = [(x['id'], grams(x.get('text') or ''), x.get('text') or '') for x in db if x.get('kind') == '数学运算' or '数学' in (x.get('section') or '') or True]
for q in qs:
    g = grams(q['stem'])
    best = sorted(((len(g & h) / max(1, len(g | h)), i, t) for i, h, t in dbg), reverse=True)[:2]
    print(q['vid'], [(i, round(s, 3)) for s, i, t in best])
