# Build out_math_sz.jsonl / out_logic_sz.jsonl from hand classifications.
# Usage: python3 -I build_out_sz.py <cls_dir>
import json, re, sys, os, collections

D = sys.argv[1]

M, N, O = "数学运算", "数字推理", "其他"
L, T, F, A = "逻辑", "图推", "定义", "类比"
G = "分数glyph缺失"
EST = "无答案/解析，难度为估计"

# id: (kind, module, kaofa, technique, difficulty, needs_figure, incomplete, note)
MATH = {
"2020SZS-4":  (N, None, "数推-分数数列(反约分)", "反约分", 2, False, False, G),
"2020SZS-8":  (N, None, "数推-分数数列(反约分)", "反约分", 2, False, False, G),
"2020SZS-9":  (N, None, "数推-分数数列(相邻做和)", "相邻做和", 3, False, False, G),
"2020SZS-16": (M, "M04", "行程-往返变速分段等时", "方程法", 3, False, False, None),
"2020SZS-17": (M, "M13", "日期-撕日历跨月连续求和", "代入排除", 3, False, False, "题称'如下图'仅为示意，文字可解；须考虑大月31天"),
"2020SZS-18": (M, "M01", "和差倍比-总价不变降价多买", "方程/代入", 2, False, False, None),
"2020SZS-19": (M, "M06", "排列组合-两人选号差≥3", "反面计数", 2, False, False, None),
"2020SZS-20": (M, "M01", "和差倍比-三量两两和求单量", "整体加减", 2, False, False, None),
"2020SZS-21": (M, "M09", "最不利-组合数计注型+抽屉", "最不利+1", 3, False, False, "正确率19%；粉笔标排列组合，核心为最不利原则"),
"2020SZS-22": (M, "M13", "植树-环形灯笼不动点", "最小公倍数", 2, False, False, "核心为公倍数(亦可归M14)；原解析误作'彩旗'"),
"2020SZS-23": (M, "M12", "浓度-多溶液混合后蒸干", "溶质守恒方程", 3, False, False, None),
"2020SZS-24": (M, "M13", "鸡兔同笼-两级技工总产量", "假设法", 2, False, False, "粉笔标基础应用；结构为鸡兔同笼"),
"2020SZS-25": (M, "M11", "容斥-三集合标准型+比例设元", "公式+设15x", 3, False, False, None),
"2020SZS-26": (M, "M03", "工程-多门通行效率方程组", "方程组", 2, False, False, "粉笔标基础应用；效率×时间=人数"),
"2020SZS-27": (M, "M04", "行程-折返取物提速追及", "比例法", 2, False, False, None),
"2020SZS-28": (M, "M13", "钟表-外出期间成90°次数", "分时段枚举", 3, False, False, "正确率17%"),
"2020SZS-29": (M, "M03", "工程-先做后合求效率+两侧植树", "效率比+植树", 3, False, False, "粉笔标植树；末步为两侧植树(棵数−1)"),
"2020SZS-30": (M, "M09", "最值-多集合反向构造(≥3项)", "反向构造", 3, False, False, None),
"2020SZ1-45": (N, None, "数推-多级数列(做商等比)", "两两做商", 3, False, False, G),
"2020SZ1-46": (M, "M13", "时间推算-停钟未校准往返", "时间差分析", 2, False, False, "粉笔标钟表问题"),
"2020SZ1-47": (M, "M10", "统筹-双面印刷+晾干时间", "并行统筹", 3, False, False, None),
"2020SZ1-48": (M, "M04", "行程-往返+后发者相遇", "方程+代入", 3, False, False, "正确率15%"),
"2020SZ1-49": (M, "M02", "不定方程组-整体消元求差", "整体消元", 3, False, False, "正确率11%；粉笔标基础应用；'得0票'的0缺失"),
"2020SZ1-50": (M, "M09", "最不利-可重复组合计种类", "最不利+1", 3, False, False, "正确率11%；易漏同色两支"),
"2020SZ1-51": (M, "M14", "多位数-数位对调差为9倍", "整除特性", 3, False, False, "年龄情境但非年龄问题"),
"2020SZ1-52": (M, "M13", "杂题-围圈报数逢7出列", "分轮枚举", 2, False, False, "粉笔标基础计算"),
"2020SZ1-53": (M, "M14", "数论-四数两两和求最大数", "配对求总和", 2, False, False, "粉笔标最值问题"),
"2020SZ1-54": (M, "M11", "容斥-两集合比例设元", "画图+设元", 2, False, False, "题干与选项分数glyph缺失"),
"2020SZ1-55": (M, "M07", "古典概率-三数和区间反面计数", "反向枚举", 3, False, False, "正确率9%"),
"2023SZ-46":  (N, None, "数推-分数数列", "观察分子分母", 2, False, False, "分数glyph全部缺失，规律不可判；" + EST),
"2023SZ-47":  (N, None, "数推-二级等差数列", "两次做差", 1, False, False, EST),
"2023SZ-48":  (N, None, "数推-两两分组求和", "分组求和", 2, False, False, EST),
"2023SZ-49":  (N, None, "数推-数位特征(首尾和=中位)", "机械划分", 3, False, False, EST),
"2023SZ-50":  (N, None, "数推-递推(前项半+后项)", "递推观察", 2, False, False, EST),
"2023SZ-51":  (M, "M08", "立体几何-球入圆柱水面相切", "等体积+代入", 2, False, False, EST),
"2023SZ-52":  (M, "M13", "杂题-天平称假币(三分法)", "3^n≥N", 1, False, False, "找次品，也可视作统筹/最值；" + EST),
"2023SZ-53":  (M, "M04", "行程-同路程时间差取整", "直接计算", 1, False, False, EST),
"2023SZ-54":  (M, "M13", "页码-连续求和多加一页", "估算求和", 1, False, False, "亦可视作M14数列求和；" + EST),
"2023SZ-55":  (M, "M12", "混合配比-单价涨跌求配比", "十字交叉/方程", 2, False, False, "成本情境，按加权平均归M12；" + EST),
"2023SZ-56":  (M, "M04", "行程-相遇掉头等效穿过", "等效穿越", 3, False, False, EST),
"2023SZ-57":  (M, "M11", "容斥-三集合韦恩分区列方程", "画图分区", 2, False, False, EST),
"2023SZ-58":  (M, "M05", "经济-两平台计费收益方程", "方程法", 2, False, False, "亦可归M01；注意'万次'单位；" + EST),
"2023SZ-59":  (M, "M13", "星期日期-出勤天数反推星期", "整周+余数枚举", 2, False, False, EST),
"2023SZ-60":  (M, "M04", "行程-环形多人追及速度差", "速度差相减", 2, False, False, EST),
"2024SZ-51":  (M, "M01", "方程-三元一次方程组(草料)", "消元法", 2, False, False, "供需平衡但无时间维度，非牛吃草"),
"2024SZ-52":  (M, "M09", "最不利-可重复组合计种类", "最不利+1", 2, False, False, "与2020SZ1-50同型"),
"2024SZ-53":  (M, "M10", "统筹-搬运途中消耗设中转", "设中转点列式", 3, False, False, None),
"2024SZ-54":  (M, "M01", "比例-部分占比逐层逆推", "逐层除法", 1, False, False, None),
"2024SZ-55":  (M, "M06", "排列组合-无序枚举得分组合", "分类枚举", 2, True, False, "各区分值(30/25/20/15/10/5/4/1)只在飞镖盘图中，需配图或补文字"),
"2024SZ-56":  (M, "M04", "行程-环形相遇比例+追及", "比例+追及公式", 2, False, False, None),
"2024SZ-57":  (M, "M05", "经济-分段计酬(补贴/扣减)", "混合居中+代入", 3, False, False, None),
"2024SZ-58":  (M, "M11", "容斥-三集合非标准求仅一项", "非标准公式", 2, False, False, None),
"2024SZ-59":  (M, "M13", "方阵-实心空心方阵融合", "方程法", 2, False, False, None),
"2024SZ-60":  (M, "M13", "钟表-外出期间成180°次数", "角速度差计算", 3, False, False, None),
}

SEQ = "深圳事件排序题，非逻辑判断，不进习题本"
LOGIC = {
"2020SZS-31": (O, None, "事件排序-触电急救流程", "首尾句排除", 2, False, False, SEQ),
"2020SZS-32": (O, None, "事件排序-洪涝灾害救援", "首尾句排除", 1, False, False, SEQ),
"2020SZS-33": (O, None, "事件排序-庭审程序先后", "常识定序", 2, False, False, SEQ),
"2020SZS-34": (O, None, "事件排序-潮汐与自转因果", "因果链定序", 3, False, False, SEQ),
"2020SZS-35": (O, None, "事件排序-南水北调背景结果", "首尾句排除", 1, False, False, SEQ),
"2020SZS-36": (O, None, "事件排序-渔业生产到销售", "首尾句排除", 1, False, False, SEQ),
"2020SZS-37": (O, None, "事件排序-运动方式演进", "常识定序", 1, False, False, SEQ),
"2020SZS-38": (O, None, "事件排序-磁石发现到大航海", "历史常识定序", 3, False, False, SEQ),
"2020SZS-39": (O, None, "事件排序-科技薄弱到掌握主动", "因果链定序", 1, False, False, SEQ),
"2020SZS-40": (O, None, "事件排序-资本市场时间线", "时政常识定序", 3, False, False, SEQ + "；需知年份"),
"2020SZS-56": (A, None, "类比-两词-时间对应", "造句法", 1, False, False, None),
"2020SZS-57": (A, None, "类比-两词-构词结构(偏正)", "词语结构分析", 3, False, False, None),
"2020SZS-58": (A, None, "类比-成语拆分-因果对应", "拆分成语", 2, False, False, None),
"2020SZS-59": (A, None, "类比-成语-近义+程度递进", "二级辨析", 3, False, False, None),
"2020SZS-60": (A, None, "类比-两词-并列+国内外之分", "二级辨析", 2, False, False, None),
"2020SZS-61": (A, None, "类比-三词-功能对应+时间先后", "二级辨析", 3, False, False, None),
"2020SZS-62": (A, None, "类比-三词-因果+特征对应", "逐对辨析", 1, False, False, None),
"2020SZS-63": (A, None, "类比-三词-并列+地点对应", "造句法", 2, False, False, None),
"2020SZS-64": (A, None, "类比-三词-组成+种属", "集合关系判断", 1, False, False, None),
"2020SZS-65": (A, None, "类比-三词-功能+特征对应", "造句法", 1, False, False, None),
"2020SZS-66": (L, "L07", "评价-反驳策略(言行矛盾)", "识别论证手法", 3, False, False, None),
"2020SZS-67": (L, "L02", "真假-三门守卫只一可信", "假设法", 2, False, False, None),
"2020SZS-68": (L, "L01", "翻译-所有/有的+逆否递推", "递推+逆否", 2, False, False, None),
"2020SZS-70": (L, "L01", "翻译-三段论补必要前提(有的)", "三段论补全", 3, False, False, "问必要前提但为直言三段论形式推理，按边界归L01；粉笔标加强"),
"2020SZS-71": (L, "L02", "真假-矛盾+两人说谎", "找矛盾", 2, False, False, None),
"2020SZS-73": (L, "C04", "综合-得分奇偶+上限判说谎", "奇偶性+极值", 3, False, False, "问谁说假话，但无真假限定，靠奇偶与最高分判断，归C04"),
"2020SZS-75": (L, "L02", "归纳-题干支持选项(火烧面积)", "话题一致+不过度", 3, False, False, "设问'上述发现最能支持的论断'为题干→选项方向，按归纳归L02；粉笔标加强"),
"2020SZS-76": (L, "L03", "加强-排除他因(仅CPU不同)", "排除他因", 2, False, False, None),
"2020SZS-77": (L, "L04", "削弱-措施达不到目的", "否定论点", 1, False, False, None),
"2020SZS-78": (L, "C05", "综合-每人对一半+图岛匹配", "假设代入", 2, False, False, "真假限定(每人只对一半)+五岛匹配"),
"2020SZS-79": (L, "L06", "解释-赞成买国货却不自用", "调和矛盾", 2, False, False, None),
"2020SZS-80": (L, "L02", "真假-元信息推理定真凶", "假设排除", 2, False, False, "认知型真假题(据'说了/没说真假'推理)，无排序匹配"),
"2020SZ1-26": (O, None, "事件排序-歌曲年代先后", "时政常识定序", 2, False, False, SEQ),
"2020SZ1-27": (O, None, "事件排序-竹简制作工序", "首尾句排除", 2, False, False, SEQ),
"2020SZ1-28": (O, None, "事件排序-疫苗研发流程", "尾句突破", 1, False, False, SEQ),
"2020SZ1-29": (O, None, "事件排序-航海冒险因果链", "因果链定序", 1, False, False, SEQ),
"2020SZ1-30": (O, None, "事件排序-伏安法测电阻步骤", "首尾句排除", 1, False, False, SEQ),
"2020SZ1-31": (L, "L01", "翻译-三段论补必要前提(所有)", "三段论补全", 1, False, False, "问必要前提但为直言三段论形式推理，按边界归L01；粉笔标加强"),
"2020SZ1-32": (L, "L04", "削弱-他因(开业优惠广告)", "他因削弱", 3, False, False, None),
"2020SZ1-33": (L, "C02", "综合-五人五轮拿球拉丁方", "列表+选项排除", 3, False, False, "人×轮次×颜色三维匹配"),
"2020SZ1-34": (L, "C05", "综合-供词全假+进门顺序定凶", "负命题+排序", 3, False, False, "供词全假，先取负命题再排进门先后"),
"2020SZ1-35": (L, "L01", "翻译-有的命题推必然真", "有的含义辨析", 2, False, False, None),
"2020SZ1-36": (L, "L01", "翻译-条件链+事实否后", "逆否递推", 1, False, False, None),
"2020SZ1-37": (F, None, "定义-单定义选是(泡菜效应)", "找关键词", 1, False, False, None),
"2020SZ1-38": (L, "C04", "综合-四次得分和17推数字", "方程+枚举", 3, False, False, None),
"2020SZ1-39": (L, "C03", "综合-课程分上下午+节数约束", "数量突破", 3, False, False, "上午4节/下午3节名额为关键；含相邻条件"),
"2020SZ1-40": (L, "L03", "加强选非-措施类论点", "排除法", 3, False, False, "正确率5%"),
"2023SZ-31":  (O, None, "事件排序-年龄雅称先后", "常识定序", 1, False, False, SEQ + "；" + EST),
"2023SZ-32":  (O, None, "事件排序-红旗渠修建历程", "首尾句排除", 1, False, False, SEQ + "；" + EST),
"2023SZ-33":  (O, None, "事件排序-炫富举报到判刑", "因果链定序", 1, False, False, SEQ + "；" + EST),
"2023SZ-34":  (O, None, "事件排序-时政事件年份", "时政常识定序", 2, False, False, SEQ + "；" + EST),
"2023SZ-35":  (O, None, "事件排序-气象卫星工作流程", "首尾句排除", 1, False, False, SEQ + "；" + EST),
"2023SZ-36":  (L, "L03", "加强-措施可行(疗效等同)", "措施可行", 2, False, False, EST),
"2023SZ-37":  (L, "L07", "评价-论证方法(排除另一解释)", "识别论证方式", 2, False, False, EST),
"2023SZ-38":  (L, "C01", "综合-七天穿鞋间隔排序", "确定信息+代入", 2, False, False, EST),
"2023SZ-39":  (L, "C02", "综合-三人名次省份匹配", "列表排除", 1, False, False, EST),
"2023SZ-40":  (F, None, "定义-单定义选非(曲解)", "找关键词", 2, False, False, EST),
"2023SZ-41":  (L, "L01", "翻译-五环条件链+事实否后", "从事实出发", 2, False, False, EST),
"2023SZ-42":  (L, "L04", "削弱-否定论据(无需买车位)", "否定论据", 2, False, False, EST),
"2023SZ-43":  (L, "C03", "综合-开关按压状态推理", "状态回溯", 2, False, False, "开关开/关状态推理，taxonomy无专门类，按取舍组合归C03；" + EST),
"2023SZ-44":  (F, None, "定义-单定义选是(鳄鱼法则)", "找关键词", 2, False, False, EST),
"2023SZ-45":  (L, "L04", "削弱-措施无效(有因无果)", "有因无果", 2, False, False, EST),
"2024SZ-31":  (O, None, "事件排序-邹忌讽齐王纳谏", "首尾句排除", 1, False, False, SEQ),
"2024SZ-32":  (O, None, "事件排序-政企抱团引才", "因果链定序", 2, False, False, SEQ),
"2024SZ-33":  (O, None, "事件排序-核污水排海事件", "尾句突破", 2, False, False, SEQ),
"2024SZ-34":  (O, None, "事件排序-企业遭打压反击", "因果链定序", 2, False, False, SEQ),
"2024SZ-35":  (O, None, "事件排序-诗句时令先后", "诗词常识定序", 2, False, False, SEQ),
"2024SZ-36":  (L, "L01", "翻译-除非否则+否后得选言", "否后+肯前", 2, False, False, None),
"2024SZ-37":  (L, "L04", "削弱-否定论点(菜地必要性)", "否定论点", 2, False, False, None),
"2024SZ-38":  (L, "L03", "加强-搭桥(只有才翻译)", "搭桥", 2, False, False, "形式搭桥(补'想取得→想从事')，亦可作L01练习"),
"2024SZ-39":  (L, "L07", "结构-逻辑错误相似(偷换概念)", "识别谬误", 2, False, False, None),
"2024SZ-40":  (L, "C02", "综合-四饰四材质条件匹配", "假设+一一对应", 3, False, False, "条件全为假言，但须用'材质各不相同'一一对应才能解，按边界归C02"),
"2024SZ-41":  (L, "L07", "结构-三段论形式对比", "符号化对比", 2, False, False, None),
"2024SZ-42":  (L, "L06", "解释选非-付费习惯vs用户流失", "排除法", 2, False, False, None),
"2024SZ-43":  (L, "C02", "综合-认知推理(长宽唯一)", "唯一性排除", 3, True, False, "11种模具长宽规格只在图中；'谁知道'型认知推理，taxonomy无专门类，按属性匹配归C02"),
"2024SZ-44":  (L, "C05", "综合-半真话+条件定罪犯组合", "选项代入", 2, False, False, "甲一半真(甲、丁恰一人)+条件+'至少三人'，真假与组合混合；也可视作C03"),
}

MATH_KINDS = {M, N, O}
LOGIC_KINDS = {L, T, F, A, O}
MOD_OK = {M: re.compile(r"^M(0[1-9]|1[0-4])$"), L: re.compile(r"^(L0[1-7]|C0[1-5])$")}


def acc_of(jx):
    m = re.search(r"全站正确率：\s*(\d+)%", jx or "")
    return int(m.group(1)) if m else None


def exp_diff(a):
    return 1 if a >= 75 else (2 if a >= 45 else 3)


def build(src, dst, table, kinds):
    items = [json.loads(l) for l in open(src, encoding="utf-8") if l.strip()]
    ids = [d["id"] for d in items]
    assert len(set(ids)) == len(ids), "duplicate ids"
    missing = [i for i in ids if i not in table]
    extra = [k for k in table if k not in ids]
    assert not missing and not extra, (missing, extra)
    probs = []
    with open(dst, "w", encoding="utf-8") as f:
        for d in items:
            i = d["id"]
            kind, mod, kaofa, tech, diff, nf, inc, note = table[i]
            assert kind in kinds, i
            if kind in MOD_OK:
                assert mod and MOD_OK[kind].match(mod), (i, mod)
            else:
                assert mod is None, i
            assert diff in (1, 2, 3), i
            if len(kaofa) > 20 or len(tech) > 12:
                probs.append((i, "len", len(kaofa), len(tech)))
            a = acc_of(d.get("jiexi"))
            if a is not None and exp_diff(a) != diff:
                probs.append((i, "acc", a, diff))
            row = {"id": i, "kind": kind, "module": mod, "kaofa": kaofa,
                   "technique": tech, "difficulty": diff, "needs_figure": nf,
                   "incomplete": inc, "note": note}
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(os.path.basename(dst), "written", len(items), "problems:", probs)


build(os.path.join(D, "math_sz.jsonl"), os.path.join(D, "out_math_sz.jsonl"), MATH, MATH_KINDS)
build(os.path.join(D, "logic_sz.jsonl"), os.path.join(D, "out_logic_sz.jsonl"), LOGIC, LOGIC_KINDS)
