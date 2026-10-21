"""Render one article from the uploaded data with masks marked.
usage: python3 -I show.py <data.json> <article-id|index> [w|m|both]"""
import json, sys
d = json.load(open(sys.argv[1]))
key = sys.argv[2]
mode = sys.argv[3] if len(sys.argv) > 3 else 'both'
a = d[int(key)] if key.isdigit() else next(x for x in d if x['id'] == key)
print(a['id'], a['src'], a['col'], a['date'], a['title'], '|', a['group'], '| paras', len(a['paras']))
ws = a.get('w', [])
for pi, para in enumerate(a['paras']):
    full = ''.join(x.get('t', x.get('m', '')) for x in para)
    # thesis masks positions
    marks = []
    pos = 0
    for x in para:
        s = x.get('t', x.get('m', ''))
        if 'm' in x and mode in ('m', 'both'):
            marks.append((pos, pos + len(s), '〔', '〕' + (x.get('label') or '')))
        pos += len(s)
    if mode in ('w', 'both'):
        for w in ws:
            if w['p'] == pi + 1:
                marks.append((w['b'], w['e'], '【', '】'))
    # insert markers from the end
    out = full
    ins = []
    for b, e, l, r in marks:
        ins.append((e, r)); ins.append((b, l))
    for p, t in sorted(ins, key=lambda z: -z[0]):
        out = out[:p] + t + out[p:]
    print(f'[{pi+1}] {out}')
if mode in ('w', 'both'):
    print('--- word notes')
    for w in ws:
        full = ''.join(x.get('t', x.get('m', '')) for x in a['paras'][w['p']-1])
        print(f"p{w['p']} {w['type'] or '-'} 「{full[w['b']:w['e']]}」 {w['note']}")
print('--- judgments')
for j in a.get('judgments', []):
    print(('√' if j['answer'] else '×'), j['statement'])
