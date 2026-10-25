import json, re
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
G9 = "考法九：分类分步·多阶段流程（评审·闯关·状态转移）"
G11 = "考法十一：全概率（加权平均型）"
G12 = "考法十二：条件概率与贝叶斯（逆概率·缩小样本空间）"
G15 = "考法十五：数学期望与方案决策"

items = [
 {
  "vid": "D06-math-h-v06",
  "group": G9,
  "seed": "考法九",
  "direction": "拓展",
  "kaofa": "状态回归：领先 2 分才胜",
  "technique": "回到原状态·只看决胜轮",
  "difficulty": 3,
  "time_s": 60,
  "stem": "某区全民健身运动会网球比赛中，甲、乙的一局打成了“平分”（双方得分相同），按规则，此后一方须领先对方 2 分才能赢下这一局。已知此后每一分甲得分的概率均为 $\\frac{2}{3}$，且各分结果相互独立，则甲赢下这一局的概率为（ ）。",
  "options": {"A": "$\\frac{2}{3}$", "B": "$\\frac{20}{27}$", "C": "$\\frac{4}{5}$", "D": "$\\frac{8}{9}$"},
  "answer": "C",
  "jiexi": "卡点：平分后可能一直打下去，要看出“两分打成 1∶1 就回到原状态”。每两分为一轮：甲连得 2 分（$\\frac49$）胜，乙连得 2 分（$\\frac19$）负，否则回到平分。只看分出胜负的那一轮，甲∶乙＝4∶1，$P=\\frac45$，选 C（也可列 $P=\\frac49+\\frac49P$）。最常见的错法是读成“再先得 2 分者胜”，按三分两胜得 $\\frac{20}{27}$；用 $1-\\frac19$ 把回到平分算成甲胜得 $\\frac89$；以为等于每分得分率得 $\\frac23$。",
 },
 {
  "vid": "D06-math-h-v07",
  "group": G11,
  "seed": "2026GD-40",
  "direction": "深化",
  "kaofa": "全概率：权重随抽样对象而定",
  "technique": "按被抽对象定权重",
  "difficulty": 2,
  "time_s": 50,
  "stem": "某社区有多层住宅楼 40 栋、高层住宅楼 20 栋，多层住宅楼每栋 24 户，高层住宅楼每栋 72 户。社区正在分批推进二次供水设施改造，目前多层住宅楼中已有 80% 的楼栋完成改造，高层住宅楼中已有 95% 的楼栋完成改造。从该社区的住户中随机抽取 1 户，该户所在楼栋已完成改造的概率为（ ）。",
  "options": {"A": "85.0%", "B": "86.0%", "C": "87.5%", "D": "89.0%"},
  "answer": "D",
  "jiexi": "卡点：随机抽的是住户，权重要按户数而不是楼栋数。多层共 $40\\times24=960$ 户、高层共 $20\\times72=1440$ 户，权重为 0.4∶0.6，$P=0.4\\times80\\%+0.6\\times95\\%=89\\%$，选 D。最常见的错法是按楼栋数 40∶20 加权，得 $\\frac{32+19}{60}=85\\%$，那是“随机抽 1 栋楼”的答案；把两个比例简单平均得 87.5%；权重与比例配反得 86%。",
 },
 {
  "vid": "D06-math-h-v08",
  "group": G11,
  "seed": "考法十一",
  "direction": "拓展",
  "kaofa": "两阶段全概率：先移入再抽取",
  "technique": "盯住被抽出的那一个",
  "difficulty": 3,
  "time_s": 70,
  "stem": "某社区书屋有甲、乙两个流动书箱：甲箱中有 4 本科普读物、1 本历史读物，乙箱中有 2 本科普读物、3 本历史读物。管理员先从甲箱中随机取出 2 本书放入乙箱，随后一位居民从乙箱中随机借走 1 本书，他借走的是科普读物的概率为（ ）。",
  "options": {"A": "$\\frac{2}{5}$", "B": "$\\frac{18}{35}$", "C": "$\\frac{4}{7}$", "D": "$\\frac{3}{5}$"},
  "answer": "B",
  "jiexi": "卡点：不必按移入几本科普分类，只盯住被借走的那 1 本：它是移入书的概率为 $\\frac27$，移入书是科普的概率同甲箱，为 $\\frac45$；是乙箱原有书的概率为 $\\frac57$，科普占 $\\frac25$。$P=\\frac27\\times\\frac45+\\frac57\\times\\frac25=\\frac{18}{35}$，选 B。最常见的错法是只按最可能的“移入 2 本都是科普”算，得 $\\frac47$；忽略移入的书得 $\\frac25$；两箱比例简单平均得 $\\frac35$。",
 },
 {
  "vid": "D06-math-h-v09",
  "group": G12,
  "seed": "2022JSA-54",
  "direction": "深化",
  "kaofa": "已知至少一个：缩小样本空间",
  "technique": "满足条件的结果里重数",
  "difficulty": 2,
  "time_s": 45,
  "stem": "某区市场监管局按照“双随机、一公开”的要求，从辖区 6 家连锁超市中随机抽取 2 家开展食品安全检查。已知甲、乙两家超市中至少有一家被抽中，则甲超市被抽中的概率为（ ）。",
  "options": {"A": "$\\frac{1}{3}$", "B": "$\\frac{4}{9}$", "C": "$\\frac{5}{9}$", "D": "$\\frac{2}{3}$"},
  "answer": "C",
  "jiexi": "卡点：“只抽中甲、只抽中乙、甲乙都抽中”三类并不等可能，要在满足条件的结果里重新数。共 $C_6^2=15$ 种抽法，甲、乙都没抽中的有 $C_4^2=6$ 种，满足条件的有 9 种；其中含甲的是甲配其余 5 家之一，共 5 种。$P=\\frac59$，选 C。最常见的错法是把三类当成等可能、甲占其中两类，得 $\\frac23$；不缩小样本空间，直接算 $\\frac26=\\frac13$；只数“只抽中甲”的 4 种，得 $\\frac49$。",
 },
 {
  "vid": "D06-math-h-v10",
  "group": G15,
  "seed": "考法十五",
  "direction": "拓展",
  "kaofa": "期望决策：从后往前算",
  "technique": "节点处比较再回乘",
  "difficulty": 2,
  "time_s": 60,
  "stem": "某区举办安全生产知识竞赛，“挑战环节”的规则是：选手先答第 1 题，答错则挑战结束、不得奖金；答对可获奖金 100 元，此时可以带着 100 元结束挑战，也可以继续答第 2 题。第 2 题答对，奖金累计为 400 元；答错，奖金全部清零。选手小李答对第 1 题、第 2 题的概率分别为 0.8 和 0.3。若小李以所得奖金的期望值最大为原则作出选择，则他在挑战环节所得奖金的期望值为（ ）元。",
  "options": {"A": "96", "B": "100", "C": "120", "D": "152"},
  "answer": "A",
  "jiexi": "卡点：从后往前算，先在“答对第 1 题”这个决策点上比较，再乘到达该点的概率。答对第 1 题后：结束得 100 元，继续的期望 $0.3\\times400=120$ 元＞100 元，应继续；整体期望 $0.8\\times120=96$ 元，选 A。最常见的错法是拿整体的 $0.8\\times0.3\\times400=96$ 元和没乘 0.8 的 100 元比，误判应结束而选 100；漏乘 0.8 得 120；以为答错第 2 题仍留 100 元，得 $0.8\\times(120+70)=152$。",
 },
]
for v in items:
    v["figure_svg"] = None
    v["verify"] = f"{S}/verify/{v['vid']}.py"
    # key order as in generate.md
    order = ["vid", "group", "seed", "direction", "kaofa", "technique", "difficulty", "time_s", "stem", "options", "answer", "jiexi", "figure_svg", "verify"]
items = [{k: v[k] for k in order} for v in items]

def rend(s):
    s = re.sub(r'\\frac\{?([^{}\s])\}?\{?([^{}\s]+?)\}?(?=[$\\=+∶，。；）×])', r'\1/\2', s)
    s = re.sub(r'\\frac\{([^}]*)\}\{([^}]*)\}', r'\1/\2', s)
    s = s.replace('\\times', '×').replace('\\%', '%')
    s = re.sub(r'C_(\d)\^(\d)', r'C\1\2', s)
    return s.replace('$', '')

for v in items:
    j = v['jiexi']
    print(v['vid'], 'raw', len(j), 'rendered', len(rend(j)), '| kaofa', len(v['kaofa']), 'tech', len(v['technique']), '| stem end:', v['stem'][-8:])
    for bad in ['参考用时', '用时']:
        assert bad not in j
    assert v['stem'].rstrip('。').endswith('）') or v['stem'].rstrip('。').endswith('）元')

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'write':
        out = f'{S}/gen/D06_math_h2.json'
        json.dump(items, open(out, 'w'), ensure_ascii=False, indent=1)
        print('wrote', out)
    if len(sys.argv) > 1 and sys.argv[1] == 'show':
        for v in items: print(rend(v['jiexi'])); print()
