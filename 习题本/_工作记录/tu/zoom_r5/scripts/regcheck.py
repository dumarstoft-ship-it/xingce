import json, re, os, sys
import pdfplumber
S='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/'
SRC='/home/user/xingce/'
batch=json.load(open(S+'tu/batch_r5.json'))
db={e['id']:e for e in json.load(open(S+'db/real_raw.json')) if isinstance(e,dict) and 'id' in e}
files=os.listdir(SRC)
def findpdf(stem):
    c=[f for f in files if f.endswith('.pdf') and f[:-4]==stem]
    if not c: c=[f for f in files if f.endswith('.pdf') and f.startswith(stem)]
    return SRC+c[0] if c else None
cache={}
def openpdf(p):
    if p not in cache: cache[p]=pdfplumber.open(p)
    return cache[p]
def check(rec, regkey, filekey, label):
    regs=rec.get(regkey) or {}
    stem=rec.get(filekey)
    if not regs or not stem: return [f'{label}: no regions/file']
    p=findpdf(stem)
    if not p: return [f'{label}: pdf not found {stem}']
    pdf=openpdf(p)
    out=[]
    pages=sorted(int(k) for k in regs)
    for i,pg in enumerate(pages):
        y0,y1=regs[str(pg)]
        page=pdf.pages[pg-1]
        for im in page.images:
            t,b=im['top'],im['bottom']
            ov=max(0,min(b,y1)-max(t,y0))/max(1,(b-t))
            if ov<0.9:
                # image partly/not covered; report only if near the region
                near = (b<=y0+2 and y0-b<120) or (t>=y1-2 and t-y1<60) or (0<ov<0.9)
                if near:
                    out.append(f'{label}: p{pg} region[{y0:.0f},{y1:.0f}] image[{t:.0f},{b:.0f}] cov={ov:.2f}')
    # next page after last region page: images at top before first text line
    last=pages[-1]
    if last < len(pdf.pages):
        nxt=pdf.pages[last]  # 0-based index = last -> page last+1
        words=nxt.extract_words()
        ws=[w for w in words if w['top']>40]
        first_text_top=min([w['top'] for w in ws], default=9999)
        tops=[im for im in nxt.images if im['top']<first_text_top]
        if tops:
            out.append(f'{label}: next page p{last+1} has image(s) above first text line ({first_text_top:.0f}): '+', '.join(f'[{im["top"]:.0f},{im["bottom"]:.0f}]' for im in tops))
    return out
for x in batch:
    rec=db.get(x['id'])
    if not rec: print(x['id'],'NOT IN DB'); continue
    res=check(rec,'regions','qfile','Q')+check(rec,'jiexi_regions','jfile','J')
    print(x['id'], 'q', rec.get('regions'), 'j', rec.get('jiexi_regions'))
    for r in res: print('    ',r)
