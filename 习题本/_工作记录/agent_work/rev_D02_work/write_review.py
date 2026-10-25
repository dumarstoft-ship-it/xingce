import json
KEY = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/review/D02_math_key.json'
OUT = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/review/D02_math_review.json'
MINE = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/rev_D02_work/blind_answers.json'
key = json.load(open(KEY, encoding='utf-8'))
mine = json.load(open(MINE, encoding='utf-8'))

problems = {
    'D02-math-2-v08': (
        'fix',
        '答案、解析、验算都对，问题是雷同：①情境与1-v05几乎相同（“某市档案馆开展档案数字化扫描”/“某档案馆开展档案数字化工作”），'
        '同一天还有真题2024GD-36（档案室整理档案），一天里3道档案题；②第一步“效率提高20%→时间缩短1/6、提前N天求原计划”与1-v03完全相同（同为6:5）。'
        '建议改情境，最好顺便换比例，例如：“某镇开展高标准农田建设需平整一批土地。若一开始就使用新型激光平地机，工作效率可提高25%，能比原计划提前6天完成；'
        '实际先用普通平地机作业了若干天，之后才换用新机器，结果比原计划提前4天完成。用普通平地机作业了（ ）天。”选项6/8/10/20，答案10'
        '（原计划6÷$\\frac{1}{5}$=30天；新机器完成原计划工作量的$\\frac{4}{6}=\\frac{2}{3}$，普通机完成$\\frac{1}{3}$即10天）。'
        '干扰项：20=比例用反；8=把“效率提高25%”当成“时间缩短25%”（原计划24天、新机器部分16天）；6=实际26天−20。已用程序验算唯一正确。'
        '若只想小改，至少把情境换掉（避开档案、道路、港口这几个本组已用的情境）。'
    ),
}

items = []
for k in key:
    v = k['vid']
    verdict, prob = problems.get(v, ('ok', ''))
    items.append({'vid': v, 'my_answer': mine[v], 'key': k['answer'], 'verdict': verdict, 'problem': prob})

overall = (
    '27题盲做与答案27/27一致；自写程序（枚举/逐日逐时模拟）逐题复核，均恰有一个正确选项。27个验算脚本都从题面数据独立求解、未写死答案，全部通过，'
    '脚本中的选项与题目文件一致；解析里列举的每一个易错值都已逐一复算，数据和归因全部正确；KaTeX 18处均可渲染。结论：26 ok、1 fix、0 drop。'
    '优点：没有只换数字的题。逆向改编（1-v04由完工日期反求合作天数、1-v09由剩余量反求总量、1-v11/1-v12资源消耗反求时长/人数、2-v07反求维修时长）、'
    '加折算（1-v13大小设备、1-v16按亩、2-v02底面积）、伪装情境（1-v15隧道积水、2-v11仓库进出货）和新子型（2-v03半高排水口、2-v06按工作量分报酬、'
    '2-v09比较轮流顺序、2-v10不等长周期）覆盖面广；干扰项大多来自真实错因；难度8道一星、18道二星、1道三星，符合第2天“基础到中等”的定位；'
    '答案分布A7/B7/C7/D6。'
    '问题与建议：①2-v08与1-v05情境雷同（另有同日真题2024GD-36也是档案），且与1-v03同用“提效20%→时间缩短1/6”，已列fix并给出验算过的替换数据。'
    '②格式不统一：math-2组11道解析都没写“选X”（math-1组16道都有），建议统一补上。'
    '③2-v04与同日真题2025GD-39结构几乎同构（合作→甲抽调→节点完成比例→丙加入→甲返回→提前完工），只是所求从“丙/甲效率比”改成“几天后返回”，'
    '作为巩固题可用，但新意有限；如需拉开，可改问“甲队离开了多少天”或把“提前”改成“推迟”。'
    '④1-v11默认“运行7天=7×24小时”，和真题2026GD-38的口径一致，可以不改；如想更严谨，可写“同时连续运行7天”。'
    '⑤同日“收割稻田”出现两次（1-v02与真题2023ZJA-64），但考法不同，可接受。'
)
json.dump({'items': items, 'overall': overall}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', len(items), 'items')
from collections import Counter
print(Counter(i['verdict'] for i in items), 'agree', sum(i['my_answer'] == i['key'] for i in items))
