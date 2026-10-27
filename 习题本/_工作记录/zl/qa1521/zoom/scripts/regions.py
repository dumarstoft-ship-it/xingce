import re, json, os
SP='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/'
HTML=SP+'zl/out/zl_d15-21.html'
h=open(HTML,encoding='utf-8').read()
body=h[h.find('<body'):]
sets=re.split(r'<section class="set">', body)[1:]
items=[]
for s in sets:
    t=re.search(r'<span class="t">第 (\d+) 套', s).group(1)
    sec=None
    for m in re.finditer(r'<div class="mat-h">(.*?)</div>|<img class="chunk" src="file://([^"]+)"|<div class="q"><span class="no">(\d+)</span><img class="qi" src="file://([^"]+)"', s):
        if m.group(1): sec=m.group(1)[:3]
        elif m.group(2): items.append((t,sec,'M',None,m.group(2).split('/')[-1]))
        else: items.append((t,sec,'Q',m.group(3),m.group(4).split('/')[-1]))
db=json.load(open(SP+'db/zl_raw.json',encoding='utf-8'))
by={r['id']:r for r in db}
cache={}
def lines_for(qfile):
    if qfile in cache: return cache[qfile]
    cands=[SP+'lines/'+os.path.basename(qfile)+'.json', qfile+'.json']
    for c in cands:
        if os.path.exists(c):
            cache[qfile]=json.load(open(c,encoding='utf-8')); return cache[qfile]
    cache[qfile]=None; return None
qstart=re.compile(r'^\s*\d{1,3}\s*[、.．]')
def page_lines(L,pg):
    for p in L['pages']:
        if p['page']==pg: return p
    return None
def analyze(rid, regions, kind):
    r=by[rid]; L=lines_for(r['qfile'])
    out=[]
    if L is None: return ['NO LINES for '+r['qfile']]
    pages=sorted(regions.keys(), key=lambda x:int(x))
    for i,pg in enumerate(pages):
        t,b=regions[pg]
        P=page_lines(L,int(pg))
        if P is None: out.append('no page %s'%pg); continue
        ls=P['lines']
        inside=[l for l in ls if (l['top']+l['bottom'])/2>=t and (l['top']+l['bottom'])/2<=b]
        straddle=[l for l in ls if (l['top']<t-0.5<l['bottom']-1) or (l['top']+1<b+0.5<l['bottom'])]
        after=[l for l in ls if (l['top']+l['bottom'])/2>b]
        after=sorted(after,key=lambda l:l['top'])
        before=sorted([l for l in ls if (l['top']+l['bottom'])/2<t],key=lambda l:l['top'])
        imgs=P.get('images',[])
        for im in imgs:
            if im['top']<t-1<im['bottom']-2 or im['top']+2<b+1<im['bottom']:
                out.append('IMAGE STRADDLES p%s region[%.1f,%.1f] img[%.1f,%.1f]'%(pg,t,b,im['top'],im['bottom']))
        for l in straddle:
            out.append('LINE STRADDLES p%s [%.1f,%.1f] line[%.1f,%.1f] %s'%(pg,t,b,l['top'],l['bottom'],l['text'][:40]))
        if kind=='M' and i==0 and inside:
            out.append('FIRST: '+' | '.join(x['text'][:30] for x in inside[:2]))
        if inside:
            out.append('LAST p%s: %s'%(pg,inside[-1]['text'][-30:]))
        if after:
            a=after[0]; gap=a['top']-b
            # treat footer: very low on page
            foot = a['top']>P['height']-70
            out.append('NEXT p%s gap=%.1f %s%s'%(pg,gap,('[footer] ' if foot else ''),a['text'][:40]))
        if before and kind=='M' and i==0:
            out.append('PREV p%s: %s'%(pg,before[-1]['text'][:40]))
    return out
seen=set()
for it in items:
    st,sec,kind,no,f=it
    m=re.match(r'(.+?)_(q|p\d+)(_t)?\.png',f)
    rid=m.group(1); part=m.group(2)
    if kind=='Q':
        res=analyze(rid, by[rid]['regions'],'Q')
        print('##',st,sec,'Q%s'%no,f); [print('   ',x) for x in res]
    else:
        if rid in seen: continue
        seen.add(rid)
        res=analyze(rid, by[rid]['stem_regions'],'M')
        print('##',st,sec,'MAT',rid); [print('   ',x) for x in res]
