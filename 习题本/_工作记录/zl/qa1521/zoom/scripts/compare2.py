import re, json, unicodedata, difflib, os, sys
SP='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/'
Z=SP+'zl/qa1521/zoom/'
ocr=json.load(open(Z+'ocr_results2.json',encoding='utf-8'))
db=json.load(open(SP+'db/zl_raw.json',encoding='utf-8'))
by={r['id']:r for r in db}
h=open(SP+'zl/out/zl_d15-21.html',encoding='utf-8').read()
body=h[h.find('<body'):]
sets=re.split(r'<section class="set">', body)[1:]
items=[]
for s in sets:
    t=re.search(r'<span class="t">第 (\d+) 套', s).group(1)
    sec=None
    for m in re.finditer(r'<div class="mat-h">(.*?)</div>|<img class="chunk" src="file://([^"]+)"|<div class="q"><span class="no">(\d+)</span><img class="qi" src="file://([^"]+)"', s):
        if m.group(1): sec=m.group(1)[:3]
        elif m.group(2): items.append((t,sec,'M',None,m.group(2)))
        else: items.append((t,sec,'Q',m.group(3),m.group(4)))
cache={}
def lines_for(qfile):
    if qfile in cache: return cache[qfile]
    for c in [SP+'lines/'+os.path.basename(qfile)+'.json', qfile+'.json']:
        if os.path.exists(c):
            cache[qfile]=json.load(open(c,encoding='utf-8')); return cache[qfile]
    cache[qfile]=None; return None
def region_lines(rid, regions):
    L=lines_for(by[rid]['qfile']); out=[]
    for pg,(t,b) in sorted(regions.items(), key=lambda x:int(x[0])):
        P=[p for p in L['pages'] if p['page']==int(pg)][0]
        for l in sorted(P['lines'],key=lambda l:(l['top'],l['x0'])):
            c=(l['top']+l['bottom'])/2
            if t<=c<=b: out.append(l['text'])
    return out
def norm(s):
    s=unicodedata.normalize('NFKC',s)
    s=re.sub(r'\s+','',s)
    s=s.replace('～','~').replace('〜','~').replace('—','-').replace('－','-').replace('–','-').replace('一','-')
    s=re.sub(r'[“”"‘’\'`·•]','',s)
    return s
def ocr_rows(p):
    o=ocr.get(p)
    if not isinstance(o,list): return None
    o=sorted(o,key=lambda r:(r['y0'],r['x0']))
    rows=[]
    for r in o:
        cy=(r['y0']+r['y1'])/2
        if rows and abs(rows[-1]['cy']-cy)<14:
            rows[-1]['items'].append(r); continue
        rows.append({'cy':cy,'items':[r]})
    out=[]
    for row in rows:
        its=sorted(row['items'],key=lambda r:r['x0'])
        out.append(dict(cy=row['cy'],t=' '.join(i['t'] for i in its),x0=min(i['x0'] for i in its),y0=min(i['y0'] for i in its),y1=max(i['y1'] for i in its)))
    return out
def present(n, hay):
    if len(n)<2: return True
    sm=difflib.SequenceMatcher(None,hay,n,autojunk=False)
    mb=sm.find_longest_match(0,len(hay),0,len(n))
    if mb.size>=max(2,int(len(n)*0.6)): return True
    # windowed ratio
    best=0
    for i in range(0,max(1,len(hay)-len(n)+1),max(1,len(n)//4)):
        r=difflib.SequenceMatcher(None,hay[i:i+len(n)+4],n,autojunk=False).ratio()
        best=max(best,r)
        if best>=0.6: return True
    return False
JUNK=re.compile(r'粉笔|模考|本试卷|生成|第\s*\d+\s*页|共\s*\d+\s*页|资料分析|根据以下资料|回答\s*\d+|正确答案|解析|答案|考点|易错|正确率|第[一二三四五六]部分|^\s*材料\s*$|材料\s*\d|^\s*-\s*\d+\s*-\s*$|行测|公务员|真题|www|http|微信|扫码|二维码')
QNUM=re.compile(r'^\s*\d{1,3}\s*[、.．,，]\s*\D')
qrep={}; mats={}
for st,sec,kind,no,p in items:
    f=p.split('/')[-1]
    rows=ocr_rows(p)
    if rows is None:
        print('NO OCR',st,sec,kind,no,f); continue
    notes=[]
    for r in rows:
        if JUNK.search(r['t']): notes.append('JUNK? y=%d "%s"'%(r['cy'],r['t'][:50]))
    hay=norm(''.join(r['t'] for r in rows))
    if kind=='Q':
        rid=re.match(r'(.+?)_q\.png',f).group(1)
        ref=region_lines(rid, by[rid]['regions'])
        if ref: ref[0]=re.sub(r'^\s*\d{1,3}\s*[、.．]\s*','',ref[0])
        if rows and QNUM.match(rows[0]['t']): notes.append('STRAY QNUM? first row "%s"'%rows[0]['t'][:30])
        if rows and re.match(r'^\s*\d{1,3}\s*$', rows[0]['t']): notes.append('STRAY NUMBER ROW? "%s"'%rows[0]['t'])
        for rl in ref:
            n=norm(rl)
            if not present(n,hay): notes.append('MISSING REF LINE "%s"'%rl.strip()[:60])
        # extra OCR rows not in ref
        refn=norm(''.join(ref))
        for r in rows:
            n=norm(r['t'])
            if len(n)>=3 and not present(n,refn): notes.append('EXTRA OCR ROW y=%d "%s"'%(r['cy'],r['t'][:50]))
        ntxt=unicodedata.normalize('NFKC',' '.join(r['t'] for r in rows))
        labs=re.findall(r'(?:^|[\s,，;；:：。?？)）])([A-D])\s*[、.．,，]',' '+ntxt)
        from collections import Counter
        cc=Counter(labs)
        if set(cc)!=set('ABCD'): notes.append('OPTION LABELS FOUND %s (raw: %s)'%(''.join(sorted(cc)),''.join(labs)))
        dup=[k for k,v in cc.items() if v>1]
        if dup: notes.append('DUPLICATE OPTION LABELS %s (raw: %s)'%(''.join(sorted(dup)),''.join(labs)))
        if notes:
            print('##',st,sec,'Q'+no,f); [print('    ',x) for x in notes]
    else:
        m=re.match(r'(.+?)_(p\d+)(_t)?\.png',f); rid=m.group(1)
        mats.setdefault((st,sec,rid),[]).append((f,rows,notes))
for (st,sec,rid),chunks in mats.items():
    ref=region_lines(rid, by[rid]['stem_regions'])
    hay=norm(''.join(r['t'] for f,rows,n in chunks for r in rows))
    notes=[]
    for f,rows,n in chunks:
        for x in n: notes.append(f+' '+x)
        if rows: notes.append('%s first row: "%s"'%(f,rows[0]['t'][:40]))
    for rl in ref:
        nn=norm(rl)
        if not present(nn,hay): notes.append('MISSING REF LINE "%s"'%rl.strip()[:60])
    allrows=[norm(r['t']) for f,rows,n in chunks for r in rows]
    from collections import Counter
    cc=Counter([x for x in allrows if len(x)>=10])
    for k,v in cc.items():
        if v>1: notes.append('DUPLICATE ROW x%d "%s"'%(v,k[:40]))
    print('## MAT',st,sec,rid); [print('    ',x) for x in notes]
