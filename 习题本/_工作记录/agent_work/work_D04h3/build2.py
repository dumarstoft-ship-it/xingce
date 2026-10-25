# Round 2 (after blind review revh_D): rebuild gen/D04_math_h3.json
# v14 unchanged; v15 new question (C); v16 deepened (C); v17 deepened (D); v18 deepened (D); v19 options rotated (D).
import json, re

S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
G12 = '考法十二：方案比较与盈亏平衡'
G13 = '考法十三：损耗、滞销与进货决策'

old = {v['vid']: v for v in json.load(open(S + '/gen/D04_math_h3.json', encoding='utf-8'))}
items = [dict(old['D04-math-h-v14'])]          # v14 kept as is (review: ok)

items.append(dict(
    vid='D04-math-h-v15', group=G12, seed='考法十二', direction='拓展',
    kaofa='接单报价：固定成本与产能挤占', technique='只比变化量，按边际贡献计',
    difficulty=3, time_s=75,
    stem=('某服装厂每月最多能生产10000件T恤，目前每月生产并销售8000件，售价为每件60元。按目前的产量核算，'
          '每件T恤的成本为45元，其中材料、计件工资等变动成本为30元，其余是按产量分摊的固定成本。'
          '现有一外贸客户要求当月加订3000件，由于产能不足，工厂接单就要相应减少当月的常规销售。'
          '仅从当月利润考虑，要使接单后当月利润不减少，这批外贸订单的单价至少为（ ）元。'),
    options={'A': '30', 'B': '35', 'C': '40', 'D': '45'},
    answer='C',
    jiexi=(r'卡点：接不接单只比“变化的部分”。每月固定成本总额（$15\times8000=120000$ 元）不因接单而变，'
           r'单件成本里分摊的15元与决策无关；产能只剩2000件，接单要挤掉1000件常规销售，每件损失的是 $60-30=30$ 元。'
           r'所以 $3000(p-30)\ge1000\times30$，$p\ge40$，选C。'
           r'易错：只看变动成本、忘了被挤掉的常规销售，得30；被挤掉的每件按利润 $60-45=15$ 元算，得35；'
           r'以为单价不能低于成本45元，得45。'),
))

items.append(dict(
    vid='D04-math-h-v16', group=G13, seed='考法十三', direction='深化',
    kaofa='连续损耗反求每天损耗率', technique='损耗连乘，开方反解',
    difficulty=2, time_s=60,
    stem=('某生鲜店从产地购进一批杨梅，进价为每斤10.53元。运输途中共2天，每天都损耗当天开始时所剩杨梅的同一个百分比，'
          '损耗的杨梅不能出售。运到后，可售杨梅的80%按每斤18元售出，其余的降价到每斤12.5元清仓，全部卖完。'
          '结果这批杨梅的利润率恰好为30%。运输途中每天损耗的百分比为（ ）。'),
    options={'A': '2.5%', 'B': '9.5%', 'C': '10%', 'D': '19%'},
    answer='C',
    jiexi=(r'卡点：两天的损耗是连乘，要用 $(1-x)^2$ 反解，不能按“两天约损耗 $2x$”线性估算。'
           r'每斤可售杨梅平均卖 $0.8\times18+0.2\times12.5=16.9$ 元，利润率30%，对应进货成本 $16.9\div1.3=13$ 元；'
           r'进价10.53元，可售比例为 $10.53\div13=0.81=(1-x)^2$，$x=10\%$，选C。'
           r'易错：按 $1-2x=0.81$ 解得9.5%（最典型）；答成两天合计损耗19%；漏算清仓收入，得2.5%。'),
))

items.append(dict(
    vid='D04-math-h-v17', group=G13, seed='考法十三', direction='拓展',
    kaofa='定量交货下冷链与普通物流比较', technique='按交付量折算总成本',
    difficulty=2, time_s=70,
    stem=('某花卉合作社接到外地花市的订单，要按每扎30元的价格交付960扎完好的鲜切花，每扎收购价为12元。'
          '若用普通物流，运费为每扎1元，途中损耗20%；若用冷链物流，途中损耗只有4%。'
          '两种物流的运费都按发运的扎数计算，途中损耗的花不能交付。'
          '仅从利润考虑，要使选冷链物流的利润不低于选普通物流，冷链物流的运费最高为每扎（ ）元。'),
    options={'A': '1.2', 'B': '2.4', 'C': '3', 'D': '3.6'},
    answer='D',
    jiexi=(r'卡点：交付量固定，两种方式收入相同，但要发运的扎数不同，收购成本也不同，要比“收购费＋运费”。'
           r'普通物流要发 $960\div0.8=1200$ 扎，共花 $1200\times13=15600$ 元；冷链只需发 $960\div0.96=1000$ 扎，'
           r'由 $1000(12+c)\le15600$ 得 $c\le3.6$，选D。'
           r'易错：只比运费，得1.2；漏了普通物流的运费，得2.4；发运量误按“960×(1+损耗率)”算，得3。'),
))

items.append(dict(
    vid='D04-math-h-v18', group=G13, seed='考法十三', direction='拓展',
    kaofa='限量退货下买断与代销的临界销量', technique='按退货上限分段检验',
    difficulty=3, time_s=75,
    stem=('某超市计划引进1500盒新款月饼，每盒定价60元。厂家提供两种合作方式：一是买断，进价每盒24元，'
          '卖不完的月饼中最多有300盒可按每盒12元退给厂家，其余不能退；二是代销，进价每盒30元，卖不完的可以按进价全部退回。'
          '两种方式下超市都按定价销售，其他费用不计。仅从利润考虑，要使选买断的利润不低于选代销，这批月饼至少要卖出（ ）盒。'),
    options={'A': '420', 'B': '540', 'C': '1000', 'D': '1080'},
    answer='D',
    jiexi=(r'卡点：退货有300盒上限，买断的利润要分段讨论。剩余不少于300盒时只能退300盒：'
           r'$60x-36000+12\times300\ge30x$，得 $x\ge1080$，此时剩420盒，确实不少于300，成立；'
           r'剩余少于300盒（$x>1200$）时，买断利润 $48x-18000$ 一定不低于 $30x$。故至少卖出1080盒，选D。'
           r'易错：忽略上限、把剩余的全按12元退，得1000（此时剩500盒，与上限矛盾）；答成剩余量420；只求买断不亏本，得540。'),
))

v19 = dict(old['D04-math-h-v19'])
v19['options'] = {'A': '120', 'B': '140', 'C': '80', 'D': '100'}   # rotated ascending (like 2024GK-74)
v19['answer'] = 'D'
v19['jiexi'] = (r'卡点：逐档比较多订的那一批。每多订1瓶，卖掉多赚4元，卖不掉亏 $8-2=6$ 元。'
                r'80加到100：多出的20瓶有17天能卖掉、3天剩下，$4\times17>6\times3$，划算；'
                r'100加到120：11天能卖掉、9天剩下，$4\times11<6\times9$，不划算，再往上更亏。'
                r'故订100瓶，选D（订80、100、120、140瓶的总利润依次为6400、7400、7200、5600元）。'
                r'易错：按众数、均值或“过半天数能卖完”订120；按最大需求订140；按最小需求订80。可放后做。')
items.append(v19)

# ---- checks ----
BANNED = ['边际', '临界', '分段', '机会成本', '十字', '线段法', '赋值', '节点', '加权', '连乘', '报童', '考法', '技巧', '【', '开方']
for it in items:
    it['figure_svg'] = None
    it['verify'] = 'verify/%s.py' % it['vid']
    st = it['stem']
    assert re.search(r'（ ）[^\s，。、；：（）]{0,3}。$', st), ('stem ending', it['vid'], st[-12:])
    for w in BANNED:
        assert w not in st and all(w not in o for o in it['options'].values()), ('hint word', it['vid'], w)
    assert it['jiexi'].startswith('卡点：'), it['vid']
    assert '参考用时' not in it['jiexi'], it['vid']
    assert len(it['jiexi']) <= 250, (it['vid'], len(it['jiexi']))
    assert len(it['kaofa']) <= 20 and len(it['technique']) <= 12, (it['vid'], len(it['kaofa']), len(it['technique']))
    assert sorted(it['options']) == list('ABCD') and it['answer'] in 'ABCD'
    assert ('选%s' % it['answer']) in it['jiexi'], it['vid']
    print(it['vid'], 'jiexi', len(it['jiexi']), 'stem', len(st), 'ans', it['answer'], 'opts', list(it['options'].values()))

keys = ['vid', 'group', 'seed', 'direction', 'kaofa', 'technique', 'difficulty', 'time_s', 'stem', 'options', 'answer',
        'jiexi', 'figure_svg', 'verify']
out = [{k: it[k] for k in keys} for it in items]
with open(S + '/gen/D04_math_h3.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('wrote', len(out))
