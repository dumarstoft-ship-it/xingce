import json, re, sys
SP='/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
d=json.load(open(SP+'/db/real_raw.json'))
ex=json.load(open(SP+'/teacher/examples.json'))
b=[e for e in ex if 'T124'<=e['tid']<='T175']
def norm(s):
    s=re.sub(r'[\s　，。、；：？！“”‘’（）()\[\]【】,.;:?!"\'<>《》\-—…·]','',s or '')
    return s
def grams(s,n=3):
    s=norm(s)
    return set(s[i:i+n] for i in range(len(s)-n+1))
bank=[(x['id'],grams(x['text'][:300])) for x in d if x.get('section')=='数量关系' or True]
for e in b:
    q=e['question'] or ''
    q=re.sub(r'^（[^）]*）','',q)
    g=grams(q[:200])
    if not g: continue
    sc=[]
    for bid,bg in bank:
        if not bg: continue
        inter=len(g&bg)
        sc.append((inter/len(g),bid))
    sc.sort(reverse=True)
    print(e['tid'], e['source'], 'db=',e['db_match'], [(round(s,2),i) for s,i in sc[:3]])
