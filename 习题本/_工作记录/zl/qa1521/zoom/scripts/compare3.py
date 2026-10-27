import re, json, unicodedata, difflib, os
from collections import Counter
SP='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/'
Z=SP+'zl/qa1521/zoom/'
ocr=json.load(open(Z+'ocr_bands.json',encoding='utf-8'))
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
    s=unicodedata.normalize('NFKC',s or '')
    s=re.sub(r'\s+','',s)
    for a,b in [('～','~'),('〜','~'),('—','-'),('－','-'),('–','-'),('一','-'),('，',','),('。','.'),('：',':'),('；',';'),('（','('),('）',')')]:
        s=s.replace(a,b)
    s=re.sub(r'[“”"‘’\'`·•]','',s)
    return s
def best(n, cands):
    b=0;bi=-1
    for i,c in enumerate(cands):
        r=difflib.SequenceMatcher(None,n,c,autojunk=False).ratio()
        if r>b: b=r;bi=i
    return b,bi
JUNK=re.compile(r'粉笔|模考|本试卷|生成|第\s*\d+\s*页|共\s*\d+\s*页|资料分析|根据以下资料|根据下列资料|回答\s*\d+|正确答案|解析|答案|考点|易错|正确率|第[一二三四五六]部分|^\s*材料\s*$|材料\s*\d|^\s*-\s*\d+\s*-\s*$|行测|公务员|真题|www|http|微信|扫码|二维码')
QNUM=re.compile(r'^\s*\d{1,3}\s*[、.．,，]\s*(?![\d%])')
mats={}
for st,sec,kind,no,p in items:
    f=p.split('/')[-1]
    B=ocr.get(p)
    if not isinstance(B,list): print('NO OCR',f,B); continue
    texts=[b for b in B if b.get('t')]
    notes=[]
    for b in texts:
        if JUNK.search(b['t']): notes.append('JUNK? y=%d "%s"'%(b['y0'],b['t'][:50]))
    if kind=='Q':
        rid=re.match(r'(.+?)_q\.png',f).group(1)
        ref=region_lines(rid, by[rid]['regions'])
        ref0=ref[0] if ref else ''
        if ref: ref[0]=re.sub(r'^\s*\d{1,3}\s*[、.．]\s*','',ref[0])
        if texts and QNUM.match(texts[0]['t']) and not QNUM.match(ref[0] if ref else ''):
            notes.append('STRAY QNUM? first band "%s"'%texts[0]['t'][:30])
        bn=[norm(b['t']) for b in texts]
        for rl in ref:
            n=norm(rl)
            if len(n)<2: continue
            r,i=best(n,bn)
            if r<0.5:
                # maybe band merges two ref lines; check containment
                joined=''.join(bn)
                sm=difflib.SequenceMatcher(None,joined,n,autojunk=False).find_longest_match(0,len(joined),0,len(n))
                if sm.size < len(n)*0.6: notes.append('MISSING REF LINE (best %.2f) "%s"'%(r,rl.strip()[:60]))
        rn=[norm(x) for x in ref]
        joinedref=''.join(rn)
        for b,n in zip(texts,bn):
            if len(n)<3: continue
            r,i=best(n,rn)
            if r<0.5:
                sm=difflib.SequenceMatcher(None,joinedref,n,autojunk=False).find_longest_match(0,len(joinedref),0,len(n))
                if sm.size < len(n)*0.6: notes.append('EXTRA BAND (best %.2f) y=%d "%s"'%(r,b['y0'],b['t'][:50]))
        ntxt=unicodedata.normalize('NFKC',' '.join(b['t'] for b in texts))
        labs=re.findall(r'(?<![A-Za-z])([A-D])\s*[、.．,，](?![A-Za-z])',ntxt)
        cc=Counter(labs)
        if set(cc)!=set('ABCD'): notes.append('OPTION LABELS %s'%(''.join(labs)))
        if any(v>1 for v in cc.values()): notes.append('DUP OPTION LABELS %s'%(''.join(labs)))
        tall=[b for b in B if not b.get('t') and b.get('note')]
        if notes:
            print('##',st,sec,'Q'+no,f,'(bands %d, ref lines %d, graphic bands %d)'%(len(B),len(ref),len(tall))); [print('    ',x) for x in notes]
    else:
        m=re.match(r'(.+?)_(p\d+)(_t)?\.png',f); rid=m.group(1)
        mats.setdefault((st,sec,rid),[]).append((f,B,notes))
print('==================== MATERIALS')
for (st,sec,rid),chunks in mats.items():
    ref=region_lines(rid, by[rid]['stem_regions'])
    bn=[norm(b['t']) for f,B,n in chunks for b in B if b.get('t')]
    joined=''.join(bn)
    notes=[]
    for f,B,n in chunks:
        for x in n: notes.append(f+' '+x)
        tb=[b for b in B if b.get('t')]
        if tb: notes.append('%s first band: "%s" | last band: "%s"'%(f,tb[0]['t'][:30],tb[-1]['t'][-30:]))
    for rl in ref:
        nn=norm(rl)
        if len(nn)<2: continue
        r,i=best(nn,bn)
        if r<0.5:
            sm=difflib.SequenceMatcher(None,joined,nn,autojunk=False).find_longest_match(0,len(joined),0,len(nn))
            if sm.size < len(nn)*0.6: notes.append('MISSING REF LINE (best %.2f) "%s"'%(r,rl.strip()[:60]))
    cc=Counter([x for x in bn if len(x)>=10])
    for k,v in cc.items():
        if v>1: notes.append('DUPLICATE BAND x%d "%s"'%(v,k[:40]))
    print('## MAT',st,sec,rid); [print('    ',x) for x in notes]
