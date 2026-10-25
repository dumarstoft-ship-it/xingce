"""Build gen/D01_math_h2.json (needs 7-12 of D01 decision new_variants)."""
import json, re, sys

S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
dec = json.load(open(f'{S}/harden/D01_decision.json'))
needs = dec['new_variants']

items = [
    dict(
        k=7, seed='考法四', direction='拓展', difficulty=2, time_s=75,
        kaofa='按“出资额×月数”分配，反求撤资月份',
        technique='钱×时间，端点计月数',
        stem=('甲、乙、丙三人合伙经营一家预制菜加工坊。甲年初出资30万元，全年未变动；'
              '乙年初出资80万元，年内某月初撤回了其中的40万元；丙8月初加入，出资80万元。'
              '除此之外，三人的出资均无变动。年终利润全部按各人“出资额×出资月数”的比例分配，'
              '结果乙分得的利润恰好是丙的2倍。乙撤回40万元是在（ ）月初。'),
        options={'A': '8', 'B': '9', 'C': '5', 'D': '7'}, answer='B', keep_order=True,
        jiexi=('卡点：分配看“钱×时间”，撤资月份未知时要把“w月初撤资”准确译成月数：80万元出资了(w−1)个月，'
               '40万元出资了(13−w)个月。丙出资8～12月共5个月，权重80×5＝400；乙是丙的2倍即800：'
               '80(w−1)＋40(13−w)＝800，得w＝9，乙9月初撤资，选B（甲的数据用不上）。'
               '易错：解出“80万元出资了8个月”就答8月（最典型）；月数两头都算，列80w＋40(13−w)＝800，得7；'
               '丙按“12−8＝4”个月算，得5。'),
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
        k=9, seed='考法七', direction='拓展', difficulty=3, time_s=80,
        kaofa='同比环比串联＋两月合计加权',
        technique='统一基期，按月拆合计',
        stem=('某海岛客运码头2025年9月的旅客发送量比8月下降了25%，2024年9月的旅客发送量比8月下降了40%；'
              '2025年8、9两月的旅客发送量合计比2024年同期增长了40%。'
              '该码头2025年9月的旅客发送量比2024年9月增长了（ ）。'),
        options={'A': '28%', 'B': '40%', 'C': '55%', 'D': '60%'}, answer='D',
        jiexi=('卡点：两月合计的增速是两个月同比增速按上年基数加权的结果，要先统一基期，再按今年的月间比例拆分合计。'
               '设2024年8月为100，则9月为60，合计160；2025年合计160×1.4＝224，8、9月之比为1:0.75，'
               '8月＝224÷1.75＝128，9月＝96，9月同比增长96÷60−1＝60%，选D。'
               '易错：增长率直接加减，40%＋(40%−25%)＝55%（最典型）；把合计增速40%当成9月的增速；'
               '算成8月同比28%。'),
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
        k=12, seed='考法十', direction='深化', difficulty=3, time_s=90,
        kaofa='三方轮换：两条净变化＋总数定解',
        technique='收进−送出＋补总数',
        stem=('某县甲、乙、丙三所乡镇中学开展教师交流轮岗，每校选派一个交流小组到另一所学校任教一学期：'
              '甲校的小组到丙校，丙校的小组到乙校，乙校的小组到甲校，其余教师不动。'
              '交流期间三所学校的在岗教师人数恰好相等。已知原来甲校的教师比乙校少12人，丙校比乙校少9人，'
              '三个交流小组共30人，则丙校选派的交流小组有（ ）人。'),
        options={'A': '7', 'B': '10', 'C': '11', 'D': '13'}, answer='A',
        jiexi=('卡点：每校只能列一条“收进−送出＝平均数−原人数”，三条相加恒为0，只有两条独立，'
               '盯住一所学校解不出，必须用上“三组共30人”。设乙校原有n人，则甲校n−12人、丙校n−9人，平均n−7人。'
               '甲校送出甲组、收进乙组，净增5：乙组＝甲组＋5；丙校送出丙组、收进甲组，净增2：甲组＝丙组＋2。'
               '于是3×丙组＋9＝30，丙组＝7人，选A。易错：按30÷3＝10人平均分；轮换方向弄反，得11；'
               '净变化正负弄反，得13。'),
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
        'kaofa': it.get('kaofa', need['kaofa']),
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
    if nums != sorted(nums) and not it.get('keep_order'): probs.append((vid, 'options not ascending'))
    print(vid, 'jiexi', len(rec['jiexi']), 'stem', len(rec['stem']), 'kaofa', rec['kaofa'], '|', rec['group'])
    out.append(rec)

for p in probs: print('SELFCHECK', p)
if '--write' in sys.argv and not probs:
    with open(f'{S}/gen/D01_math_h2.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('written', len(out))
