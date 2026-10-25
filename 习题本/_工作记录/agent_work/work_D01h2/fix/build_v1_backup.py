"""Build gen/D01_math_h2.json (needs 7-12 of D01 decision new_variants)."""
import json, re, sys

S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
dec = json.load(open(f'{S}/harden/D01_decision.json'))
needs = dec['new_variants']

items = [
    dict(
        k=7, seed='考法四', direction='拓展', difficulty=2, time_s=80,
        technique='钱×时间分段加权',
        stem=('甲、乙、丙三人合伙经营一家预制菜加工坊。甲年初出资30万元，全年未变动；'
              '乙年初出资80万元，4月初撤回其中的40万元；丙10月初加入，出资80万元，此后各人出资均未再变动。'
              '三人约定：年终利润先提取20%作为发展基金，其余按各人“出资额×出资月数”的比例分配。'
              '年终结算时丙分得16万元，则该加工坊这一年的利润为（ ）万元。'),
        options={'A': '80', 'B': '100', 'C': '130', 'D': '140'}, answer='B',
        jiexi=('卡点：分配权重是“钱×时间”，乙中途撤资要分段算；由丙的所得倒推时，还要把先提取的20%加回。'
               '甲30×12＝360，乙80×3＋40×9＝600，丙80×3＝240，共1200，丙占$\\frac{1}{5}$。'
               '可分配利润＝16×5＝80万元，只占利润的80%，利润＝80÷0.8＝100万元，选B。'
               '易错：算出80万元就作答，漏了提取的20%（最典型）；乙按80万元算全年，得130；'
               '丙按“12−10＝2”个月算，得140。'),
    ),
    dict(
        k=8, seed='考法五', direction='深化', difficulty=3, time_s=90,
        technique='每步重找不变量',
        stem=('某县人民医院本院与分院的医生人数之比为3:1。本院抽调部分医生到分院长期支援后，'
              '本院与分院的医生人数之比变为7:3；此后分院又招聘了20名医生，本院与分院的医生人数之比变为3:2。'
              '期间两院没有其他人员变动。最初分院有医生（ ）人。'),
        options={'A': '20', 'B': '30', 'C': '36', 'D': '50'}, answer='B',
        jiexi=('卡点：两步变化的不变量不同——抽调时两院总数不变，招聘时本院人数不变，每一步都要重新找不变量再通分。'
               '先看招聘：本院不变，7:3＝21:9，3:2＝21:14，分院多5份＝20人，1份＝4人，此时两院共30份＝120人；'
               '抽调前后总数相同，最初也是120人，分院占$\\frac{1}{4}$，为30人，选B。'
               '易错：招聘一步仍按总数不变通分，拿7:3与6:4对比，得总数200、分院50（最典型）；'
               '首尾3:1与3:2直接比、当本院始终不变，得20；答成抽调后的36人。'),
    ),
    dict(
        k=9, seed='考法七', direction='拓展', difficulty=2, time_s=70,
        technique='统一基期连乘除',
        stem=('某口岸2025年9月的出入境旅客量比8月下降了25%，比2024年9月增长了20%；'
              '2024年9月的出入境旅客量比8月下降了20%。该口岸2025年8月的出入境旅客量比2024年8月增长了（ ）。'),
        options={'A': '20%', 'B': '25%', 'C': '28%', 'D': '60%'}, answer='C',
        jiexi=('卡点：三个增长率的基期各不相同（两个“比上月”、一个“比上年同月”），要统一到同一个基数上连乘除。'
               '设2024年8月为100：2024年9月为80，2025年9月为80×1.2＝96，2025年8月为96÷(1−25%)＝128，'
               '同比增长28%，选C。易错：增长率直接加减，20%−20%＋25%＝25%（最典型）；'
               '倒推时把“比8月下降25%”当成“8月比9月多25%”，96×1.25＝120，得20%；'
               '拿128与2024年9月的80比，得60%。'),
    ),
    dict(
        k=10, seed='考法九', direction='拓展', difficulty=2, time_s=60,
        technique='按人数比打包',
        stem=('某建筑工地给工人发放劳保手套。若每人发6副，还剩50副；若露天作业的工人每人发8副、'
              '其余工人每人发5副，则恰好发完。已知露天作业的工人比其余工人多$\\frac{1}{3}$，'
              '该工地共有工人（ ）人。'),
        options={'A': '70', 'B': '100', 'C': '175', 'D': '470'}, answer='A',
        jiexi=('卡点：两类工人标准不同，要按人数比加权折成一个标准，不能简单平均。'
               '“多$\\frac{1}{3}$”即露天:其余＝4:3，把4名露天工人和3名其余工人打成一组：'
               '第二种发法每组用8×4＋5×3＝47副，第一种每组用6×7＝42副，每组多用5副，'
               '正好用掉多出的50副，共10组、70人，选A。'
               '易错：取(8＋5)÷2＝6.5副当平均标准，得100人（最典型）；人数比写反成3:4，得175人；'
               '求成手套总数470副。'),
    ),
    dict(
        k=11, seed='考法九', direction='拓展', difficulty=2, time_s=70,
        technique='空床位数夹范围',
        stem=('某中学组织新生参加国防教育营，安排学生住营地宿舍。若每间宿舍住4人，则有18人没有宿舍可住；'
              '若每间宿舍住6人，则有一间宿舍住了人但没有住满，其余宿舍都正好住满。'
              '参加国防教育营的学生最多有（ ）人。'),
        options={'A': '54', 'B': '58', 'C': '62', 'D': '66'}, answer='C',
        jiexi=('卡点：“有一间住了人但没住满”给的不是等式，而是范围。设有n间，每间由住4人改为住6人，'
               '共多出2n个床位，先安置没房的18人，剩下的空床都在那间没住满的宿舍里，应有1～5个：'
               '1≤2n−18≤5，得n＝10或11。人数4n＋18最多为62人，选C。'
               '易错：当成“空出一间”，列6(n−1)＝4n＋18，得66（最典型）；当成全部住满，得54；'
               '取了最少的58。'),
    ),
    dict(
        k=12, seed='2020SC1206-48', direction='深化', difficulty=2, time_s=60,
        technique='一站收进减送出',
        stem=('某区甲、乙、丙三个消防救援站开展跨站轮训，各站抽出一个班组：甲站的班组到乙站、'
              '乙站的班组到丙站、丙站的班组到甲站，其余人员不动。轮训期间三个站的在站人数恰好相等。'
              '已知原来甲站比乙站多4人、比丙站少7人，乙站抽出的班组有8人，则甲站抽出的班组有（ ）人。'),
        options={'A': '5', 'B': '7', 'C': '12', 'D': '13'}, answer='D',
        jiexi=('卡点：不必设六个未知数，只盯乙站一个站的“收进−送出”，并先算准平均数。'
               '设甲站原有a人，则乙站a−4人、丙站a＋7人，平均每站a＋1人。乙站送出本站8人、收进甲站的班组，'
               '最后变成a＋1人：a−4−8＋甲组＝a＋1，甲组＝13人，选D。'
               '易错：以为相等时都等于甲站原有的a人，得12（最典型）；把轮换方向弄反，按甲站收进乙站班组列式，得7；'
               '把乙站净增的5人当成班组人数。'),
    ),
]

HINT_WORDS = ['比例问题', '盈亏', '赋值', '份数', '不变量', '整体', '十字交叉', '设而不求', '代入',
              '公式', '提示', '不等式', '加权', '平均', '基期', '同比', '环比', '净变化', '打包', '通分',
              '【', '改编', '真题']

out, probs = [], []
for it in items:
    need = needs[it['k'] - 1]
    vid = f"D01-math-h-v{it['k']:02d}"
    rec = {
        'vid': vid,
        'group': need['group'],
        'seed': it['seed'],
        'direction': it['direction'],
        'kaofa': need['kaofa'],
        'technique': it['technique'],
        'difficulty': it['difficulty'],
        'time_s': it['time_s'],
        'stem': it['stem'],
        'options': it['options'],
        'answer': it['answer'],
        'jiexi': it['jiexi'],
        'figure_svg': None,
        'verify': f'verify/{vid}.py',
    }
    # self checks
    if len(rec['kaofa']) > 20: probs.append((vid, 'kaofa>20', len(rec['kaofa'])))
    if len(rec['technique']) > 12: probs.append((vid, 'technique>12'))
    if len(rec['jiexi']) > 250: probs.append((vid, 'jiexi>250', len(rec['jiexi'])))
    if not re.search(r'（ ）[^。（）]{0,3}。$', rec['stem']): probs.append((vid, 'stem ending'))
    for w in HINT_WORDS:
        if w in rec['stem'] or any(w in o for o in rec['options'].values()):
            probs.append((vid, 'hint word in stem/options: ' + w))
    if '参考用时' in rec['jiexi']: probs.append((vid, 'jiexi has 参考用时'))
    vals = list(rec['options'].values())
    nums = [float(v.rstrip('%')) for v in vals]
    if nums != sorted(nums): probs.append((vid, 'options not ascending'))
    print(vid, 'jiexi', len(rec['jiexi']), 'stem', len(rec['stem']), 'kaofa', rec['kaofa'], '|', rec['group'])
    out.append(rec)

for p in probs: print('SELFCHECK', p)
if '--write' in sys.argv and not probs:
    with open(f'{S}/gen/D01_math_h2.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('written', len(out))
