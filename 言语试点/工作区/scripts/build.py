import json, glob, re, sys, os, collections, html as H

SP = os.environ.get('GAIJU_SP', '/tmp/claude-0/-home-user-xingce/209cadd4-dba5-515b-8f1c-c663f6e288a0/scratchpad/')
ARGS = [x for x in sys.argv[1:] if not x.startswith('--words=')]
WFILES = [x[len('--words='):] for x in sys.argv[1:] if x.startswith('--words=')]
ann_path, out_path = ARGS[0], ARGS[1]

ANN, VER = {}, {}
for path in [ann_path] + ARGS[2:]:
    res = json.load(open(path, encoding='utf-8'))
    res = res.get('result', res)
    for r in res['results']:
        for a in r['ann']['articles']:
            ANN[a['id']] = a
        for v in (r['ver'] or {}).get('items', []):
            VER[(v['id'], v['idx'])] = v
WORDS = {}
def _collect(o):
    if isinstance(o, dict):
        if 'result' in o: _collect(o['result']); return
        if 'results' in o:
            for r in o['results']: _collect((r or {}).get('ann') or r)
            return
        for a in o.get('articles', []):
            WORDS.setdefault(a['id'], []).extend(a.get('words', []))
for wf in WFILES:
    _collect(json.load(open(wf, encoding='utf-8')))
dropped_words = []
CS_GROUPS = ['时政与规划', '科技与国防', '法律', '广东省情', '历史文化', '经济社会生态']

tr = json.load(open(SP + 'core/tier_result.json', encoding='utf-8'))['merged']
corder = {c['name']: i for i, c in enumerate(tr['clusters'])}
CL = {i: c['name'] for c in tr['clusters'] for i in c['ids']}

NF_GROUPS = [
    ('总目标与“1310”', ['10155140', '10161789', '10155311']),
    ('1 大湾区建设', ['10167858', '10164275', '10181306']),
    ('2 制造业当家与广货行天下', ['10155013', '10163813', '10163099']),
    ('3 教育科技人才强省', ['10181250', '10181304']),
    ('4 百千万工程与区域协调', ['10169767', '10170615', '10179433']),
    ('5 海洋强省', ['10169594']),
    ('6 绿美广东', ['10155869']),
    ('7 文化强省', ['10182982', '10180091']),
    ('8 民生与共同富裕', ['10164827']),
    ('9 法治广东平安广东', ['10170502', '10182667']),
    ('10 党的建设与政治生态', ['10156656']),
    ('重大工程与经济特区', ['10166714', '10181143']),
]
nfg = {cid: (name, i) for i, (name, ids) in enumerate(NF_GROUPS) for cid in ids}

log = collections.Counter()
dropped_masks = []
out = []
for f in sorted(glob.glob(SP + 'build/json/*.json')) + sorted(glob.glob(SP + 'cs/json/*.json')):
    a = json.load(open(f, encoding='utf-8'))
    an = ANN.get(a['id'])
    if not an:
        log['no_annotation'] += 1
    masks = collections.defaultdict(list)
    for m in (an or {}).get('masks', []):
        masks[m['p']].append(m)
    paras = []
    texts = []
    mcount = 0
    for pi, text in enumerate(a['paras'], 1):
        text = H.unescape(text)
        texts.append(text)
        spans = []
        for m in masks.get(pi, []):
            s = H.unescape(m['s']).strip()
            k = text.find(s)
            if k < 0:
                s2 = s.rstrip('。；！？')
                k = text.find(s2)
                s = s2 if k >= 0 else s
            if k < 0 or not s:
                dropped_masks.append((a['id'], pi, m['s'][:30]))
                log['mask_not_found'] += 1
                continue
            spans.append((k, k + len(s), m.get('label', '')))
        spans.sort()
        segs, pos = [], 0
        for j, (b, e, label) in enumerate(spans):
            if b < pos:
                log['mask_overlap'] += 1
                continue
            if b > pos:
                segs.append({'t': text[pos:b]})
            mcount += 1
            segs.append({'m': text[b:e], 'id': f'p{pi}m{j}', 'label': label})
            pos = e
        if pos < len(text):
            segs.append({'t': text[pos:]})
        if len(text) <= 30 and not re.search(r'[。；！？，]$', text):
            segs[0]['sub'] = True if segs else None
        paras.append(segs)
    if mcount == 0:
        log['article_without_masks'] += 1
    wl, used = [], collections.defaultdict(list)
    for w in WORDS.get(a['id'], []):
        p = w.get('p')
        if not isinstance(p, int) or not 1 <= p <= len(texts):
            log['word_bad_p'] += 1; continue
        t = texts[p - 1]
        ws = H.unescape(w.get('s', '')).strip(); pre = H.unescape(w.get('pre', ''))
        if not ws or len(ws) > 8:
            log['word_bad_s'] += 1; continue
        b = -1
        if pre:
            k = t.find(pre + ws)
            if k >= 0: b = k + len(pre)
        if b < 0:
            if t.count(ws) == 1: b = t.find(ws)
            elif not pre and t.startswith(ws): b = 0
        if b < 0:
            log['word_not_found'] += 1; dropped_words.append((a['id'], p, ws, pre)); continue
        e = b + len(ws)
        if any(not (e <= x or b >= y) for x, y in used[p]):
            log['word_overlap'] += 1; continue
        used[p].append((b, e))
        wl.append({'p': p, 'b': b, 'e': e, 'id': 'w%d' % len(wl), 'type': w.get('type', ''), 'note': w.get('note', '')})
    log['words'] += len(wl)
    js = []
    for idx, j in enumerate((an or {}).get('judgments', [])):
        v = VER.get((a['id'], idx))
        if v is None:
            log['judg_unverified_dropped'] += 1
            continue
        if v['verdict'] == 'drop':
            log['judg_drop'] += 1
            continue
        if v['verdict'] == 'fix':
            fx = v.get('fixed') or {}
            if all(k in fx for k in ('statement', 'answer', 'explain', 'source_url', 'source_quote')):
                j = fx
                log['judg_fix'] += 1
            else:
                log['judg_fix_incomplete_dropped'] += 1
                continue
        else:
            log['judg_ok'] += 1
        js.append({k: j[k] for k in ('statement', 'answer', 'explain', 'source_url', 'source_quote')})
    if a.get('kind') == 'cs':
        gname, gidx = a['group'], CS_GROUPS.index(a['group'])
    elif a['src'] == '人民日报':
        gname = CL.get(a['id'], a.get('group', ''))
        gidx = corder.get(gname, 99)
    else:
        gname, gidx = nfg.get(a['id'].split('_')[1], ('其他', 99))
    out.append({
        'id': a['id'], 'src': a['src'], 'col': a['col'], 'date': a['date'], 'page': a.get('page', ''),
        'title': H.unescape(a['title']), 'author': a.get('author', ''), 'url': a['url'],
        'group': a['focus'] if a.get('kind') == 'cs' else a.get('group', ''), 'kind': a.get('kind', ''),
        'gname': gname, 'gidx': gidx, 'paras': paras, 'judgments': js, 'w': wl,
    })

ref = {
    'intro': '省委十三届三次全会（2023 年 6 月 20 日）提出：“1”是锚定“走在前列”总目标，“3”是激活改革、开放、创新三大动力，“10”是奋力实现“十大新突破”。下表逐字摘自广东省人民政府网新闻稿。',
    'items': [
        '要纵深推进新阶段粤港澳大湾区建设，在牵引全面深化改革开放上取得新突破',
        '要始终坚持实体经济为本、制造业当家，在建设更具国际竞争力的现代化产业体系上取得新突破',
        '要一体推进教育强省、科技创新强省、人才强省建设，在实现高水平科技自立自强上取得新突破',
        '要深入实施“百县千镇万村高质量发展工程”，在城乡区域协调发展上取得新突破',
        '要全面推进海洋强省建设，在打造海上新广东上取得新突破',
        '要深入推进绿美广东生态建设，在打造人与自然和谐共生的现代化广东样板上取得新突破',
        '要扎实推进文化强省建设，在交出物质文明和精神文明两份好的答卷上取得新突破',
        '要用心用情抓好民生社会事业，在推动共同富裕上取得新突破',
        '要扎实推进法治广东平安广东建设，在构建新安全格局上取得新突破',
        '要坚定不移加强党的全面领导和党的建设，在营造良好政治生态上取得新突破',
    ],
    'notes': [
        '全会《决议》第 7 条写作“在努力交出物质文明和精神文明两份好的答卷上取得新突破”，比新闻稿多“努力”二字。',
        '2025 年下半年起，“1310”前面固定加一句：“锚定在推进中国式现代化建设中走在前列的总目标，紧扣坚定不移挑好大梁、全面推进强省建设的总任务”，常与“走在前、作示范、挑大梁”连用。',
        '2026 年省政府工作报告、省“十五五”规划纲要仍沿用“1310”具体部署。',
    ],
    'url': 'https://www.gd.gov.cn/gdywdt/gdyw/content/post_4205038.html',
}

tpl = open(SP + 'build/template.html', encoding='utf-8').read()
data = json.dumps(out, ensure_ascii=False).replace('</', '<\\/')
refs = json.dumps(ref, ensure_ascii=False).replace('</', '<\\/')
html = tpl.replace('/*__DATA__*/', data).replace('/*__REF1310__*/', refs)
open(out_path, 'w', encoding='utf-8').write(html)
print('articles', len(out), dict(log))
print('masks total', sum(1 for a in out for p in a['paras'] for s in p if 'm' in s),
      'judgments', sum(len(a['judgments']) for a in out))
print('dropped masks sample', dropped_masks[:8])
print('dropped words', len(dropped_words), dropped_words[:10])
