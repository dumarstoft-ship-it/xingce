"""python3 qcheck.py ann_result.json -> 对最终保留的每道判断题，抓取 source_url，检查 source_quote 是否在页面正文中出现。"""
import json,sys,re,html,hashlib,subprocess,os,difflib
SP=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
res=json.load(open(sys.argv[1],encoding='utf-8')); res=res.get('result',res)
VER={}
for r in res['results']:
    for v in (r['ver'] or {}).get('items',[]): VER[(v['id'],v['idx'])]=v
items=[]
for r in res['results']:
    for a in r['ann']['articles']:
        for i,j in enumerate(a.get('judgments',[])):
            v=VER.get((a['id'],i))
            if not v or v['verdict']=='drop': continue
            if v['verdict']=='fix':
                fx=v.get('fixed') or {}
                if not all(k in fx for k in ('statement','answer','explain','source_url','source_quote')): continue
                j=fx
            items.append({'id':a['id'],'i':i,'verdict':v['verdict'],**j})
def page(u):
    h=hashlib.md5(u.encode()).hexdigest()[:16]; p=SP+'jpages/'+h+'.html'
    if not (os.path.exists(p) and os.path.getsize(p)>0):
        subprocess.run(['curl','-sSL','--max-time','40','-A','Mozilla/5.0',u,'-o',p],capture_output=True)
    b=open(p,'rb').read() if os.path.exists(p) else b''
    for enc in ('utf-8','gb18030'):
        try: return b.decode(enc)
        except UnicodeDecodeError: pass
    return b.decode('utf-8','ignore')
def norm(t):
    t=html.unescape(re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S))
    t=re.sub(r'<[^>]+>','',t)
    return re.sub(r'[\s　\xa0“”"‘’\'「」『』、，,。．.；;：:！!？?（）()《》<>【】\[\]—\-…·]','',t)
out=[]
for it in items:
    body=norm(page(it['source_url'])); q=norm(it['source_quote'])
    ok=bool(q) and q in body
    ratio=0
    if not ok and body and q:
        m=difflib.SequenceMatcher(None,body,q,autojunk=False).find_longest_match(0,len(body),0,len(q))
        ratio=round(m.size/len(q),2)
    out.append({**it,'found':ok,'ratio':ratio,'pagelen':len(body)})
json.dump(out,open(SP+'qcheck.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('kept',len(items),'found',sum(o['found'] for o in out))
for o in out:
    if not o['found']: print('NOT FOUND',o['id'],o['i'],o['ratio'],o['pagelen'],o['source_url'],o['source_quote'][:50])
