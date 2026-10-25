import json
q = {x['vid']: x for x in json.load(open('review/revh_C_questions.json'))}
k = {x['vid']: x for x in json.load(open('review/revh_C_key.json'))}
g = {}
for f in ['gen/D01_math_h.json', 'gen/D01_math_h2.json', 'gen/D01_math_h3.json']:
    for x in json.load(open(f)):
        g[x['vid']] = x
for v in q:
    a, b, c = q[v], k[v], g.get(v)
    same = a['stem'] == b['stem'] and a['options'] == b['options']
    same_g = c is not None and c['stem'] == b['stem'] and c['options'] == b['options'] and c.get('answer') == b['answer'] and c.get('jiexi') == b['jiexi']
    print(v, 'q==key', same, '| gen==key', same_g)
# method-hint words in stems
hints = ['十字交叉', '不变量', '整除', '反比', '打包', '赋值', '份数', '方程', '倒推', '假设']
for v in q:
    s = q[v]['stem']
    hit = [h for h in hints if h in s]
    if hit: print('HINT WORD in stem', v, hit)
