"""Build gen/D06_math_h.json (needs #1-#5 of harden/D06_decision.json new_variants) and run format checks."""
import json, re, sys

S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
OUT = S + '/gen/D06_math_h.json'

G1 = '考法一：古典概率·组合直算（恰有/都是与反求总数）'
G2 = '考法二：对立事件（至少·既有又有·正难则反）'
G8 = '考法八：独立重复试验（n 次恰 k 次）'
G9 = '考法九：分类分步·多阶段流程（评审·闯关·状态转移）'

V = [
    dict(
        vid='D06-math-h-v01', group=G1, seed='考法一', direction='拓展',
        kaofa='配对问题：恰好成一双', technique='先选双、再选只', difficulty=3, time_s=75,
        stem='某街道应急物资仓库盘点时发现，5 双款式各不相同的防护手套被拆散后混放在同一个箱子里，共 10 只。'
             '仓管员从箱中随机取出 4 只，取出的 4 只中恰好有 2 只能配成一双、另外 2 只配不成双的概率为（ ）。',
        options={'A': r'$\frac{1}{7}$', 'B': r'$\frac{4}{7}$', 'C': r'$\frac{13}{21}$', 'D': r'$\frac{2}{3}$'},
        answer='B',
        jiexi='卡点：“恰好一双”要先选双、再选只，另 2 只才不会再成双。成双的一双 5 种；另 2 只取自其余 4 双中的 2 双 $C_4^2=6$，每双再选左或右 $2^2=4$，共 120 种；总数 $C_{10}^4=210$，概率 $\\frac47$，选 B。易错：成双后从剩下 8 只任取 2 只，$5C_8^2=140$，混进了“两双”的取法且各算了两次，得 $\\frac23$（D）；漏乘 $2^2$ 得 $\\frac17$（A）；求成“至少一双”得 $\\frac{13}{21}$（C）。',
    ),
    dict(
        vid='D06-math-h-v02', group=G2, seed='考法二', direction='深化',
        kaofa='三方两两有重合：反面容斥', technique='取反后容斥，固定共用者', difficulty=3, time_s=90,
        stem='某区公布了 5 个红色教育研学基地，甲、乙、丙三所中学各自从中随机选定 2 个组织学生参观，三校的选择互不影响。'
             '任意两所学校选定的基地都至少有一个相同的概率为（ ）。',
        # 选项按"轮转升序"排列（同 2024GK-74 的排法），让答案落在 D，保持本批答案分布
        options={'A': '63%', 'B': '10%', 'C': '34.3%', 'D': '37%'},
        answer='D',
        jiexi=r'卡点：反面“至少一对完全错开”中三对事件不独立，必须容斥。某对错开：固定一校，另一校 2 个都在另 3 个中，'
              r'$\frac{C_3^2}{C_5^2}=0.3$，3 对共 0.9；两对同时错开必共用一校，固定它，另两校都在另 3 个中，$0.3^2=0.09$，'
              r'3 种共 0.27；三对都错开需 6 个基地，不可能。反面 0.9−0.27=0.63，所求 37%，选 D。'
              r'易错：容斥漏了加回得 1−0.9=10%（B）；当作三对独立得 $0.7^3=34.3\%$（C）；忘了取反得 63%（A）。',
    ),
    dict(
        vid='D06-math-h-v03', group=G8, seed='考法八', direction='深化',
        kaofa='两人命中次数比较', technique='列分布，按一人分类', difficulty=2, time_s=75,
        stem='某区机关职工篮球赛中场设有罚球挑战：甲、乙两名队员各罚球 2 次，甲每次罚中的概率为 0.6，乙每次罚中的概率为 0.5，'
             '各次罚球结果相互独立。甲罚中的次数比乙多的概率为（ ）。',
        options={'A': '27%', 'B': '33%', 'C': '39%', 'D': '76%'},
        answer='C',
        jiexi='卡点：两人比较，先各列命中 0、1、2 次的分布，再按甲分类、乙取“比甲少”的累计。甲：0.16、0.48、0.36（中 1 次有两种顺序）；乙：0.25、0.5、0.25。甲中 1 次且乙 0 次：$0.48\\times0.25=0.12$；甲中 2 次且乙不超过 1 次：$0.36\\times0.75=0.27$；合计 39%，选 C。易错：甲中 1 次漏乘 2，得 33%（B）；只算甲中 2 次，得 27%（A）；把“多于”算成“不少于”，加上平局 37%，得 76%（D）。',
    ),
    dict(
        vid='D06-math-h-v04', group=G8, seed='考法八', direction='拓展',
        kaofa='停止规则：末次必成功', technique='末次锁定再排前3次', difficulty=3, time_s=60,
        stem='某市 12345 政务服务便民热线对已办结的工单进行电话回访：回访员按名单依次给市民打电话，每次拨打能接通的概率均为 0.6，'
             '各次是否接通相互独立；累计接通 2 位市民，本轮回访即告完成。回访员恰好拨打 4 次完成本轮回访的概率为（ ）。',
        options={'A': '17.28%', 'B': '28.80%', 'C': '34.56%', 'D': '82.08%'},
        answer='A',
        jiexi='卡点：“恰好第 4 次完成”⇔第 4 次接通且前 3 次恰接通 1 次：$C_3^1\\times0.6\\times0.4^2\\times0.6=17.28\\%$，选 A。易错：套“4 次中恰 2 次”得 $C_4^2\\times0.6^2\\times0.4^2=34.56\\%$（C），混进了第 2、3 次就已完成的情况；漏乘第 4 次的 0.6 得 28.80%（B）；求成“4 次以内完成”得 82.08%（D）。对照比赛题的“打满”：问谁赢可以打满，问第几次结束不能打满，最后一次必须成功。',
    ),
    dict(
        vid='D06-math-h-v05', group=G9, seed='考法九', direction='深化',
        kaofa='流程树＋已知结果反推', technique='缩小样本空间＋约去', difficulty=3, time_s=70,
        stem='某区面向社会征集“口袋公园”设计方案。每份方案先参加初评，初评通过的概率为 40%；初评未通过的方案均修改后参加 1 次复评，'
             '复评通过的概率为 30%；初评或复评通过的方案进入终评，在终评中被采纳的概率均为 50%。已知某份方案最终被采纳，'
             '则它是经复评才进入终评的概率为（ ）。',
        options={'A': r'$\frac{9}{50}$', 'B': r'$\frac{9}{29}$', 'C': r'$\frac{3}{7}$', 'D': r'$\frac{9}{20}$'},
        answer='B',
        jiexi='卡点：由结果反推来路要缩小样本空间，只在“被采纳”的方案里看经复评的占比；终评对两条路径都是 50%，可约去。直接过初评 0.4，经复评通过 $0.6\\times0.3=0.18$，所求 $\\frac{0.18}{0.58}=\\frac{9}{29}$，选 B。易错：不缩小样本空间，答 $0.18=\\frac{9}{50}$（A）；漏乘“初评未通过”的 0.6，得 0.3÷0.7=$\\frac37$（C）；只除以另一条路径，得 0.18÷0.4=$\\frac{9}{20}$（D）。',
    ),
]

KEYS = ['vid', 'group', 'seed', 'direction', 'kaofa', 'technique', 'difficulty', 'time_s', 'stem', 'options', 'answer', 'jiexi',
        'figure_svg', 'verify']
HINT_WORDS = ['对立', '反面', '正难则反', '条件概率', '贝叶斯', '二项', '独立重复', '捆绑', '插空', '打满', '跟屁虫', '全概率', '加权',
              '样本空间', '本题', '改编', '真题', '利用', '技巧', '公式', '考法', '【']

recs, bad = [], 0
for v in V:
    v['figure_svg'] = None
    v['verify'] = f"verify/{v['vid']}.py"
    recs.append({k: v[k] for k in KEYS})
    j, st = v['jiexi'], v['stem']
    probs = []
    if len(j) > 250: probs.append(f'jiexi too long {len(j)}')
    if '用时' in j: probs.append('jiexi mentions 用时')
    if not st.endswith('（ ）。'): probs.append('stem ending')
    if len(v['kaofa']) > 20: probs.append('kaofa > 20')
    if len(v['technique']) > 12: probs.append('technique > 12')
    for w in HINT_WORDS:
        if w in st or any(w in o for o in v['options'].values()): probs.append('hint word in stem/options: ' + w)
    if f"选 {v['answer']}" not in j: probs.append('jiexi does not state the keyed answer')
    for L in 'ABCD':
        if L != v['answer'] and f'（{L}）' not in j: probs.append(f'distractor {L} not explained')
    if j.count('$') % 2 or st.count('$') % 2: probs.append('unbalanced $')
    bad += len(probs)
    print(v['vid'], v['answer'], 'jiexi', len(j), 'stem', len(st), probs or 'ok')

json.dump(recs, open(OUT, 'w'), ensure_ascii=False, indent=1)
print('wrote', OUT, len(recs), 'answers', ''.join(r['answer'] for r in recs), 'problems', bad)
sys.exit(1 if bad else 0)
