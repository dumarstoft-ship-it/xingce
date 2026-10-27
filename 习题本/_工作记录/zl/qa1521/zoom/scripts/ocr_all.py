import re, json, sys, os
from multiprocessing import Pool
HTML='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/out/zl_d15-21.html'
OUT='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/qa1521/zoom/ocr_results2.json'
h=open(HTML,encoding='utf-8').read()
files=[]
for m in re.finditer(r'src="file://([^"]+\.png)"', h):
    p=m.group(1)
    if p not in files: files.append(p)
eng=None
def init():
    global eng
    from rapidocr_onnxruntime import RapidOCR
    eng=RapidOCR()
def work(p):
    try:
        import numpy as np
        from PIL import Image, ImageOps
        im=Image.open(p).convert('RGB')
        pad=ImageOps.expand(im,border=(60,150,60,150),fill=(255,255,255))
        res,_=eng(np.array(pad))
        out=[]
        for r in (res or []):
            box=r[0]
            out.append({'x0':min(b[0] for b in box)-60,'y0':min(b[1] for b in box)-150,'x1':max(b[0] for b in box)-60,'y1':max(b[1] for b in box)-150,'t':r[1],'c':float(r[2])})
        return p,out
    except Exception as e:
        return p,{'err':str(e)}
if __name__=='__main__':
    print(len(files), flush=True)
    res={}
    with Pool(4, initializer=init) as pool:
        for i,(p,o) in enumerate(pool.imap_unordered(work, files)):
            res[p]=o
            if i%20==0:
                print(i, flush=True)
                json.dump(res, open(OUT,'w'), ensure_ascii=False)
    json.dump(res, open(OUT,'w'), ensure_ascii=False)
    print('done', flush=True)
