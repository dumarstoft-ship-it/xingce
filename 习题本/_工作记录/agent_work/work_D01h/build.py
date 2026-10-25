# Build gen/D01_math_h.json (needs 1-6 of harden/D01_decision.json new_variants) with self-checks.
import json, os, re, subprocess, sys
from fractions import Fraction as F
from collections import Counter

S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
OUT = os.path.join(S, 'gen', 'D01_math_h.json')
G2 = '考法二：和差倍链（设一个量表示全部）'
G3 = '考法三：量率对应（分数、百分数与份数）'
G4 = '考法四：三量关系与连比（总量＝个数×均量）'

V = []
V.append(dict(
    vid='D01-math-h-v01', group=G2, seed='考法二', direction='深化',
    kaofa='两个独立假设调动，用总量统一', technique='总数作单位1，分率作差',
    difficulty=2, time_s=70,
    stem='某地铁站旁有甲、乙两个共享单车停放点。运维人员测算发现：若从甲点调35辆到乙点，则乙点的单车数是甲点的3倍；若改为从乙点调40辆到甲点，则甲点的单车数是乙点的2倍。甲点现有共享单车（ ）辆。',
    options={'A': '45', 'B': '59', 'C': '80', 'D': '180'}, answer='C',
    jiexi='卡点：两个“若”都是从现状出发的独立假设，每种假设下两点总数都不变，可把总数看作单位“1”。第一种调后甲点占总数的$\\frac14$，第二种调后占$\\frac23$；两种调后状态的甲点相差35＋40＝75辆，对应$\\frac23-\\frac14=\\frac{5}{12}$，总数180辆，甲点现有180×$\\frac14$＋35＝80辆，选C。列方程组也行但慢。易错：误把两次调整当作先后发生，只用40辆对应$\\frac{5}{12}$，得59，最典型；算出调后的45辆忘了加回35；答成总数180。',
))
V.append(dict(
    vid='D01-math-h-v02', group=G2, seed='2021GK-63', direction='深化',
    kaofa='已知最多与最少之差，先定大小', technique='先假设大小再回代',
    difficulty=3, time_s=90,
    stem='某镇开展助农直播，连续4场直播的订单量有如下关系：第二场比第一场少20%，第三场比前两场之和少30单，第四场比第一场的1.5倍多15单。已知订单量最多的一场比最少的一场多50单，这4场直播共有订单（ ）单。',
    options={'A': '90', 'B': '240', 'C': '342', 'D': '393'}, answer='B',
    jiexi='卡点：哪一场最多取决于第一场的量，不能凭系数大小认定，要先假设、再回代检验。设第一场x单，四场依次为x、0.8x、1.8x−30、1.5x＋15，最少的是第二场。若第三场最多，x−30＝50，x＝80，但此时第三场114单＜第四场135单，矛盾；故第四场最多，0.7x＋15＝50，x＝50，四场为50、40、60、90单，检验成立，共240单，选B。代选项反推x有三项是整数，仍要检验大小。易错：按系数认定第三场最多，得393；照搬“第一场最少、第四场最多”，得342；答成最多一场的90。',
))
V.append(dict(
    vid='D01-math-h-v03', group=G3, seed='考法三', direction='深化',
    kaofa='“占其余之和几分之几”化为占总量', technique='化为占总数的分率',
    difficulty=2, time_s=60,
    stem='某届外贸展会设甲、乙、丙三个展区。甲展区的参展企业数是乙、丙两个展区之和的$\\frac{1}{3}$，乙展区的参展企业数是甲、丙两个展区之和的$\\frac{1}{4}$，丙展区比乙展区多126家参展企业。甲展区有参展企业（ ）家。',
    options={'A': '90', 'B': '198', 'C': '252', 'D': '360'}, answer='A',
    jiexi='卡点：“是其余两者之和的$\\frac13$”要先化成“占总数的$\\frac14$”（1份比3份，共4份）。同理乙占$\\frac15$，丙占$\\frac{11}{20}$，丙比乙多$\\frac{7}{20}$，对应126家，总数360家，甲＝360×$\\frac14$＝90家，选A。易错：把$\\frac13$、$\\frac14$直接当成占总数的比例，丙占$\\frac{5}{12}$，126家对应$\\frac16$，得甲252家，最典型；答成丙198家或总数360家。',
))
V.append(dict(
    vid='D01-math-h-v04', group=G3, seed='考法三', direction='深化',
    kaofa='两种变动，分子分母逐项判断', technique='逐项判断分子分母',
    difficulty=2, time_s=70,
    stem='某企业的用工由合同制职工和劳务派遣人员两部分组成，其中劳务派遣人员占15%。为规范用工，企业先将10名劳务派遣人员转为合同制职工，再将20名劳务派遣人员退回派遣单位，除此之外用工没有其他变动，此时劳务派遣人员占用工总量的比例降为10%。该企业原来的用工总量为（ ）人。',
    options={'A': '360', 'B': '400', 'C': '540', 'D': '560'}, answer='D',
    jiexi='卡点：两次变动对分母的影响不同，要逐项判断。转为合同制的10人仍在企业，只减分子、不减分母；退回的20人分子、分母都减。设原总量x，0.15x−10−20＝0.1(x−20)，x＝560，选D（派遣84人→54人，54÷540＝10%）。易错：照搬“其余部分不变”、漏掉转正的10人，得360，最典型；把下降的5个百分点直接对应退回的20人，得400；把转正也算成总量减少（或答成现在的总量），得540。',
))
V.append(dict(
    vid='D01-math-h-v05', group=G3, seed='2022JSA-57', direction='深化',
    kaofa='两单位规模不等的两层比例合并', technique='十字交叉定规模比',
    difficulty=3, time_s=100,
    stem='甲、乙两个农民专业合作社合并，每名社员只属于种植户、养殖户中的一类。合并前，甲社种植户与养殖户的人数之比为2:1，乙社为1:2；合并后，种植户与养殖户的人数之比为5:4。甲社种植户中有$\\frac{1}{4}$、养殖户中有$\\frac{1}{3}$开设了网店，乙社种植户中有$\\frac{1}{2}$、养殖户中有$\\frac{2}{3}$开设了网店。合并后开设了网店的社员中，种植户与养殖户的人数之比为（ ）。',
    options={'A': '1:2', 'B': '3:5', 'C': '3:4', 'D': '4:3'}, answer='C',
    jiexi='卡点：两社人数不等，不能按“各占一半”合并，要先用种植户占比求两社规模比。种植户占比甲社$\\frac23$、乙社$\\frac13$，合并后$\\frac59$，十字交叉得甲:乙＝($\\frac59-\\frac13$):($\\frac23-\\frac59$)＝2:1。设甲社36人（种植24、养殖12）、乙社18人（种植6、养殖12），开网店的种植户6＋3＝9人、养殖户4＋8＝12人，比为3:4，选C。易错：默认两社人数相等，得3:5，最典型；规模比对应反了，得1:2；比例颠倒成4:3。',
))
V.append(dict(
    vid='D01-math-h-v06', group=G4, seed='2020SZS-18', direction='深化',
    kaofa='总价不变，数量比化价格反比', technique='数量比取倒数',
    difficulty=2, time_s=60,
    stem='某单位工会每次都花同样多的钱为职工采购同一品种的荔枝：第一次按原价采购，买了300斤；第二次采购时价格有所下降，买了400斤；第三次采购时价格在第二次的基础上又下降了2元/斤，买了480斤。这种荔枝的原价为（ ）元/斤。',
    options={'A': '8', 'B': '9.6', 'C': '15', 'D': '16'}, answer='D',
    jiexi='卡点：每次花的钱一样多，单价与数量成反比，要把数量比取倒数，而不是把顺序倒过来。数量比300:400:480＝15:20:24，单价比＝$\\frac1{15}:\\frac1{20}:\\frac1{24}$＝8:6:5。第三次比第二次每斤低1份＝2元，原价为8份＝16元/斤，选D（每次花4800元）。易错：把单价比写成24:20:15，得9.6；以为数量多几分之几、单价就降几分之几，得15；把2元当成第一次的降价，得8。',
))

for v in V:
    v['figure_svg'] = None
    v['verify'] = f"verify/{v['vid']}.py"

ORDER = ['vid', 'group', 'seed', 'direction', 'kaofa', 'technique', 'difficulty', 'time_s',
         'stem', 'options', 'answer', 'jiexi', 'figure_svg', 'verify']
V = [{k: v[k] for k in ORDER} for v in V]

# ---------- checks ----------
HINT_WORDS = ['赋值', '十字', '设而不求', '不变量', '整体代换', '整体法', '份数', '单位"1"', '单位“1”', '量率', '提示', '考法', '技巧',
              '秒杀', '盈亏', '还原', '倒推', '代换', '代入', '方程', '比例法', '特值', '模型', '公式', '差不变', '注意：', '本题', '【',
              '不变', '反比', '假设', '份']
probs = []
for v in V:
    vid = v['vid']
    if len(v['jiexi']) > 250: probs.append((vid, 'jiexi too long', len(v['jiexi'])))
    if len(v['kaofa']) > 20: probs.append((vid, 'kaofa too long'))
    if len(v['technique']) > 12: probs.append((vid, 'technique too long', len(v['technique'])))
    for w in HINT_WORDS:
        if w in v['stem'] or any(w in o for o in v['options'].values()):
            probs.append((vid, 'hint word', w))
    if not re.search(r'（ ）[^（）。]*。$', v['stem']): probs.append((vid, 'stem ending'))
    if '参考用时' in v['jiexi']: probs.append((vid, '参考用时 in jiexi'))
    if f"选{v['answer']}" not in v['jiexi']: probs.append((vid, 'jiexi does not name answer'))
    vals = []
    for k in 'ABCD':
        o = v['options'][k]
        vals.append(F(*map(int, o.split(':'))) if ':' in o else F(o))
    if vals != sorted(vals) or len(set(vals)) < 4: probs.append((vid, 'options not ascending/distinct'))
    if v['difficulty'] not in (2, 3): probs.append((vid, 'difficulty'))
    p = os.path.join(S, v['verify'])
    r = subprocess.run([sys.executable, '-I', p], capture_output=True, text=True, timeout=120, cwd=os.path.dirname(p))
    last = (r.stdout or '').strip().split('\n')[-1]
    if last != v['answer']: probs.append((vid, 'verify', last, r.stderr[-300:]))
    print(vid, 'jiexi', len(v['jiexi']), 'kaofa', len(v['kaofa']), 'tech', len(v['technique']), 'stem', len(v['stem']), 'verify->', last)
print('answers', Counter(v['answer'] for v in V))
for p in probs: print('PROBLEM', p)
if not probs:
    json.dump(V, open(OUT, 'w'), ensure_ascii=False, indent=1)
    print('wrote', OUT, len(V))
