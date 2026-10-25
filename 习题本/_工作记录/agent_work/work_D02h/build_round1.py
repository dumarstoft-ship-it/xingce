import json, re
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
dec = json.load(open(f'{S}/harden/D02_decision.json'))
G = [nv['group'] for nv in dec['new_variants']]   # group titles verbatim, in new_variants order

V = [
 dict(
  seed='2026ZJA-56', direction='深化',
  kaofa='由进度求效率再按效率分配', technique='补齐法+实际工时', difficulty=3, time_s=90,
  stem='某快递分拨中心的甲、乙、丙三条分拣线上午8:00同时开工，各自分拣280件包裹。12:00时，甲线还剩160件、乙线还剩80件未分拣，丙线已于11:30分拣完毕。次日新到560件包裹，全部分给这三条线分拣：甲、乙两线8:00开工，丙线因检修9:00才开工，要求三条线同时分拣完毕。若各线的分拣速度与前一天相同，应给丙线分配的包裹为（ ）件。',
  options={'A': '224', 'B': '240', 'C': '280', 'D': '320'}, answer='B',
  jiexi='卡点：按效率分配≠按效率比分，分配量=效率×实际工作时间。先求速度：丙280件只用了3.5小时，每小时80件；甲(280−160)÷4=30件、乙(280−80)÷4=50件，速度比3:5:8。次日丙晚开工1小时，先“补齐”：假设丙也8:00开工，总量变为560+80=640，按3:5:8分每份40，丙得320件，再减去补上的80件，应分240件（三线均于12:00完成），选B。易错：直接按3:5:8分得280；补齐后忘减得320；丙速度误按280÷4算得224。',
 ),
 dict(
  seed='资源消耗·中途返回', direction='拓展',
  kaofa='中途返回带走补给的人·天', technique='人·天逐人算账', difficulty=2, time_s=60,
  stem='某科考队进入无人区考察，携带的补给恰好够全体队员用25天（每人每天的消耗量相同）。出发5天后，有6名队员原路返回，返程同样需要5天，返程所需补给从现有补给中带走；其余队员继续考察，剩下的补给又恰好用了23天。该科考队原有队员（ ）人。',
  options={'A': '26', 'B': '30', 'C': '36', 'D': '46'}, answer='C',
  jiexi='卡点：返程补给是“看不见的消耗”，按人·天逐人算账。原计划每人用25天的量：返回的6人只用了去程5天+返程5天=10天，每人省下15天，共省90人·天；其余队员实际用了5+23=28天，每人多用3天。省下的恰好被多用掉，其余队员有90÷3=30人，原有30+6=36人，选C。也可列25N=6×10+28(N−6)。易错：忘了返程补给得46；返程按往返10天带补给得26；答成留下的30人。',
 ),
 dict(
  seed='牛吃草·中途减少台数', direction='深化',
  kaofa='牛吃草中途减少台数反求原数', technique='新旧分拨+还原', difficulty=3, time_s=90,
  stem='某地铁站基坑内有一定积水，且地下水以恒定速度渗入坑内。若用10台同型号抽水泵，18小时可将坑内积水抽干；若用14台，9小时可抽干。施工方先开动若干台抽水泵，抽了4小时后调走3台支援另一处工地，剩下的抽水泵又抽了2小时，恰好将积水抽干。开始时开动的抽水泵有（ ）台。',
  options={'A': '13', 'B': '15', 'C': '16', 'D': '19'}, answer='D',
  jiexi='卡点：中途减泵后公式不能直接套，要把抽新渗水和抽原有积水的泵分开看。由10台18小时、14台9小时：抽原有积水的泵数与时间成反比，为1:2，相差的4台就是1份，故10台中4台抽原有积水、6台恰好抵消渗水，原有积水=4×18=72（台·小时）。还原：若调走的3台没走，原有积水相当于72+3×2=78，由N−6台抽6小时，N−6=13，N=19，选D。易错：忘了这6小时新渗入的水得13；渗水只算后2小时得15；答成调走后的16台。',
 ),
 dict(
  seed='依次加入', direction='拓展',
  kaofa='每隔几天增加一台的依次加入', technique='等差求和定段', difficulty=2, time_s=75,
  stem='某河涌清淤工程，若只用1艘清淤船作业，需要300天完成。实际施工时清淤船分批投入：第1~5天1艘，从第6天起增至2艘，从第11天起增至3艘……此后每5天增加1艘，直到完工（每艘船每天的清淤量相同）。该工程完工是在第（ ）天。',
  options={'A': '50', 'B': '52', 'C': '53', 'D': '55'}, answer='C',
  jiexi='卡点：船数逐段递增，各段完成量5×1、5×2、5×3……成等差，用求和公式直接定位，不必逐天累加。设1艘每天完成1份，总量300份。前m段共完成5m(m+1)÷2，m=10时为275，m=11时为330>300，所以第50天末完成275，剩25份由11艘完成，25÷11≈2.3，还需3天，第53天完工，选C。易错：凑满第11段答55；把2.3天当成2天答52；停在第10段末答50。',
 ),
 dict(
  seed='效率与时间反比', direction='深化',
  kaofa='先提效后降效同幅度不抵消', technique='分段时间按倒数算', difficulty=2, time_s=75,
  stem='某段海堤加固工程原计划每天施工量相同，若干天完工。实际施工中，前一半工程量施工时天气晴好，工作效率比原计划提高了40%；后一半工程量施工时遭遇连续降雨，工作效率比原计划降低了40%，结果比原计划推迟4天完工。该工程原计划工期为（ ）天。',
  options={'A': '21', 'B': '25', 'C': '30', 'D': '70'}, answer='A',
  jiexi='卡点：一升一降同幅度并不抵消。工作量对半分，时间与效率成反比：提高40%，效率比5:7，时间×$\\frac{5}{7}$；降低40%，效率比5:3，时间×$\\frac{5}{3}$。设每半段原计划21份时间，实际15+35=50份，比原计划42份多8份=4天，1份=0.5天，原计划42×0.5=21天，选A。易错：把效率提高40%当成时间减少40%得30；把效率降低40%当成时间增加40%得70；把整体效率1.4×0.6=0.84误当成时间增加16%得25。若按时间对半分，完成量才真正抵消。',
 ),
]

out = []
for i, v in enumerate(V, 1):
    vid = f'D02-math-h-v{i:02d}'
    rec = {'vid': vid, 'group': G[i - 1], 'seed': v['seed'], 'direction': v['direction'], 'kaofa': v['kaofa'],
           'technique': v['technique'], 'difficulty': v['difficulty'], 'time_s': v['time_s'], 'stem': v['stem'],
           'options': v['options'], 'answer': v['answer'], 'jiexi': v['jiexi'], 'figure_svg': None,
           'verify': f'{S}/verify/{vid}.py'}
    # format checks
    assert len(rec['kaofa']) <= 20 and len(rec['technique']) <= 12, vid
    assert rec['stem'].endswith('（ ）' + rec['stem'].split('（ ）')[-1]) and re.search(r'（ ）[人台天件]。$', rec['stem']), vid
    assert len(rec['jiexi']) <= 250, (vid, len(rec['jiexi']))
    assert '参考用时' not in rec['jiexi'] and '用时' not in rec['jiexi'][-30:], vid
    assert f"选{rec['answer']}" in rec['jiexi'], vid
    assert rec['options'][rec['answer']] in rec['jiexi'], vid
    for bad in ('牛吃草', '台·天', '人·天', '等差', '反比', '效率之比', '效率比为', '补齐', '按比例', '还原', '赋值'):
        assert bad not in rec['stem'], (vid, bad)
    print(vid, 'jiexi', len(rec['jiexi']), 'stem', len(rec['stem']), rec['answer'], rec['group'][:5])
    out.append(rec)

json.dump(out, open(f'{S}/gen/D02_math_h.json', 'w'), ensure_ascii=False, indent=1)
print('answers', [r['answer'] for r in out])
