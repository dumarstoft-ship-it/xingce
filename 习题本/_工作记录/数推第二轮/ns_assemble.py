"""数推第二轮整本：ns_set.py 出的 30 道改编题按类型轮流排（相邻两题类型不同），再插进 4 道没用过的真题，写成
make_cx.py 的输入。Usage: ns_assemble.py <ns_new_items.json> <out.json>"""
import itertools, json, random, sys

TYPES = ['多级', '作商', '倍数', '递推', '幂次', '分数', '根式', '多重', '机械']
REAL = [  # 4 道真题：盲做与官方答案一致（_工作记录/第二轮/blind_gailv_shutui.json），截图已修
    {'id': '2020ZJB-5', 'answer': 'D', 'key': '前项减后项，差是 2、3、5、7，连续质数；末项 1 可以用来验证。',
     'steps': ['42 − 40 = 2，40 − 37 = 3，37 − 32 = 5，32 − 25 = 7，下一个差是 11，所求项 25 − 11 = 14。', '验证：14 − 13 = 1，正好接上末项。'], 'traps': ''},
    {'id': '2022SZ-48', 'answer': 'C', 'key': '8 项，隔项看：奇数项 1、2、4、8 每次 ×2；偶数项 2、5、11 的差是 3、6。',
     'steps': ['括号是第 8 项，属于偶数项：2，5，11，差 3，6，下一个差是 12。', '所求项 11 + 12 = 23。'], 'traps': ''},
    {'id': '2022SZ-47', 'answer': 'C', 'key': '四位数之间看不出规律，看每一项自身：前两位 = 后两位数字的乘积。',
     'steps': ['14 = 2 × 7，27 = 3 × 9，45 = 5 × 9，32 = 4 × 8，56 = 7 × 8。', '选项里只有 2045 满足 20 = 4 × 5。'], 'traps': ''},
    {'id': '2022SZ-50', 'answer': 'B', 'key': '分子、分母分别写成幂次：分母是 1⁰、3¹、5²、7³，分子是 2⁻¹、4⁰、6¹、8²。',
     'steps': ['分母的底数 1、3、5、7，指数 0、1、2、3，下一个是 9⁴ = 6561。', '分子的底数 2、4、6、8，指数 −1、0、1、2，下一个是 10³ = 1000。所求项 1000/6561。'], 'traps': ''},
]
META = {
    'title': '数字推理第二轮',
    'intro': ('30 道新出的改编题，加 4 道第 1–14 天没用过的真题。改编题照着广东、深圳、江苏近几年的数推来出，类型打乱排。'
              '每道改编题的答案都由程序按规律算出，再用一组常见规律去拟合题干，确认没有第二种规律指向别的选项；'
              '然后找人不看答案独立做，判为送分的、不找规律也能从选项猜出来的题都重出了。'),
    'method_title': '看到数列先问三件事',
    'method': ['<b>数的大小</b>：平缓的先做差；增长快的先作商，或者看幂次；忽大忽小、项数多的，考虑隔项或分组。',
               '<b>数的样子</b>：多位数、小数先想机械划分；有分数先反约分，分子分母分开看；有根号先统一成根号。',
               '做一次看不出来，就换个方向再试，而不是在同一个方向上越做越深。'],
    'model': {'label': '规律类型速查',
              'table': [['类型', '先想到它的信号'], ['多级做差', '数列平缓地增或减'], ['作商、倍数修正', '增长快，相邻两项接近整数倍'],
                        ['递推', '做差、作商都不整齐，后项和前两三项都有关'], ['幂次修正', '数落在平方数、立方数、2 的幂附近'],
                        ['分数、根式', '有分数先反约分；有根号先统一'], ['多重数列', '项数多（7 项以上）、大小交错、有两个括号'],
                        ['机械划分', '多位数、小数，数字之间看不出大小规律']],
              'steps': []},
    'key_name': '卡点', 'draw_label': '草稿', 'draw_mm': 26}

def build(new, seed):
    """round-robin over types, so neighbours differ in kind; seed > 0 shuffles the order inside each type"""
    groups = {}
    for it in new:
        groups.setdefault(next(i for i, t in enumerate(TYPES) if t in it['label']), []).append(it)
    if seed:
        for g in groups.values(): random.Random(seed).shuffle(g)
    order = []
    while any(groups.values()):
        for k in sorted(groups):
            if groups[k]: order.append(groups[k].pop(0))
    for k, it in zip((5, 13, 21, 29), REAL):
        order.insert(k, it)
    return order

def max_run(order):
    return max(len(list(g)) for _, g in itertools.groupby(it['answer'] for it in order))

if __name__ == '__main__':
    new = json.load(open(sys.argv[1]))
    seed = next(s for s in range(1000) if max_run(build(new, s)) <= 2)  # no answer letter three times in a row
    order = build(new, seed)
    json.dump({**META, 'items': order}, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
    print(len(order), 'items, seed', seed, ''.join(it['answer'] for it in order))
