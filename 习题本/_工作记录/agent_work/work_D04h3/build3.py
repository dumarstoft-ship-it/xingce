# Round 3 (after revh2_C review + coordinator notes): rebuild gen/D04_math_h3.json
# - v16: reviewer's integer data (9 / 16 / 11 / 35%), A = 约2.6%
# - v15: technique label in plain words
# - v17: question asks for the freight at which the two profits are equal (different wording, same data/answer)
# - v18: options rotated to 1080/420/540/1000 (answer A)
# - all: jiexi ends with “选X。”, no other “选X” inside
import json, re

S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
old = {v['vid']: v for v in json.load(open(S + '/work_D04h3/D04_math_h3_round2.json', encoding='utf-8'))}
items = []

v = dict(old['D04-math-h-v14'])
v['jiexi'] = (r'卡点：三种方案都是分段计费，两个临界点要各在对应的段里求，不能拿“含多少小时”当边界。'
              r'乙与甲比：20小时内乙只交1200元，$1200\div80=15$，超过15小时乙更省（超出20小时后乙每小时60元仍比甲便宜）。'
              r'乙与丙比：50小时内丙固定2400元，乙超出20小时后再用 $(2400-1200)\div60=20$ 小时就与丙持平，即40小时；'
              r'50小时以上丙单价更低。所以时长大于15且小于40。易错：只看两档的包含时长，得D；两个临界点只求对一个，得B或C。选A。')
items.append(v)

v = dict(old['D04-math-h-v15'])
v['technique'] = '只比变化量，固定成本不计'
v['jiexi'] = (r'卡点：接不接单只比“变化的部分”。每月固定成本总额（$15\times8000=120000$ 元）不因接单而变，'
              r'单件成本里分摊的15元与决策无关；产能只剩2000件，接单要挤掉1000件常规销售，每件损失的是 $60-30=30$ 元。'
              r'所以 $3000(p-30)\ge1000\times30$，$p\ge40$。'
              r'易错：只看变动成本、忘了被挤掉的常规销售，得30；被挤掉的每件按利润 $60-45=15$ 元算，得35；'
              r'以为单价不能低于成本45元，得45。选C。')
items.append(v)

v = dict(old['D04-math-h-v16'])
v['stem'] = ('某生鲜店从产地购进一批杨梅，进价为每斤9元。运输途中共2天，每天都损耗当天开始时所剩杨梅的同一个百分比，'
             '损耗的杨梅不能出售。运到后，可售杨梅的80%按每斤16元售出，其余的降价到每斤11元清仓，全部卖完。'
             '结果这批杨梅的利润率恰好为35%。运输途中每天损耗的百分比为（ ）。')
v['options'] = {'A': '约2.6%', 'B': '9.5%', 'C': '10%', 'D': '19%'}
v['answer'] = 'C'
v['jiexi'] = (r'卡点：两天损耗是连乘，要用 $(1-x)^2$ 反解，不能按“两天约损耗 $2x$”线性估算。'
              r'每斤可售杨梅平均卖 $0.8\times16+0.2\times11=15$ 元；进价9元、利润率35%，每斤进货要收回 $9\times1.35=12.15$ 元，'
              r'可售比例 $12.15\div15=0.81=(1-x)^2$，$x=10\%$。'
              r'易错：按 $1-2x=0.81$ 得9.5%（最典型）；答成两天共损耗19%；漏算清仓收入，由 $12.8(1-x)^2=12.15$ 得约2.6%。选C。')
items.append(v)

v = dict(old['D04-math-h-v17'])
v['stem'] = ('某花卉合作社接到外地花市的订单，要按每扎30元的价格交付960扎完好的鲜切花，每扎收购价为12元。'
             '若用普通物流，运费为每扎1元，途中损耗20%；若用冷链物流，途中损耗只有4%。'
             '两种物流的运费都按发运的扎数计算，途中损耗的花不能交付。'
             '若选冷链物流与选普通物流的利润恰好相同，则冷链物流的运费为每扎（ ）元。')
v['jiexi'] = (r'卡点：交付量固定，两种方式收入相同，但要发运的扎数不同，收购成本也不同，要比“收购费＋运费”。'
              r'普通物流要发 $960\div0.8=1200$ 扎，共花 $1200\times13=15600$ 元；冷链只需发 $960\div0.96=1000$ 扎，'
              r'由 $1000(12+c)=15600$ 得 $c=3.6$。'
              r'易错：只比运费，得1.2；漏了普通物流的运费，得2.4；发运量误按“960×(1+损耗率)”算，得3。选D。')
items.append(v)

v = dict(old['D04-math-h-v18'])
v['options'] = {'A': '1080', 'B': '420', 'C': '540', 'D': '1000'}   # rotated ascending, answer moved to A
v['answer'] = 'A'
v['jiexi'] = (r'卡点：退货有300盒上限，买断的利润要分段讨论。剩余不少于300盒时只能退300盒：'
              r'$60x-36000+12\times300\ge30x$，得 $x\ge1080$，此时剩420盒，确实不少于300，成立；'
              r'剩余少于300盒（$x>1200$）时，买断利润 $48x-18000$ 一定不低于 $30x$。故至少卖出1080盒。'
              r'易错：忽略上限、把剩余的全按12元退，得1000（此时剩500盒，与上限矛盾）；答成剩余量420；只求买断不亏本，得540。选A。')
items.append(v)

v = dict(old['D04-math-h-v19'])
v['jiexi'] = (r'卡点：逐档比较多订的那一批。每多订1瓶，卖掉多赚4元，卖不掉亏 $8-2=6$ 元。'
              r'80加到100：多出的20瓶有17天能卖掉、3天剩下，$4\times17>6\times3$，划算；'
              r'100加到120：11天能卖掉、9天剩下，$4\times11<6\times9$，不划算，再往上更亏。'
              r'故订100瓶（订80、100、120、140瓶的总利润依次为6400、7400、7200、5600元）。'
              r'易错：按众数、均值或“过半天数能卖完”订120；按最大需求订140；按最小需求订80。可放后做。选D。')
items.append(v)

# ---- checks ----
BANNED = ['边际', '临界', '分段', '机会成本', '十字', '线段法', '赋值', '节点', '加权', '连乘', '报童', '考法', '技巧', '【', '开方']
for it in items:
    it['figure_svg'] = None
    it['verify'] = 'verify/%s.py' % it['vid']
    st = it['stem']
    assert re.search(r'（ ）[^\s，。、；：（）]{0,3}。$', st), ('stem ending', it['vid'], st[-12:])
    for w in BANNED:
        assert w not in st and all(w not in o for o in it['options'].values()), ('hint word', it['vid'], w)
    j = it['jiexi']
    assert j.startswith('卡点：'), it['vid']
    assert '参考用时' not in j, it['vid']
    assert len(j) <= 250, (it['vid'], len(j))
    assert j.endswith('选%s。' % it['answer']), (it['vid'], j[-6:])
    assert re.findall(r'选[A-D]', j) == ['选%s' % it['answer']], (it['vid'], re.findall(r'选[A-D]', j))
    assert len(it['kaofa']) <= 20 and len(it['technique']) <= 12, (it['vid'], len(it['kaofa']), len(it['technique']))
    assert sorted(it['options']) == list('ABCD') and it['answer'] in 'ABCD'
    print(it['vid'], 'jiexi', len(j), 'ans', it['answer'], 'opts', list(it['options'].values()), '| tech', it['technique'])

keys = ['vid', 'group', 'seed', 'direction', 'kaofa', 'technique', 'difficulty', 'time_s', 'stem', 'options', 'answer',
        'jiexi', 'figure_svg', 'verify']
out = [{k: it[k] for k in keys} for it in items]
with open(S + '/gen/D04_math_h3.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('wrote', len(out))
