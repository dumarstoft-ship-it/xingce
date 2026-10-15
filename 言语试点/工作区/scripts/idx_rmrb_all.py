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
base=f'https://paper.people.com.cn/rmrb/pc/layout/{ym}/{dd}/'
t=get(base+'node_01.html')
out=[]
seen=set()
for m in re.finditer(r'<a[^>]*href="(node_\d+\.html)"[^>]*>(.*?)</a>',t):
    node=m.group(1)
    if node in seen: continue
    seen.add(node)
    name=re.sub(r'\s+',' ',re.sub('<[^>]+>','',html.unescape(m.group(2)))).strip()
    p=t if node=='node_01.html' else get(base+node)
    for a in re.finditer(r'<a href="([^"]*content[^"]*)"[^>]*>(.*?)</a>',p,re.S):
        title=re.sub(r'\s+',' ',re.sub('<[^>]+>','',html.unescape(a.group(2)))).strip()
        url='https://paper.people.com.cn/rmrb/pc/'+a.group(1).replace('../','')
        if title: out.append('\t'.join([d,node[5:-5],name,title,url]))
out=sorted(set(out))
open(os.path.join(outdir,d+'.tsv'),'w',encoding='utf-8').write('\n'.join(out)+('\n' if out else ''))
print(d,len(out))
