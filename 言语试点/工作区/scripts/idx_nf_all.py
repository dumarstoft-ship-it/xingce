import re,html,sys,subprocess,time,os
def get(u):
    for i in range(3):
        r=subprocess.run(['curl','-sS','--max-time','25',u],capture_output=True)
        t=r.stdout.decode('utf-8','ignore')
        if t: return t
        time.sleep(1.5)
    return ''
d,outdir=sys.argv[1],sys.argv[2]
ym=d[:7].replace('-',''); dd=d[8:]
out=[]
# old layout
base=f'https://epaper.southcn.com/nfdaily/html/{ym}/{dd}/'
t=get(base+'node_A01.html')
pages=sorted(set(re.findall(r'第([A-Z]+\d+)版[：:]([^<_"]+)',t)))
for code,name in pages:
    if not re.fullmatch(r'A\d+',code): continue
    p=get(base+f'node_{code}.html')
    for a in re.finditer(r'<a[^>]*href="([^"]*content_\d+\.html)"[^>]*>(.*?)</a>',p,re.S):
        title=re.sub(r'\s+',' ',re.sub('<[^>]+>','',html.unescape(a.group(2)))).strip()
        url=a.group(1)
        if not url.startswith('http'): url=base+url.split('/')[-1]
        if title: out.append('\t'.join([d,code,name.strip(),title,url]))
if not out:
    base=f'https://epaper.nfnews.com/nfdaily/html/{ym}/{dd}/'
    t=get(base+'node_A01.html')
    pages=sorted(set(re.findall(r'"?layout"?:"([A-Z]+\d+)","?layoutName"?:"([^"]+)"',t)))
    for code,name in pages:
        if not re.fullmatch(r'A\d+',code): continue
        p=get(base+f'node_{code}.html')
        for m in re.finditer(r'title:"(.*?)",urlPad:"[^"]*",url:"(https://epaper\.nfnews\.com/nfdaily/html/\d+/\d+/content_\d+\.html)"',p,re.S):
            title=re.sub(r'\s+',' ',re.sub('<[^>]+>','',html.unescape(m.group(1)))).strip()
            if title: out.append('\t'.join([d,code,name,title,m.group(2)]))
out=sorted(set(out))
open(os.path.join(outdir,d+'.tsv'),'w',encoding='utf-8').write('\n'.join(out)+('\n' if out else ''))
print(d,len(out))
