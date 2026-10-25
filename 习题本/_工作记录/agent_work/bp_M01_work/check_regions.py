import json,ast,re
S='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
JUNK = re.compile(r'本试卷由粉笔用户|认准淘宝|通关达人|TB：|TB:|Seeyee|淘宝店铺|获取持续更新|获取试卷更新|微信|公众号|QQ群|免费获取|考公资料|hijoe|^\s*-?\d+-?\s*$|^\s*\d+\s*/\s*\d+\s*$|第\s*\d+\s*页|网友回忆版）\s*$')
db={r['id']:r for r in json.load(open(S+'/db/real_raw.json'))}
m=json.load(open(S+'/tasks_in/M01.json'))
NEXTQ=re.compile(r'^\s*\d{1,3}\s*[、.．]')
for r in m['real']:
    i=r['id']; d=db[i]
    for kind,fkey,rkey in [('q','qfile','regions'),('j','jfile','jiexi_regions')]:
        reg=d.get(rkey); 
        if not reg: continue
        reg=ast.literal_eval(reg) if isinstance(reg,str) else reg
        if not reg: continue
        try: L=json.load(open(S+'/lines/'+d[fkey]+'.json'))
        except Exception as e: print(i,kind,'nolines',e); continue
        pages=sorted(reg,key=int)
        for k,pg in enumerate(pages):
            a,b=reg[pg]; p=L['pages'][int(pg)-1]
            lines=[l for l in p['lines'] if not JUNK.search(l['text'])]
            if k>0:
                pre=[l for l in lines if l['bottom']<=a+1 and l['top']>=0]
                if pre: print(i,kind,'p',pg,'MISSED-TOP', [(round(l['top'],1),l['text'][:40]) for l in pre])
            # lines after bottom
            post=[l for l in lines if l['top']>=b-1]
            if post:
                nxt=post[0]
                if not NEXTQ.match(nxt['text']) and (k==len(pages)-1):
                    print(i,kind,'p',pg,'AFTER-BOTTOM', round(b,1), [(round(l['top'],1),l['text'][:50]) for l in post[:2]])
