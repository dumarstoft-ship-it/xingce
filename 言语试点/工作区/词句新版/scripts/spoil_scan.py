"""剧透与跨篇重复扫描：python3 -I spoil_scan.py <data.json> <M*.json ...>
同一篇里，前面题的说明或选项含后面题挖掉的原文（短空整词，长空任一 4 字片段），且这段字在考生读到那条说明时全文露出的部分里（前面的题已揭开）没出现过，就列出来。
另列出在不止一篇里当正确项的原文。"""
import json, sys, collections
data = {a['id']: a for a in json.load(open(sys.argv[1]))}
def ptext(a, p): return ''.join(x.get('t', x.get('m', '')) for x in data[a]['paras'][p - 1])
ans = collections.defaultdict(list)
for f in sys.argv[2:]:
    name = f.split('/')[-1]
    for art in json.load(open(f))['articles']:
        aid = art['id']; qs = []
        for q in art['questions']:
            t = ptext(aid, q['p']); b0 = q['blanks'][0]
            qs.append(((q['p'], t.index(b0.get('pre', '') + b0['s'])), q))
        qs.sort(key=lambda x: x[0])
        masked = [ptext(aid, p) for p in range(1, len(data[aid]['paras']) + 1)]
        spans = []
        for _, q in qs:
            t = ptext(aid, q['p']); ss = []
            for b in q['blanks']:
                k = t.index(b.get('pre', '') + b['s']) + len(b.get('pre', ''))
                ss.append((k, k + len(b['s'])))
            spans.append((q['p'], ss))
        def visible_after(i):
            # 第 i 题（从 0 起）答完时露出的全文：它和前面的题已揭开，后面的题还遮着
            m = list(masked)
            for p, ss in spans[i + 1:]:
                t = m[p - 1]
                for b0, e0 in ss: t = t[:b0] + '＿' * (e0 - b0) + t[e0:]
                m[p - 1] = t
            return '\n'.join(m)
        vis_at = [visible_after(i) for i in range(len(qs))]
        for j, (_, qj) in enumerate(qs):
            for b in qj['blanks']:
                s = b['s']; ans[s].append((name, aid, j + 1))
                grams = {s} if len(s) < 6 else {s[k:k + 4] for k in range(len(s) - 3)}
                for i in range(j):
                    qi = qs[i][1]; txt = qi['note'] + '|' + '|'.join(qi['options'])
                    hit = [g for g in grams if len(g) >= 2 and g in txt and g not in vis_at[i]]
                    if hit: print(f"剧透？{name} {aid} 第{i+1}题的说明或选项含第{j+1}题的原文片段 {hit[:3]}（原文：{s[:30]}）")
dup = {s: v for s, v in ans.items() if len({x[1] for x in v}) > 1}
for s, v in dup.items(): print('跨篇重复：', s, v)
print('扫描完毕')
