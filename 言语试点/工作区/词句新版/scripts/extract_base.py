"""从现有的"盖句精读"网页里拆出构建新版要用的三样东西：
文章数据 data.json（含全文，不要放进仓库）、ref1310.json、网页外壳 head.html（样式和目录栏，不含文章）。
用法：python3 -I extract_base.py <网页.html> <输出目录>"""
import json, re, sys, os
html = open(sys.argv[1], encoding='utf-8').read()
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
def block(i):
    m = re.search(r'<script id="%s" type="application/json">(.*?)</script>' % i, html, re.S)
    return m.group(1)
data = json.loads(block('data'))
ref = json.loads(block('ref1310'))
for a in data:                       # 新版字段不带进底稿，重建时再并入
    for k in ('q', 'items', 'pilot'):
        a.pop(k, None)
json.dump(data, open(os.path.join(out, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False)
json.dump(ref, open(os.path.join(out, 'ref1310.json'), 'w', encoding='utf-8'), ensure_ascii=False)
head = html[:html.index('<script id="data"')].rstrip() + '\n'
head = re.sub(r'/\* 新版遮词句.*?(?=</style>)', '', head, flags=re.S)   # 去掉上次并入的新版样式
open(os.path.join(out, 'head.html'), 'w', encoding='utf-8').write(head)
print(len(data), '篇 →', out)
