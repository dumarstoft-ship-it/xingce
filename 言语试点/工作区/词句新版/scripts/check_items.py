"""检查广东式政治常识题：格式、答案、依据原话能否在原文或已核原话里逐字找到。
用法：python3 -I check_items.py <结果.json> <base data.json> [其他已核原话文件 ...]"""
import json, sys, re
res = json.load(open(sys.argv[1], encoding='utf-8'))
data = json.load(open(sys.argv[2], encoding='utf-8'))
by = {a['id']: a for a in data}
verified = [j['source_quote'] for a in data for j in a.get('judgments', [])]
for f in sys.argv[3:]:                      # 其他核过官方页面的文件（如一文多题答案），整篇当作已核原话来源
    verified.append(open(f, encoding='utf-8').read())
def norm(s):
    return re.sub(r'[\s“”"‘’\'「」『』…·]', '', s)
vn = [norm(v) for v in verified]
bad = weak = 0
for art in res['articles']:
    a = by[art['id']]
    text = ''.join(x.get('t', x.get('m', '')) for p in a['paras'] for x in p)
    tn = norm(text)
    for ii, it in enumerate(art['items']):
        tag = f"{art['id']} 第{ii+1}题（{it.get('type')}）"
        err = []
        t = it.get('type')
        if t not in ('判断', '单选', '多选'): err.append('题型')
        if it.get('area') not in ('政治理论', '常识'): err.append('area')
        if t == '判断' and not isinstance(it.get('answer'), bool): err.append('判断题答案要是 true/false')
        if t in ('单选', '多选'):
            if len(it.get('options', [])) != 4: err.append('选项数')
            ans = it.get('answer')
            if t == '单选' and ans not in list('ABCD'): err.append('单选答案')
            if t == '多选' and (not isinstance(ans, list) or not ans or any(x not in 'ABCD' for x in ans)): err.append('多选答案')
        srcs = it.get('sources', [])
        if not srcs: err.append('没有依据')
        kinds = set()
        for s in srcs:
            k, q = s.get('kind'), norm(s.get('quote', ''))
            kinds.add(k)
            if k == '原文' and q and q not in tn: err.append('原文依据在文章里找不到：' + s.get('quote', '')[:40])
            if k == '已核原话' and q and not any(q in v for v in vn): err.append('已核原话对不上：' + s.get('quote', '')[:40])
        if kinds and kinds <= {'搜索佐证'}:
            weak += 1; print(tag, '只有搜索佐证')
        if err:
            bad += 1; print(tag, '；'.join(err))
    print(art['id'], len(art['items']), '题')
print('有问题：', bad, '；只有搜索佐证：', weak)
