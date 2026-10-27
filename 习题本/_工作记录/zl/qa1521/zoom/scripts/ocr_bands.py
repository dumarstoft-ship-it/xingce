import re, json, sys
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageOps
HTML='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/out/zl_d15-21.html'
OUT='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/qa1521/zoom/ocr_bands.json'
h=open(HTML,encoding='utf-8').read()
files=[]
for m in re.finditer(r'src="file://([^"]+\.png)"', h):
    if m.group(1) not in files: files.append(m.group(1))
eng=None
def init():
    global eng
    from rapidocr_onnxruntime import RapidOCR
    eng=RapidOCR()
def bands(a, thr=200, mingap=3):
    ink=(a<thr).sum(axis=1)>0
    out=[];s=None
    for i,v in enumerate(ink):
        if v and s is None: s=i
        if not v and s is not None: out.append([s,i-1]); s=None
    if s is not None: out.append([s,len(ink)-1])
    m=[]
    for b in out:
        if m and b[0]-m[-1][1]<=mingap: m[-1][1]=b[1]
        else: m.append(b)
    return m
def rec(img):
    res,_=eng(np.array(img.convert('RGB')),use_det=False,use_cls=False,use_rec=True)
    if res: return res[0][1], float(res[0][2])
    return None, 0.0
def work(p):
    try:
        im=Image.open(p).convert('L'); a=np.array(im)
        out=[]
        for s,e in bands(a):
            h=e-s+1
            sub=a[s:e+1]
            cols=np.where((sub<200).any(axis=0))[0]
            x0,x1=int(cols[0]),int(cols[-1])
            item={'y0':s,'y1':e,'x0':x0,'x1':x1,'h':h}
            if h>70:
                item['t']=None; item['note']='tall band (graphic?)'
                out.append(item); continue
            band=im.crop((max(0,x0-4),max(0,s-3),min(im.width,x1+5),min(im.height,e+4)))
            band=ImageOps.expand(band,border=(10,6,10,6),fill=255)
            t,c=rec(band)
            if t is None and (x1-x0)>600:
                # split in halves at a whitespace column near middle
                colink=(sub<200).any(axis=0)
                mid=(x0+x1)//2; cut=None
                for d in range(0,(x1-x0)//2):
                    for c2 in (mid-d,mid+d):
                        if x0<c2<x1 and not colink[c2-2:c2+3].any(): cut=c2; break
                    if cut: break
                if cut:
                    t1,c1=rec(ImageOps.expand(im.crop((x0,s,cut,e+1)),border=(10,6,10,6),fill=255))
                    t2,c2_=rec(ImageOps.expand(im.crop((cut,s,x1+1,e+1)),border=(10,6,10,6),fill=255))
                    t=(t1 or '')+' '+(t2 or ''); c=min(c1,c2_)
            item['t']=t; item['c']=c
            out.append(item)
        return p,out
    except Exception as ex:
        return p,{'err':repr(ex)}
if __name__=='__main__':
    print(len(files), flush=True)
    res={}
    with Pool(4, initializer=init) as pool:
        for i,(p,o) in enumerate(pool.imap_unordered(work, files)):
            res[p]=o
            if i%25==0: print(i, flush=True)
    json.dump(res, open(OUT,'w'), ensure_ascii=False)
    print('done', flush=True)
