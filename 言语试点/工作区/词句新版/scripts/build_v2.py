"""把新版遮词句（选词填空 / 语句填空）和广东式政治常识题并进"盖句精读"网页。

用法：
python3 -I build_v2.py --base data.json --ref ref1310.json --head head.html --css extra.css --js app_v2.js \
    --masks M1.json M2.json ... --items P1.json P2.json ... --zz Z1.json ... --out 盖句精读.html [--ver v2] [--note 说明]

base 是现有网页里嵌的 151 篇数据（含全文、点题句、旧遮词 w、旧判断题 judgments）。
masks 里每题按 pre+s 在段落原文中定位，算出起止位置；items 原样并入，答案转成下标。
zz 是主旨理解题：题干材料由第 from_p 到 to_p 段截取删改而来，这里算出它和原文的差异（删了哪些、加了哪些），网页答完后标出来。
"""
import argparse, difflib, json, sys

ap = argparse.ArgumentParser()
for k in ('base', 'ref', 'head', 'css', 'js', 'out'):
    ap.add_argument('--' + k, required=True)
ap.add_argument('--masks', nargs='*', default=[])
ap.add_argument('--items', nargs='*', default=[])
ap.add_argument('--zz', nargs='*', default=[])
ap.add_argument('--ver', default='v2')
ap.add_argument('--note', default='')
args = ap.parse_args()

data = json.load(open(args.base, encoding='utf-8'))
by = {a['id']: a for a in data}
L = 'ABCD'


def para_text(a, p):
    return ''.join(x.get('t', x.get('m', '')) for x in a['paras'][p - 1])


errors = []
for path in args.masks:
    for art in json.load(open(path, encoding='utf-8'))['articles']:
        a = by[art['id']]
        qs = []
        for qi, q in enumerate(art['questions']):
            text = para_text(a, q['p'])
            blanks = []
            for b in q['blanks']:
                key = b.get('pre', '') + b['s']
                if text.count(key) != 1:
                    errors.append(f"{a['id']} 第{qi+1}题 定位失败：{key}")
                    break
                i = text.index(key) + len(b.get('pre', ''))
                blanks.append({'b': i, 'e': i + len(b['s'])})
            else:
                ans = L.index(q['answer'])
                want = ' '.join(text[x['b']:x['e']] for x in blanks)
                if q['options'][ans] != want:
                    errors.append(f"{a['id']} 第{qi+1}题 正确项和原文不一致：{q['options'][ans]} / {want}")
                    continue
                qs.append({'kind': q['kind'], 'p': q['p'], 'blanks': blanks, 'options': q['options'],
                           'answer': ans, 'note': q['note']})
        qs.sort(key=lambda q: (q['p'], q['blanks'][0]['b']))
        for i, q in enumerate(qs):
            q['id'] = 'q%d' % (i + 1)
        a['q'] = qs
        a['pilot'] = True

for path in args.items:
    for art in json.load(open(path, encoding='utf-8'))['articles']:
        a = by[art['id']]
        items = []
        for ii, it in enumerate(art['items']):
            t = it['type']
            ans = it['answer']
            if t == '判断':
                if not isinstance(ans, bool):
                    errors.append(f"{a['id']} 第{ii+1}道题 判断题答案要是 true/false"); continue
                opts = None
            elif t == '单选':
                ans = L.index(ans); opts = it['options']
            elif t == '多选':
                ans = sorted(L.index(x) for x in ans); opts = it['options']
            else:
                errors.append(f"{a['id']} 第{ii+1}道题 题型不认识：{t}"); continue
            if opts is not None and len(opts) != 4:
                errors.append(f"{a['id']} 第{ii+1}道题 选项不是 4 个"); continue
            x = {'id': 'i%d' % (ii + 1), 'area': it['area'], 'type': t, 'stem': it['stem'], 'answer': ans,
                 'explain': it['explain'], 'sources': it.get('sources', [])}
            if opts is not None:
                x['options'] = opts
            items.append(x)
        a['items'] = items
        a['pilot'] = True



def unpack_edits(orig, ed):
    out, pos = [], 0
    for e in ed:
        if e[0] == '-':
            out.append(orig[pos:e[1]]); pos = e[2]
        else:
            out.append(orig[pos:e[1]]); pos = e[1]; out.append(e[2])
    out.append(orig[pos:])
    return ''.join(out)


def diff_ops(orig, passage):
    """原文和题干材料逐字比对：= 相同，- 命题人删去，+ 命题人添上或改写成的字。"""
    ops = []
    sm = difflib.SequenceMatcher(None, orig, passage, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal': ops.append(['=', orig[i1:i2]])
        else:
            if i2 > i1: ops.append(['-', orig[i1:i2]])
            if j2 > j1: ops.append(['+', passage[j1:j2]])
    return ops


for path in args.zz:
    for art in json.load(open(path, encoding='utf-8'))['articles']:
        a = by[art['id']]
        zs = []
        for zi, z in enumerate(art['questions']):
            f, t = z['from_p'], z['to_p']
            if not (1 <= f <= t <= len(a['paras'])):
                errors.append(f"{a['id']} 主旨第{zi+1}题 段号不对：{f}-{t}"); continue
            orig = '\n'.join(para_text(a, p) for p in range(f, t + 1))
            # 仓库里的存档不放原文，只有删改记录 edits，这里用原文还原题干
            passage = z['passage'].strip() if 'passage' in z else unpack_edits(orig, z['edits'])
            hide = sorted(set(z.get('hide_p') or []))
            zs.append({'type': z.get('type', ''), 'from': f, 'to': t, 'passage': passage, 'stem': z['stem'],
                       'options': z['options'], 'answer': L.index(z['answer']), 'note': z['note'],
                       'hide': hide, 'diff': diff_ops(orig, passage)})
        zs.sort(key=lambda z: z['from'])
        for i in range(1, len(zs)):
            if zs[i]['from'] <= zs[i - 1]['to']:
                errors.append(f"{a['id']} 主旨题段落重叠：{zs[i-1]['from']}-{zs[i-1]['to']} 和 {zs[i]['from']}-{zs[i]['to']}")
        for z in zs:
            for h in z['hide']:
                if not (isinstance(h, int) and 1 <= h <= len(a['paras'])) or any(y['from'] <= h <= y['to'] for y in zs):
                    errors.append(f"{a['id']} 主旨题第{z['from']}段那题的 hide_p 不对：{h}")
        for i, z in enumerate(zs):
            z['id'] = 'z%d' % (i + 1)
        a['z'] = zs

if errors:
    print('\n'.join(errors))
    sys.exit(1)


def blob(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


head = open(args.head, encoding='utf-8').read().rstrip() + '\n'
css = open(args.css, encoding='utf-8').read()
head = head.replace('</style>', css + '</style>', 1)
html = (head + '<script id="data" type="application/json">' + blob(data) + '</script>\n'
        + '<script id="ref1310" type="application/json">' + open(args.ref, encoding='utf-8').read().strip().replace('</', '<\\/') + '</script>\n'
        + '<script id="meta" type="application/json">' + blob({'ver': args.ver, 'note': args.note}) + '</script>\n'
        + '<script>\n' + open(args.js, encoding='utf-8').read() + '</script>\n</body>\n</html>\n')
open(args.out, 'w', encoding='utf-8').write(html)
n = sum(1 for a in data if a.get('pilot'))
print(f"写出 {args.out}：{len(data)} 篇，新版 {n} 篇，词句题 {sum(len(a.get('q', [])) for a in data)} 道，主旨题 {sum(len(a.get('z', [])) for a in data)} 道（{sum(1 for a in data if a.get('z'))} 篇），政治常识题 {sum(len(a.get('items', [])) for a in data)} 道，{len(html)//1024} KB")
