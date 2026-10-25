import re, os, sys, glob, json
D = sys.argv[1]
head_re = re.compile(r'^\s*(?:第[一二三四五六七八]部分|[一二三四五六七八]\s*[\.、．])\s*(政治理论|常识判断|言语理解|数量关系|判断推理|科学推理|资料分析)')
qre = re.compile(r'^\s*(\d{1,3})\s*[\.、．]')
def split_questions(lines):
    qs = []; cur = None
    for l in lines:
        m = qre.match(l)
        if m:
            n = int(m.group(1))
            if cur is None or (n > cur[0] and n - cur[0] < 4):
                cur = [n, [l]]; qs.append(cur); continue
        if cur is not None: cur[1].append(l)
    return [(n, '\n'.join(b)) for n,b in qs]
def cls_judge(t):
    s = re.sub(r'\s+','',t)
    if re.search(r'图形|所给图|折叠|拼接|拼合|视图|截面|立体|展开图|问号处|呈现一定的规律|规律性|左边给定|外表面', s) and not re.search(r'定义', s):
        return '图推'
    if re.search(r'根据(上述|以上|题干)?.{0,6}定义|符合.{0,10}定义|属于.{0,12}的是|不属于', s) and re.search(r'定义|是指|指的是', s):
        return '定义'
    if re.search(r'逻辑关系最为?(相似|贴近|接近|一致)|依次填入划横线|依次填入画横线|相当于', s) or re.match(r'^\d+[\.、．][^。，？]{0,30}[：:][^。]{0,40}(A|Ａ)[\.、．]', s):
        return '类比'
    # analytic reasoning
    names = len(re.findall(r'甲|乙|丙|丁|戊|己|庚|小[一-龥]', s))
    if re.search(r'已知[:：]|①', s) and re.search(r'分别|各|每人|每个|座位|排名|名次|顺序|相邻|左|右|依次|一一对应|恰好|各不相同|之一', s) and not re.search(r'削弱|加强|支持|质疑|反驳|解释|前提|假设|结构|相似|评价', s):
        return '综合推理'
    if names >= 6 and re.search(r'分别|各|每人|名次|排名|相邻|座位', s) and not re.search(r'削弱|加强|支持|质疑|反驳|解释|前提|假设|结构|相似|评价', s):
        return '综合推理'
    if re.search(r'只有一(句|个|人).{0,6}(真|假)|一真|一假|只有一人说|说了真话|说了假话|为真.{0,4}为假', s):
        return '真假推理'
    return '逻辑'
tot = {}
out = {}
for f in sorted(glob.glob(os.path.join(D,'*.txt'))):
    name = os.path.basename(f)
    if '解析' in name or '答案' in name or '方案' in name: continue
    lines = open(f, encoding='utf-8', errors='ignore').read().split('\n')
    heads = [(i, m.group(1)) for i,l in enumerate(lines) for m in [head_re.match(l)] if m]
    row = {}
    for k,(i,s) in enumerate(heads):
        j = heads[k+1][0] if k+1 < len(heads) else len(lines)
        if s not in ('数量关系','判断推理'): continue
        qs = split_questions(lines[i+1:j])
        if s == '数量关系':
            nr = sum(1 for n,t in qs if re.search(r'^\s*\d+[\.、．]\s*[\d，, ]+[,，]', t.split('\n')[0]) and not re.search(r'[一-龥]{4,}', t.split('\n')[0][4:]))
            row['数字推理?'] = nr
            row['数学运算'] = len(qs) - nr
        else:
            for n,t in qs:
                c = cls_judge(t); row[c] = row.get(c,0)+1
    out[name] = row
    for k,v in row.items(): tot[k] = tot.get(k,0)+v
    print(name[:44].ljust(44), row)
print('TOTAL', tot)
