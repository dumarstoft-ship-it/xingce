import re, json, unicodedata, difflib, os
from collections import Counter
exec(open('/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/qa1521/zoom/scripts/compare3.py').read().split("mats={}")[0])
rows=[]
for st,sec,kind,no,p in items:
    if kind!='Q': continue
    f=p.split('/')[-1]
    B=ocr[p]
    rid=re.match(r'(.+?)_q\.png',f).group(1)
    ref=region_lines(rid, by[rid]['regions'])
    tb=[b for b in B if b['h']>=10 and not b.get('note')]
    gb=[b for b in B if b.get('note')]
    tiny=[b for b in B if b['h']<10]
    first=(B[0].get('t') or '<None>') if B else ''
    # ref lines that are pure option labels (image options) e.g. "A."
    reftext=[r for r in ref]
    flag=''
    if len(tb)!=len(reftext): flag='COUNT bands=%d ref=%d graphic=%d'%(len(tb),len(reftext),len(gb))
    rows.append((st,sec,no,f,flag,first[:60],[b['h'] for b in tiny]))
for r in rows:
    print(r[0],r[1],'Q%s'%r[2],r[3],'|',r[5],'|',r[4],('tiny:%s'%r[6] if r[6] else ''))
