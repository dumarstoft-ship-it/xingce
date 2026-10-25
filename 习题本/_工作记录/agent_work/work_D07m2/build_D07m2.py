# Build gen/D07_math_2.json (day 7, math batch 2: M08 groups 4/7/5).
# Revision 2 (after blind review): stems end with "（ ）+单位"; jiexi as one paragraph without option
# letters; v01 new person/height data; v08 parallelogram remark corrected.
# gen/real_D07-math-2.json is written only with --real (it is not part of this revision).
import json, sys, re
from collections import Counter

S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
W = S + '/work_D07m2'
V = S + '/verify'
G4 = '考法四：相似三角形与相似比（影长·铺砖·面积比 = 相似比²）'
G7 = '考法七：几何最值入门（周长与面积互定·和定积最大）'
G5 = '考法五：三角形面积比模型（对角线分四块·梯形四块）'
fig_v08 = open(W + '/fig_v08.svg').read().strip()
BL = '（ ）'   # blank, same characters as batch 1: U+FF08, space, U+FF09

items = [
    dict(group=G4, seed='2022GD-39', direction='巩固',
         kaofa='路灯影长·影子顶端位移', technique='影长与人灯距成正比', difficulty=1, time_s=45,
         stem='某小区一盏路灯的灯泡位于灯杆顶端，离地面 4.5 米。身高 1.8 米的小陈先站在距灯杆底部 3 米处，'
              '然后沿直线背离灯杆走到距灯杆底部 9 米处。在这一过程中，小陈影子的顶端在地面上移动了' + BL + '米。',
         options={'A': '4', 'B': '6', 'C': '8.4', 'D': '10'}, answer='D',
         jiexi=r'路灯影长模型：灯杆、人、影子构成“A 字形”相似。设人距灯杆 $d$ 米，影子顶端距灯杆 $x$ 米，'
               r'则 $\frac{x-d}{x}=\frac{1.8}{4.5}=0.4$，得 $x=\frac{5}{3}d$，即顶端到灯杆的距离与人到灯杆的距离成正比。'
               r'$d$ 从 3 变到 9，$x$ 从 5 变到 15，顶端移动 10 米，选 D。'
               r'分步看：影长 $=\frac{1.8d}{4.5-1.8}=\frac{2}{3}d$，影子只变长 4 米，再加上人走的 6 米。'
               r'陷阱：只算影子变长得 4；以为顶端与人同步移动得 6；把比例列成 $\frac{\text{影长}}{d}=\frac{1.8}{4.5}$，'
               r'影长算成 $0.4d$，得 $6+2.4=8.4$。'),
    dict(group=G4, seed='2020ZJB-12', direction='深化',
         kaofa='相似比定块数·按朝向分类计数', technique='逐行计数等差求和', difficulty=2, time_s=60,
         stem='某文化广场有一个边长为 4 米的正三角形舞台，舞台的一个顶点正对北方。现用边长为 50 厘米的正三角形瓷砖'
              '把舞台铺满，瓷砖不切割，每块瓷砖的边都与舞台的边平行。铺好后，有一个顶点正对南方的瓷砖共有' + BL + '块。',
         options={'A': '28', 'B': '32', 'C': '36', 'D': '64'}, answer='A',
         jiexi=r'先用相似比定总块数，再按朝向分类。边长比 $4\div0.5=8$，面积比为 $8^2=64$，共 64 块。'
               r'从北往南逐行看：第 $k$ 行有 $k$ 块顶点朝北的砖，中间夹着 $k-1$ 块顶点朝南的砖，'
               r'每行朝北的都比朝南的多 1 块，8 行共多 8 块，所以朝南的 $=(64-8)\div2=28$ 块，选 A'
               r'（即 $0+1+\cdots+7$；朝北的为 $1+2+\cdots+8=36$）。'
               r'技巧：两种朝向并不各占一半，与舞台同向的比反向的多“行数”块，不必逐行去数。'
               r'陷阱：以为两种朝向各占一半得 32；把顶点朝北的 36 块当成所求；只算了总数 64。'),
    dict(group=G4, seed='2023JSA-53', direction='拓展',
         kaofa='面积比=半径比平方·费用比较', technique='先比个数再乘单价', difficulty=1, time_s=45,
         stem=r'某市一片城区原来由 4G 基站覆盖，每个 4G 基站的覆盖半径为 1.2 千米。现计划改用 5G 基站覆盖同一片城区，'
              r'每个 5G 基站的覆盖半径为 400 米，单个建设费用是 4G 基站的 $\frac{1}{6}$。若所需基站个数都按'
              r'“城区面积÷单个基站的覆盖面积”估算，则用 5G 基站覆盖的建设总费用比用 4G 基站覆盖高' + BL + '。',
         options={'A': '50%', 'B': '150%', 'C': '350%', 'D': '800%'}, answer='A',
         jiexi=r'面积比等于半径比的平方。半径比 $1200\div400=3$，单个基站覆盖面积之比为 $3^2=9$，所以 5G 基站个数是 4G 的 9 倍；'
               r'单价是 4G 的 $\frac{1}{6}$，总费用是 4G 的 $9\times\frac{1}{6}=1.5$ 倍，即高 50%，选 A。'
               r'陷阱：把“是 1.5 倍”当成“高 150%”；把平方误用成立方，$27\times\frac{1}{6}=4.5$ 倍，得 350%；'
               r'忘乘单价比，只看个数 9 倍，得 800%。若直接拿半径比 3 乘单价比，会得到“低 50%”，与设问矛盾，说明面积比忘了平方。'),
    dict(group=G7, seed='2023HB-70', direction='巩固',
         kaofa='靠墙围栏·周长定面积最大', technique='凑和为定值取相等', difficulty=1, time_s=45,
         stem='某社区计划利用一面足够长的围墙，用总长 60 米的栅栏围出一块矩形的共享菜园，靠墙的一边直接利用围墙，'
              '不用栅栏。这块菜园的面积最大为' + BL + '平方米。',
         options={'A': '225', 'B': '400', 'C': '450', 'D': '900'}, answer='C',
         jiexi=r'和定积最大：把面积凑成“和为定值的两数之积”。设垂直于墙的边长为 $x$ 米，则平行于墙的边长为 $(60-2x)$ 米，'
               r'面积 $S=x(60-2x)=\frac{1}{2}\cdot2x\cdot(60-2x)$。$2x$ 与 $60-2x$ 的和恒为 60，二者相等时积最大：'
               r'$2x=30$，$x=15$，$S=15\times30=450$，选 C。'
               r'结论：靠墙围矩形时，平行于墙的一边取栅栏总长的一半。'
               r'陷阱：以为三边相等最好，取 $20\times20$ 得 400；四边都按栅栏算成 $15\times15$ 得 225；'
               r'漏了一条垂直边，按 $x(60-x)$ 算得 900。'),
    dict(group=G7, seed='2024HB-64', direction='深化',
         kaofa='整米围栏·周长定面积最大', technique='整数边长取最接近', difficulty=2, time_s=70,
         stem='园林科有 46 片长 1 米的直围栏，围栏不能弯折、不能截断，可以有剩余。现要用这些围栏围出两块周长相等、'
              '互不相邻的矩形苗圃，每块苗圃四周都要围住，每条边由若干片围栏首尾相接拼成，不重叠。'
              '两块苗圃的面积之和最大为' + BL + '平方米。',
         options={'A': '30', 'B': '60', 'C': '60.5', 'D': '72'}, answer='B',
         jiexi=r'整数约束下的“周长定，面积最大”。每块最多用 $46\div2=23$ 片；每条边由整片围栏拼成，边长都是整数米，'
               r'周长 = 2×(长 + 宽) 必为偶数，所以每块周长最多 22 米，长 + 宽 = 11。和一定时两边越接近积越大，'
               r'但边长只能取整数，取 $5\times6=30$，两块共 60 平方米，选 B（剩 2 片不用）。'
               r'陷阱：取正方形 $5.5\times5.5$ 得 60.5，但 5.5 米拼不出来；每块按 24 片围成 $6\times6$ 得 72，'
               r'共需 48 片，超过 46 片；只算一块得 30。'),
    dict(group=G7, seed='考法七', direction='拓展',
         kaofa='预算约束下面积最大', technique='两部分花费相等', difficulty=2, time_s=60,
         stem='某景区计划沿一条笔直的河岸建一个矩形临时停车场，靠河的一边不设围栏；与河岸平行的一边安装铁艺围栏，'
              '每米 300 元；与河岸垂直的两边安装普通围栏，每米 200 元。若围栏总预算为 2.4 万元，'
              '则停车场的面积最大为' + BL + '平方米。',
         options={'A': '600', 'B': '1200', 'C': '1800', 'D': '2400'}, answer='B',
         jiexi=r'预算约束下的面积最大，仍是“和定积最大”。设垂直于河岸的边长 $x$ 米、平行边长 $y$ 米，'
               r'则 $400x+300y=24000$。$xy=\frac{400x\cdot300y}{120000}$，$400x$ 与 $300y$ 的和为定值，'
               r'相等时积最大：$400x=300y=12000$，$x=30$，$y=40$，面积 1200 平方米，选 B。'
               r'结论：两类围栏各花一半预算；不用此法就要列二次函数配方，耗时翻倍。'
               r'陷阱：靠河一边也装了铁艺围栏，得 600；平行边误按每米 200 元，得 1800；'
               r'垂直边只算一条，得 2400。'),
    dict(group=G5, seed='2025ZJA-66', direction='巩固',
         kaofa='梯形对角线四块·知上下求整体', technique='腰旁两块相等·对角积等', difficulty=2, time_s=50,
         stem=r'某湿地公园有一块梯形草坪 $ABCD$，$AD\parallel BC$。沿对角线 $AC$、$BD$ 各修一条小路，两条小路交于点 $O$，'
              r'把草坪分成四块。经测量，$\triangle AOD$ 区域的面积为 45 平方米，$\triangle BOC$ 区域的面积为 125 平方米。'
              r'不计小路宽度，整块草坪的面积为' + BL + '平方米。',
         options={'A': '245', 'B': '320', 'C': '340', 'D': '420'}, answer='B',
         jiexi=r'梯形被两条对角线分成四块：两腰旁的两块面积相等（$\triangle ABD$ 与 $\triangle ACD$ 同底等高，各减去 $\triangle AOD$），'
               r'且相对两块面积之积相等。所以 $S_{\triangle AOB}=S_{\triangle COD}=\sqrt{45\times125}=75$，'
               r'总面积 $45+125+75\times2=320$ 平方米，选 B。'
               r'速记：梯形面积 $=(\sqrt{45}+\sqrt{125})^2=(3\sqrt{5}+5\sqrt{5})^2=320$。'
               r'陷阱：只加了一块腰旁三角形得 245；把腰旁两块当成上下两块的平均数 85，得 340；'
               r'把面积比 9∶25 当成上下底之比，腰旁每块算成 125，得 420。'),
    dict(group=G5, seed='2026GD-41', direction='巩固',
         kaofa='对角线分四块·相对两块积相等', technique='比例平移', difficulty=3, time_s=80,
         stem='如图，某社区一块不规则的四边形空地被沿对角线修建的两条步道分成甲、乙、丙、丁四个区域。'
              '已知乙区域的面积比甲区域少 20%，丙区域比丁区域少 25 平方米，乙区域比丙区域多 20 平方米。'
              '不计步道宽度，这块空地的总面积为' + BL + '平方米。',
         options={'A': '370', 'B': '410', 'C': '495', 'D': '594'}, answer='C',
         figure_svg=fig_v08,
         jiexi=r'由图，甲与丙、乙与丁相对，相对两块面积之积相等：甲×丙 = 乙×丁，即 丁∶丙 = 甲∶乙（比例平移）。'
               r'乙比甲少 20%，甲是乙的 $\frac{1}{0.8}=1.25$ 倍，故丁是丙的 1.25 倍；丁比丙多 25，'
               r'得丙 = 100，丁 = 125，乙 = 120，甲 = 150，共 495 平方米，选 C。'
               r'取舍：想到比例平移约 60 秒可解，想不到宜先跳过。'
               r'陷阱：把“少 20%”当成甲是乙的 1.2 倍，得 594；误用“相对两块面积之和相等”'
               r'（这是平行四边形的性质，一般四边形不成立），得 410；漏加丁区得 370。'),
    dict(group=G5, seed='2026GD-41', direction='深化',
         kaofa='梯形对角线四块·上下底定份数', technique='按份数分配', difficulty=2, time_s=60,
         stem=r'某街道把一块梯形空地 $ABCD$ 改造成口袋公园，$AD\parallel BC$，上底 $AD$ 长 16 米，下底 $BC$ 长 24 米，'
              r'高 15 米。沿两条对角线修建的步道交于点 $O$，把公园分成四块。不计步道宽度，$\triangle AOB$ 这一块的面积为'
              + BL + '平方米。',
         options={'A': '72', 'B': '90', 'C': '108', 'D': '120'}, answer='A',
         jiexi=r'梯形对角线分四块，面积比为 $a^2:ab:b^2:ab$（$a$、$b$ 为上、下底）。$AD:BC=2:3$，'
               r'$\triangle AOD$、$\triangle AOB$、$\triangle BOC$、$\triangle COD$ 之比为 $4:6:9:6$，共 25 份。'
               r'梯形面积 $\frac{(16+24)\times15}{2}=300$，每份 12，$S_{\triangle AOB}=72$，选 A。'
               r'另法：$S_{\triangle ABD}=120$，$BO:BD=3:5$，得 72。'
               r'陷阱：以为对角线互相平分，取 $\frac{1}{2}S_{\triangle ABC}=90$；把 $AO:OC$ 写反成 $3:2$ '
               r'或求成 $\triangle BOC$，得 108；按上下底之比直接取梯形面积的 $\frac{2}{5}$，得 120。'),
    dict(group=G5, seed='考法五', direction='拓展',
         kaofa='对角线四块求第四块·加权产值', technique='先配对再加权求和', difficulty=2, time_s=75,
         stem='某四边形果园被沿两条对角线修建的小路分成四块，分别种植荔枝、龙眼、黄皮和杨桃，其中荔枝区与黄皮区'
              '隔着两条小路的交叉口相对。已知荔枝区 16 亩、龙眼区 12 亩、黄皮区 24 亩；荔枝、龙眼、黄皮、杨桃每亩的'
              '年产值依次为 0.8 万元、0.4 万元、0.6 万元、1 万元。不计小路占地，这个果园的年总产值为' + BL + '万元。',
         options={'A': '40', 'B': '50', 'C': '58.8', 'D': '64'}, answer='D',
         jiexi=r'先用“相对两块面积之积相等”求出第四块，再加权求和。荔枝区与黄皮区相对，则龙眼区与杨桃区相对：'
               r'杨桃区 $=16\times24\div12=32$ 亩。总产值 $=16\times0.8+12\times0.4+24\times0.6+32\times1=12.8+4.8+14.4+32=64$ 万元，选 D。'
               r'陷阱：把相邻的荔枝、龙眼当成相对，杨桃算成 $16\times12\div24=8$ 亩，得 40；把龙眼与黄皮当成相对，'
               r'杨桃算成 $12\times24\div16=18$ 亩，得 50；用每亩产值的简单平均 0.7 万元乘总面积 84 亩，'
               r'得 58.8——各块面积不同，必须加权。'),
]

out = []
for i, it in enumerate(items, 1):
    vid = f'D07-math-2-v{i:02d}'
    assert '\n' not in it['jiexi'] and not re.search(r'（[A-D]）', it['jiexi']), vid
    assert it['stem'].endswith(BL + '。') or re.search('（ ）[^（）]{1,4}。$', it['stem']), vid
    rec = {'vid': vid, 'group': it['group'], 'seed': it['seed'], 'direction': it['direction'],
           'kaofa': it['kaofa'], 'technique': it['technique'], 'difficulty': it['difficulty'],
           'time_s': it['time_s'], 'stem': it['stem'], 'options': it['options'], 'answer': it['answer'],
           'jiexi': it['jiexi'], 'figure_svg': it.get('figure_svg'), 'verify': f'{V}/{vid}.py'}
    out.append(rec)
json.dump(out, open(S + '/gen/D07_math_2.json', 'w'), ensure_ascii=False, indent=1)

if '--real' in sys.argv:
    real = [{
        'id': '2026GD-41', 'answer': 'D',
        'jiexi': r'由图，青菜与茄子、毛豆与番茄相对，相对两块面积之积相等：青菜×茄子 = 毛豆×番茄，'
                 r'即 番茄∶茄子 = 青菜∶毛豆 = 1.4（比例平移）。番茄比茄子多 40，得茄子 = 100，'
                 r'番茄 = 140，青菜 = 280，毛豆 = 200，毛豆比茄子多 100 平方米，选 D。' '\n'
                 r'也可设毛豆为 $m$，列 $1.4m(1.4m-180)=m(1.4m-140)$，解得 $m=200$。' '\n'
                 r'陷阱：相对的两块须看图找准。把青菜与毛豆当成相对，解出的面积不是整数且毛豆比茄子小；'
                 r'把青菜与番茄当成相对则无正数解。参考用时 60 秒。',
        'verify': f'{V}/real_2026GD-41.py'}]
    json.dump(real, open(S + '/gen/real_D07-math-2.json', 'w'), ensure_ascii=False, indent=1)


def vis_len(s):
    return len(re.sub(r'\\[a-zA-Z]+|[{}$^_ ]', '', s))


for r in out:
    print(r['vid'], r['answer'], 'jiexi visible(no spaces)', vis_len(r['jiexi']), '| ...' + r['stem'][-16:])
print(Counter(r['answer'] for r in out))
