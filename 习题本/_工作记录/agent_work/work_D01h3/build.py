"""Build gen/D01_math_h3.json (needs 13-18 of D01 decision new_variants)."""
import json, re, sys

S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
OUT = S + '/gen/D01_math_h3.json'
V = S + '/verify/D01-math-h-v{:02d}.py'

G10 = '考法十：转移调配与倒推还原'
G11 = '考法十一：等价代换、兑换与配套'
G12 = '考法十二：多元一次方程组（消元与整体求和）'
G15 = '考法十五：平均分摊与多退少补（题库缺）'

items = [
    dict(
        k=13, group=G10, seed='2022HB-66', direction='深化',
        kaofa='三方互相翻倍，末态成比例倒推', technique='正推规律+整除定解',
        difficulty=3, time_s=120,
        stem=('某快递网点A、B、C三个分拣台共有待分拣包裹200件，为平衡工作量，网点在三个分拣台之间先后调配了三次：'
              '第一次从A台分出部分包裹给B、C两台，使B、C两台的包裹数都增加了一倍；'
              '第二次从B台分出部分包裹给A、C两台，使A、C两台的包裹数都增加了一倍；'
              '第三次从C台分出部分包裹给A、B两台，使A、B两台的包裹数都增加了一倍。'
              '调配期间没有包裹进出这三个分拣台，调配结束时C台的包裹数恰好是A台的$\\frac{7}{8}$。'
              '调配前A台有包裹（ ）件。'),
        options={'A': '104', 'B': '107', 'C': '108', 'D': '116'}, answer='C',
        jiexi=('卡点：末态只给比例，要靠“包裹数都是整数”定解。正推更快：每次分出包裹的那一台，新数＝2×原数−200，另两台翻倍，'
               '故末态A＝4(2a−200)、末态C＝8c−200。由末态C＝$\\frac{7}{8}$×末态A得8c＝7a−500，a除以8余4，选项只剩108、116；'
               'a＝116时b＝45，第二次B台不够分，故a＝108。也可设末态A＝8x、C＝7x倒推，得a＝100＋x。'
               '易错：倒推只验到x是4的倍数，选104；不验B台够不够分（末态B＝200−15x＞0），选116；比例看反得107。'),
    ),
    dict(
        k=14, group=G11, seed='2024GK-67', direction='深化',
        kaofa='销售额相等→数量反比→打包', technique='反比定包+假设法',
        difficulty=2, time_s=80,
        stem=('某博物馆推出甲、乙、丙三种研学套票，单价分别为60元、40元、80元。'
              '某天三种套票共售出300张，收入18400元，其中甲、乙两种套票的销售额相同。'
              '这天丙种套票售出（ ）张。'),
        options={'A': '25', 'B': '70', 'C': '100', 'D': '125'}, answer='D',
        jiexi=('卡点：“甲、乙销售额相同”→张数与单价成反比，甲∶乙＝40∶60＝2∶3。'
               '把2张甲＋3张乙打成一包（5张，240元），丙也5张一包（400元），300张共60包。'
               '假设全是甲乙包，收入14400元，比实际少4000元；每把一包换成丙多收160元，丙有25包，即125张。'
               '易错：按单价正比取甲∶乙＝3∶2，得100（最典型）；求出25包忘了乘5；答成甲票的70张。'),
    ),
    dict(
        k=15, group=G12, seed='考法十二', direction='深化',
        kaofa='总量相同先定比，再配大小车', technique='齐次定比+鸡兔同笼',
        difficulty=3, time_s=90,
        stem=('某镇调运一批防汛沙袋加固堤围。若派2辆大货车和4辆小货车，运5趟恰好运完；'
              '若派1辆大货车和7辆小货车，运4趟也恰好运完。现调派大、小货车共14辆，运2趟恰好运完。'
              '已知每辆车每趟都满载，同型号货车的载重量相同，则调派的大货车有（ ）辆。'),
        # 按协调人要求轮转选项（答案移到B，平衡第1天答案分布），不再按数值升序
        options={'A': '6', 'B': '8', 'C': '1', 'D': '2'}, answer='B', allow_unsorted=True,
        jiexi=('卡点：总量没给，但几种方案运的是同一批沙袋。先定载重比：5×(2大＋4小)＝4×(1大＋7小)，得6大＝8小，大∶小＝4∶3。'
               '设大车每趟4份、小车3份，沙袋共5×(8＋12)＝100份；14辆车2趟运完，每趟要运50份。'
               '若全是小车每趟42份，少8份，每换1辆大车多1份，需大车8辆。'
               '易错：载重比写反（大∶小＝3∶4）得1；补差时除以大车载重4，得2；求成小车辆数6。'),
    ),
    dict(
        k=16, group=G12, seed='考法十二', direction='拓展',
        kaofa='三元两式配系数，求各一件', technique='差式配系数/特值',
        difficulty=3, time_s=70,
        stem=('某社区老年大学书画班分两次采购用品，两次购买的同种用品单价相同。'
              '第一次买了4支毛笔、7刀宣纸和1瓶墨汁，共花费190元；'
              '第二次买了5支毛笔、9刀宣纸和1瓶墨汁，共花费240元。'
              '买1支毛笔、1刀宣纸和1瓶墨汁共需（ ）元。'),
        options={'A': '40', 'B': '50', 'C': '90', 'D': '140'}, answer='A',
        jiexi=('卡点：三个单价都解不出，要把“各1件”用两次购买凑出来。两式相减：1支毛笔＋2刀宣纸＝50元；'
               '第一次的“4支、7刀、1瓶”恰好是“各1件”再加3组“1支＋2刀”，故各1件＝190−3×50＝40元。'
               '也可令墨汁单价为0，解得毛笔30元、宣纸10元，和为40元。'
               '易错：执意求单价而卡住；把差额50元当答案；只减一次差得140；用240减3×50得90。'),
    ),
    dict(
        k=17, group=G15, seed='考法十五', direction='拓展',
        kaofa='拼车按段分摊，由差额反求里程', technique='同乘段抵消看差额',
        difficulty=2, time_s=75,
        stem=('甲、乙两名同事从单位乘同一辆出租车出发，行驶18公里后在途经的小区门口接上同事丙，'
              '三人同乘一段路后甲下车，乙、丙又继续乘坐12公里到达终点。全程车费共150元，车费与行驶里程成正比。'
              '三人约定：每段路程的车费由该段在车上的人平均分摊，结算后丙比甲少付9元。三人同乘了（ ）公里。'),
        options={'A': '20', 'B': '32', 'C': '50', 'D': '70'}, answer='A',
        jiexi=('卡点：同乘段三人平摊，甲、丙在这段付得一样多，差额只来自前后两段：甲另付前18公里车费的一半，丙另付后12公里车费的一半。'
               '设每公里x元，(9−6)x＝9，x＝3，全程150÷3＝50公里，同乘50−18−12＝20公里，不必解同乘里程的方程。'
               '易错：忘了前后两段都是两人平摊，列6x＝9，得70；求出全程50公里就停；把丙的乘车里程32公里当成同乘里程。'),
    ),
    dict(
        k=18, group=G15, seed='考法十五', direction='拓展',
        kaofa='人数增减致人均变化，双条件消总额', technique='抓差异消去总额',
        difficulty=3, time_s=90,
        stem=('某读书会周末组织会员聚会，包下一处农家乐小院，租金由参加的会员平均分摊。'
              '如果比原定多2人参加，每人可少分摊30元；如果比原定少2人参加，每人要多分摊50元。'
              '这处小院的租金是（ ）元。'),
        options={'A': '600', 'B': '720', 'C': '1200', 'D': '1800'}, answer='C',
        jiexi=('卡点：两种假设都含未知租金，抓“差异”把它消掉。设原定n人、每人x元。'
               '多2人：原n人共少付30n元，正是新来2人所付，2(x−30)＝30n；'
               '少2人：剩下n−2人共多付50(n−2)元，正是缺席2人原应付的，2x＝50(n−2)。'
               '两式相减得n＝8，x＝150，租金1200元（设租金T、两式相除也可）。'
               '易错：只验一个条件，720、1800只满足多2人，600只满足少2人。'),
    ),
]

BANNED = ['比例问题', '盈亏', '赋值', '份数', '不变量', '整体', '十字交叉', '设而不求', '代入', '公式',
          '提示', '倒推', '还原', '打包', '反比', '整除', '配系数', '特值', '鸡兔', '分段', '差异', '假设',
          '【', '改编', '真题']
out = []
problems = []
for it in items:
    k = it['k']
    vid = 'D01-math-h-v{:02d}'.format(k)
    rec = {
        'vid': vid, 'group': it['group'], 'seed': it['seed'], 'direction': it['direction'],
        'kaofa': it['kaofa'], 'technique': it['technique'], 'difficulty': it['difficulty'],
        'time_s': it['time_s'], 'stem': it['stem'], 'options': it['options'], 'answer': it['answer'],
        'jiexi': it['jiexi'] + '选{}。'.format(it['answer']), 'figure_svg': None, 'verify': V.format(k),
    }
    sel = re.findall(r'选([ABCD])', rec['jiexi'])
    if sel != [rec['answer']] or not rec['jiexi'].endswith('选{}。'.format(rec['answer'])):
        problems.append((vid, 'jiexi 选X mismatch', sel))
    # field checks
    if len(rec['kaofa']) > 20: problems.append((vid, 'kaofa too long', len(rec['kaofa'])))
    if len(rec['technique']) > 12: problems.append((vid, 'technique too long', len(rec['technique'])))
    if len(rec['jiexi']) > 250: problems.append((vid, 'jiexi too long', len(rec['jiexi'])))
    if '参考用时' in rec['jiexi']: problems.append((vid, 'jiexi has 参考用时'))
    if not re.search(r'（ ）[^，。；（）]{1,3}。$', rec['stem']): problems.append((vid, 'stem ending', rec['stem'][-12:]))
    txt = rec['stem'] + ''.join(rec['options'].values())
    for w in BANNED:
        if w in txt: problems.append((vid, 'hint word in stem/options', w))
    vals = [float(v) for v in rec['options'].values()]
    if vals != sorted(vals) and not it.get('allow_unsorted'): problems.append((vid, 'options not ascending'))
    if rec['stem'].count('$') % 2 or rec['jiexi'].count('$') % 2: problems.append((vid, 'unbalanced $'))
    print(vid, 'jiexi', len(rec['jiexi']), 'stem', len(rec['stem']), 'kaofa', len(rec['kaofa']),
          'tech', len(rec['technique']), 'ans', rec['answer'])
    out.append(rec)

for p in problems: print('PROBLEM', p)
if problems and '--force' not in sys.argv:
    sys.exit(1)
json.dump(out, open(OUT, 'w'), ensure_ascii=False, indent=1)
print('wrote', OUT, len(out))
