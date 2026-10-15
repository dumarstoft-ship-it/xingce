"""用法: python3 fetch_any.py <人民日报或南方日报电子版文章URL>
打印标题行、作者/版面、正文段落（每段一行，前面带 [段号]）和总字数。只读，不写文件。"""
import re,html,sys,subprocess,time
url=sys.argv[1]
t=''
for i in range(3):
    r=subprocess.run(['curl','-sS','--max-time','30',url],capture_output=True)
    t=r.stdout.decode('utf-8','ignore')
    if 'ozoom' in t or 'enpcontent' in t: break
    time.sleep(2)
def clean(p): return re.sub(r'\s+',' ',re.sub('<[^>]+>','',html.unescape(p))).replace('　','').replace('\xa0',' ').strip()
title=''; meta=''
if 'paper.people.com.cn' in url:
    m=re.search(r'<div[^>]*id="ozoom"[^>]*>(.*?)</div>\s*</div>',t,re.S)
    body=m.group(1) if m else ''
    hs=[clean(x) for x in re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>',t,re.S)]
    title=' / '.join(h for h in hs if h)
    sec=re.search(r'<p class="sec">(.*?)</p>',t,re.S)
    meta=clean(re.sub(r'<!--.*?-->','',sec.group(1),flags=re.S)) if sec else ''
    ps=[clean(p) for p in re.findall(r'<p[^>]*>(.*?)</p>',body,re.S)]
    ps=[p for p in ps if p and not re.match(r'^\d{6,}http',p)]
else:
    m=re.search(r'<!--enpcontent-->(.*?)(?:</body>|<!--enpproperty)',t,re.S)
    body=m.group(1) if m else ''
    tm=re.search(r'<title>(.*?)</title>',t,re.S); title=clean(tm.group(1)) if tm else ''
    ps=[clean(p) for p in re.findall(r'<p[^>]*>(.*?)</p>',body,re.S)]
    ps=[p for p in ps if p]
if not ps: print('FAIL: 没取到正文', url); sys.exit(1)
print('标题:', title); print('信息:', meta)
for i,p in enumerate(ps,1): print(f'[{i}] {p}')
print('总字数:', sum(len(p) for p in ps))
