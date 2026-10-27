import re, json, unicodedata, difflib
SP='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/'
Z=SP+'zl/qa1521/zoom/'
ocr=json.load(open(Z+'ocr_results.json',encoding='utf-8'))
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
def norm(s):
    s=unicodedata.normalize('NFKC',s)
    s=re.sub(r'\s+','',s)
    s=s.replace('～','~').replace('—','-').replace('－','-').replace('–','-')
    s=re.sub(r'[“”"‘’\'`]','',s)
    return s
def ocr_lines(p):
    o=ocr.get(p)
    if not isinstance(o,list): return None
    # group by rows
    o=sorted(o,key=lambda r:(r['y0'],r['x0']))
    rows=[]
    for r in o:
        cy=(r['y0']+r['y1'])/2
        if rows and abs(rows[-1]['cy']-cy)<12:
            rows[-1]['items'].append(r); continue
        rows.append({'cy':cy,'items':[r]})
    out=[]
    for row in rows:
        its=sorted(row['items'],key=lambda r:r['x0'])
        out.append((row['cy'],' '.join(i['t'] for i in its), min(i['x0'] for i in its)))
    return out
JUNK=re.compile(r'粉笔|模考|本试卷|生成|第\s*\d+\s*页|共\s*\d+\s*页|资料分析|根据以下资料|回答\s*\d+|正确答案|解析|答案|考点|易错|正确率|第[一二三四五六]部分|^材料$|^\(?材料\d\)?$|^-\s*\d+\s*-$')
QNUM=re.compile(r'^\s*\d{2,3}\s*[、.．,，]')
rep=[]
for st,sec,kind,no,p in items:
    f=p.split('/')[-1]
    L=ocr_lines(p)
    if L is None: rep.append((st,sec,kind,no,f,'NO OCR')); continue
    txt=''.join(l[1] for l in L)
    notes=[]
    for cy,lt,x0 in L:
        if JUNK.search(lt): notes.append('JUNK? y=%d "%s"'%(cy,lt[:40]))
    if kind=='Q':
        rid=re.match(r'(.+?)_q\.png',f).group(1)
        ref=by[rid]['text']
        ref1=re.sub(r'^\s*\d{1,3}\s*[、.．]\s*','',ref)
        nr=norm(ref1); no_=norm(txt)
        if L and QNUM.match(L[0][1]): notes.append('STRAY QNUM? first line "%s"'%L[0][1][:30])
        # start/end check
        head_ok = no_[:4]==nr[:4] or difflib.SequenceMatcher(None,no_[:8],nr[:8]).ratio()>0.6
        tail_ok = no_[-4:]==nr[-4:] or difflib.SequenceMatcher(None,no_[-8:],nr[-8:]).ratio()>0.6
        ratio=difflib.SequenceMatcher(None,no_,nr).ratio()
        if not head_ok: notes.append('HEAD MISMATCH ocr="%s" ref="%s"'%(no_[:20],nr[:20]))
        if not tail_ok: notes.append('TAIL MISMATCH ocr="%s" ref="%s"'%(no_[-20:],nr[-20:]))
        if ratio<0.85: notes.append('LOW SIM %.2f'%ratio)
        # check each reference line present
        for rl in ref1.split('\n'):
            n=norm(rl)
            if len(n)<2: continue
            # fuzzy find
            sm=difflib.SequenceMatcher(None,no_,n)
            mb=sm.find_longest_match(0,len(no_),0,len(n))
            if mb.size < max(2, int(len(n)*0.5)):
                notes.append('REF LINE MISSING? "%s"'%n[:40])
        # option letters present
        opts=re.findall(r'(?:^|[^A-Za-z])([A-D])[、.．]',unicodedata.normalize('NFKC',txt))
        if sorted(set(opts))!=['A','B','C','D']: notes.append('OPTIONS FOUND %s'%''.join(sorted(set(opts))))
        if len(opts)>4: notes.append('OPTION LETTERS x%d %s'%(len(opts),''.join(opts)))
    rep.append((st,sec,kind,no,f,notes,L[:1],L[-1:]))
json.dump(rep,open(Z+'compare.json','w'),ensure_ascii=False)
for r in rep:
    if len(r)==6: print(r); continue
    st,sec,kind,no,f,notes,first,last=r
    if notes:
        print('##',st,sec,kind,no,f)
        for n in notes: print('    ',n)
