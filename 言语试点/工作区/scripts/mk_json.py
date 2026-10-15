"""python3 mk_json.py final.json  -> cs/json/<id>.json（字段与 build/json 一致，另加 kind/focus/priority_points/extend_points）"""
import re,html,sys,json,subprocess,time,os
SP=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
final=json.load(open(sys.argv[1],encoding='utf-8'))
idx={}
for f in ('rmrb_all.tsv','nf_all.tsv'):
    for line in open(SP+f,encoding='utf-8'):
        c=line.rstrip('\n').split('\t')
        if len(c)==5: idx[c[4]]=c
def get(u,need):
    for i in range(4):
        r=subprocess.run(['curl','-sS','--max-time','30',u],capture_output=True)
        t=r.stdout.decode('utf-8','ignore')
        if need in t: return t
        time.sleep(2)
    return ''
def clean(p): return re.sub(r'\s+',' ',re.sub('<[^>]+>','',html.unescape(p))).replace('　','').replace('\xa0',' ').strip()
ok=0
for a in final['articles']:
    url=a['url'].strip()
    row=idx.get(url) or idx.get(url.replace('epaper.southcn.com','epaper.nfnews.com')) or idx.get(url.replace('epaper.nfnews.com','epaper.southcn.com'))
    cid=re.search(r'content_(\d+)',url).group(1)
    if 'people.com.cn' in url:
        t=get(url,'ozoom')
        m=re.search(r'<div[^>]*id="ozoom"[^>]*>(.*?)</div>\s*</div>',t,re.S)
        ps=[clean(p) for p in re.findall(r'<p[^>]*>(.*?)</p>',m.group(1) if m else '',re.S)]
        ps=[p for p in ps if p and not re.match(r'^\d{6,}http',p)]
        sec=re.search(r'<p class="sec">(.*?)</p>',t,re.S)
        sx=re.sub(r'<!--.*?-->','',sec.group(1),flags=re.S) if sec else ''
        author=re.sub(r'\s+','',html.unescape(re.split(r'<span',sx)[0])) if sx else ''
        pg=re.search(r'第(?:&nbsp;|\s)*(\d+)(?:&nbsp;|\s)*版',sx)
        page=('第%d版'%int(pg.group(1))) if pg else ''
        col=re.sub(r'^\d+版[：:]','',row[2]) if row else ''
        d=row[0] if row else a['date']
        aid=d.replace('-','')+'_'+cid; src='人民日报'
    else:
        t=get(url,'enpcontent')
        m=re.search(r'<!--enpcontent-->(.*?)(?:</body>|<!--enpproperty)',t,re.S)
        ps=[clean(p) for p in re.findall(r'<p[^>]*>(.*?)</p>',m.group(1) if m else '',re.S)]
        ps=[p for p in ps if p]
        author=''
        if ps and len(ps[0])<=20 and not re.search(r'[。，；！？]',ps[0]): author=ps.pop(0)
        d=row[0] if row else a['date']
        page='第%s版'%row[1] if row else a['page']; col=row[2] if row else ''
        aid='nf'+d.replace('-','')+'_'+cid; src='南方日报'
        url=url.replace('epaper.nfnews.com','epaper.southcn.com')
    if not ps: print('FAIL',url); continue
    title=row[3] if row else a['title']
    json.dump({'id':aid,'src':src,'kind':'cs','date':d,'col':col,'page':page,'title':title,'url':url,'author':author,
               'paras':ps,'chars':sum(len(p) for p in ps),'group':a['group'],'focus':a['focus'],
               'priority_points':a['priority_points'],'extend_points':a['extend_points'],'why':a['why']},
              open(SP+f'json/{aid}.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
    ok+=1; print('OK',aid,src,col,len(ps),sum(len(p) for p in ps),title)
print('total ok',ok,'of',len(final['articles']))
