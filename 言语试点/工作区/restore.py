"""从 annotations.json 恢复盖句精读的工作目录。

仓库里只存标注（遮挡位置、判断题、遮词辨析）和原文链接，不存文章全文。
本脚本按链接重新抓取原文，用每段的 md5 核对段落没变，再把标注还原成 build.py 能直接用的输入。

用法：python3 restore.py <工作区目录> <输出目录>
之后：GAIJU_SP=<输出目录>/ python3 <输出目录>/build/build.py <输出目录>/restored_ann.json 盖句精读.html --words=<输出目录>/restored_words.json
"""
import json, re, sys, os, hashlib, html as H, subprocess, time, shutil
from concurrent.futures import ThreadPoolExecutor

WS, OUT = sys.argv[1].rstrip('/') + '/', sys.argv[2].rstrip('/') + '/'
for d in ('build/json', 'cs/json', 'core'):
    os.makedirs(OUT + d, exist_ok=True)
ann = json.load(open(WS + 'annotations.json', encoding='utf-8'))


def get(url, need):
    for i in range(4):
        r = subprocess.run(['curl', '-sS', '--max-time', '30', url], capture_output=True)
        t = r.stdout.decode('utf-8', 'ignore')
        if need in t:
            return t
        time.sleep(2)
    return ''


def candidates(p):
    """抓取时用过的几种清洗方式，逐一试，看哪种和存下的 md5 对得上。"""
    a = re.sub('<[^>]+>', '', H.unescape(p)).replace('　', '').replace('\xa0', ' ').strip()
    b = re.sub(r'\s+', ' ', re.sub('<[^>]+>', '', H.unescape(p))).replace('　', '').strip()
    c = re.sub(r'\s+', ' ', re.sub('<[^>]+>', '', H.unescape(p))).replace('　', '').replace('\xa0', ' ').strip()
    out = []
    for x in (a, b, c, c.replace('​', '').strip()):
        if x and x not in out:
            out.append(x)
    return out


def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()[:12]


def fetch(a):
    url = a['url']
    if 'people.com.cn' in url:
        t = get(url, 'ozoom')
        m = re.search(r'<div[^>]*id="ozoom"[^>]*>(.*?)</div>\s*</div>', t, re.S)
        body = m.group(1) if m else ''
    else:
        t = get(url, 'enpcontent') or get(url.replace('epaper.southcn.com', 'epaper.nfnews.com'), 'enpcontent')
        m = re.search(r'<!--enpcontent-->(.*?)(?:</body>|<!--enpproperty)', t, re.S)
        body = m.group(1) if m else ''
    raw = re.findall(r'<p[^>]*>(.*?)</p>', body, re.S)
    want, got, i = a['para_md5'], [], 0
    for p in raw:
        if i >= len(want):
            break
        for c in candidates(p):
            if md5(c) == want[i]:
                got.append(c); i += 1
                break
    return a, got


ok, bad = 0, []
with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(fetch, ann))
art_by_id = {}
for a, paras in res:
    if len(paras) != len(a['para_md5']):
        bad.append((a['id'], len(paras), len(a['para_md5']), a['url']))
        continue
    meta = {k: v for k, v in a.items() if k not in ('para_md5', 'masks', 'judgments', 'words')}
    meta['paras'] = paras
    meta['chars'] = sum(len(p) for p in paras)
    d = 'cs/json/' if a.get('kind') == 'cs' else 'build/json/'
    json.dump(meta, open(OUT + d + a['id'] + '.json', 'w', encoding='utf-8'), ensure_ascii=False)
    art_by_id[a['id']] = paras
    ok += 1

articles, ver, words = [], [], []
for a in ann:
    if a['id'] not in art_by_id:
        continue
    texts = [H.unescape(p) for p in art_by_id[a['id']]]
    masks = [{'p': p, 's': texts[p - 1][b:e], 'label': lab} for p, b, e, lab, _id in sorted(a['masks'], key=lambda m: (m[0], m[1]))]
    articles.append({'id': a['id'], 'masks': masks, 'judgments': a['judgments']})
    ver += [{'id': a['id'], 'idx': i, 'verdict': 'ok', 'fixed': {}, 'note': 'restored'} for i in range(len(a['judgments']))]
    ws = sorted(a['words'], key=lambda w: int(w[5][1:]))
    if ws:
        words.append({'id': a['id'], 'words': [{'p': p, 's': texts[p - 1][b:e], 'pre': texts[p - 1][max(0, b - 8):b], 'type': ty, 'note': no} for p, b, e, ty, no, _id in ws]})

json.dump({'results': [{'ann': {'articles': articles}, 'ver': {'items': ver}}]}, open(OUT + 'restored_ann.json', 'w', encoding='utf-8'), ensure_ascii=False)
json.dump({'articles': words}, open(OUT + 'restored_words.json', 'w', encoding='utf-8'), ensure_ascii=False)
cl = json.load(open(WS + 'core_clusters.json', encoding='utf-8'))
json.dump({'merged': cl}, open(OUT + 'core/tier_result.json', 'w', encoding='utf-8'), ensure_ascii=False)
for f in ('build.py', 'template.html', 'test.js', 't3.js'):
    shutil.copy(WS + 'scripts/' + f, OUT + 'build/' + f)
print('restored', ok, 'of', len(ann))
for b in bad:
    print('MISMATCH', b)
