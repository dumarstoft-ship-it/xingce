# Build out_logic_2.jsonl from hand classifications (one row per input id).
import json, sys

SRC = sys.argv[1]
DST = sys.argv[2]

L, T, D, A = "逻辑", "图推", "定义", "类比"

# id: (kind, module, kaofa, technique, difficulty, needs_figure, incomplete, note)
C = {
"2021SC2-80": (L, "L03", "加强-补充论据(无因无果)", "无因无果", 2, False, False, ""),
"2021SC2-81": (L, "L04", "削弱-否定论点", "否定论点", 2, False, False, ""),
"2021SC2-82": (L, "L04", "削弱-他因削弱", "他因", 2, False, False, "C项(范围拆桥)为强干扰"),
"2021SC2-83": (L, "L01", "翻译-只有才+否后推否前", "逆否等价", 1, False, False, "题干中夹页码噪声"),
"2021SC2-84": (L, "L06", "解释-认识差异(比较vs绝对)", "调和矛盾", 2, False, False, ""),
"2021SC2-85": (L, "C01", "综合-三人三天昼夜排班约束", "代入排除", 3, False, False, "天×班次排班表，也可视作C02"),
"2021GK-81":  (T, None, "立体-多面体切割三等分", "空间重构", 3, True, False, "立体图形题，缺图"),
"2021GK-106": (L, "L04", "削弱-措施无法达到目的", "否定论点", 1, False, False, ""),
"2021GK-107": (L, "L04", "削弱-胶原蛋白为深层原因", "否定论点", 2, False, False, "答案缺,按C归;文本末尾混入另一题(108)问句+选项,需清理"),
"2021GK-109": (L, "L03", "加强-搭桥(防晒霜入海→珊瑚)", "搭桥", 2, False, False, "答案缺,按A(搭桥)归;C为重复论据干扰"),
"2021GK-110": (L, "L03", "加强-补充论据(吸引客流)", "补充论据", 1, False, False, ""),
"2021GK-111": (L, "L03", "加强-搭桥(成分↔认知障碍)", "搭桥", 2, False, False, ""),
"2021GK-112": (L, "L05", "前提-搭桥(证据→陨石撞击)", "搭桥", 1, False, False, ""),
"2021GK-113": (L, "L06", "解释-矛盾现象(政策失效原因)", "调和矛盾", 2, False, False, ""),
"2021GK-114": (L, "C01", "综合-八人排房间隔约束", "代入排除", 3, False, False, ""),
"2021GK-115": (L, "L04", "削弱-他因削弱", "他因", 1, False, False, ""),
"2021SD-51":  (D, None, "定义-成语释义选是", "找关键词", 1, False, False, "山东卷成语释义题"),
"2021SD-59":  (A, None, "类比-地点-行为-对象", "造句法", 1, False, False, ""),
"2021SD-60":  (A, None, "类比-三词并列(金属)", "并列细分", 2, False, False, ""),
"2021SD-66":  (L, "L02", "真假-找矛盾+至多一假", "找矛盾", 2, False, False, "名次情境但核心是矛盾"),
"2021SD-67":  (L, "L04", "削弱-否定解释机制", "否定原因", 2, False, False, ""),
"2021SD-68":  (L, "L03", "加强-对照组(无因无果)", "无因无果", 2, False, False, "答案缺,按A(对照)归"),
"2021SD-69":  (L, "L01", "翻译-两个多数重叠推有的", "集合重叠", 2, False, False, ""),
"2021SD-70":  (L, "L04", "削弱-他因(非唯一原因)", "他因", 1, False, False, ""),
"2021SD-71":  (L, "C05", "综合-预测真假+身份匹配", "假设+矛盾", 2, False, False, ""),
"2021SD-72":  (L, "L04", "削弱-因果倒置", "因果倒置", 2, False, False, ""),
"2021SD-73":  (L, "L01", "翻译-补前提得结论(所有递推)", "递推+逆否", 1, False, False, "问补前提但为形式推理,按边界归L01"),
"2021SD-74":  (L, "L03", "加强-补充论据(火星环境)", "补充论据", 1, False, False, ""),
"2021SD-75":  (L, "L03", "加强-反方原因由本因导致", "因果链搭桥", 2, False, False, ""),
"2021JSA-67": (A, None, "类比-组成关系(首领-群体)", "造句法", 1, False, False, ""),
"2021JSA-68": (A, None, "类比-必要条件关系", "造句法", 2, False, False, ""),
"2021JSA-69": (A, None, "类比-原材料+种属", "逐对验证", 1, False, False, ""),
"2021JSA-70": (A, None, "类比-一词多义+种属", "一词多义", 2, False, False, ""),
"2021JSA-71": (A, None, "类比-交叉+种属", "逐对验证", 2, False, False, ""),
"2021JSA-72": (A, None, "类比-动宾+目的对应", "造句法", 2, False, False, ""),
"2021JSA-73": (A, None, "类比-职责+目的对应", "造句法", 2, False, False, "末尾混入下一题(填空型)选项"),
"2021JSA-91": (L, "L01", "翻译-唯有才+肯前推肯后", "肯前否后", 1, False, False, ""),
"2021JSA-93": (L, "L03", "加强-补充论据(目的推断)", "补充论据", 3, False, False, "正确率14%"),
"2021JSA-94": (L, "C05", "综合-预言真假+职业匹配", "假设+选项排除", 2, False, False, ""),
"2021JSA-95": (L, "L04", "削弱选非-排除反向论据", "排除法", 2, False, False, ""),
"2021JSA-96": (L, "L04", "削弱-否定论点(演化未中断)", "否定论点", 2, False, False, ""),
"2021JSA-97": (L, "L01", "翻译-补条件得结论(或+逆否)", "递推+逆否", 2, False, False, "问所需前提但为形式推理,按边界归L01"),
"2021JSA-98": (L, "L03", "加强-补充论据(解释原因)", "补充论据", 1, False, False, "文本末尾附99-100题共享材料(隧道),需剥离"),
"2021JSA-99": (L, "C05", "综合-一拖二隧道南北排序", "画图+代入", 3, False, True, "材料在2021JSA-98文本末尾;一拖n按表归C05,核心为C01排序"),
"2021JSA-100": (L, "C05", "综合-一拖二隧道排序附加条件", "画图+代入", 2, False, True, "材料在2021JSA-98文本末尾;一拖n按表归C05,核心为C01排序"),
"2021JSA-101": (D, None, "定义-单定义选非", "找关键词", 1, False, False, ""),
"2021JSA-102": (D, None, "定义-单定义选是", "找关键词", 1, False, False, ""),
"2021JSA-103": (D, None, "定义-单定义选非", "找关键词", 3, False, False, "正确率39%"),
"2021JSA-104": (D, None, "定义-单定义选是", "找关键词", 3, False, False, "正确率8%"),
"2021JSA-105": (D, None, "定义-单定义选是", "找关键词", 1, False, True, "B项残缺、D项缺失"),
"2021JSA-106": (D, None, "定义-单定义选是(诗词化用)", "找关键词", 1, False, False, ""),
"2021JSA-107": (D, None, "定义-单定义选是", "找关键词", 1, False, False, ""),
"2021JSA-108": (D, None, "定义-单定义选非", "找关键词", 2, False, False, ""),
"2021JSA-109": (D, None, "定义-单定义选非", "找关键词", 1, False, True, "B项开头缺失"),
"2021JSA-110": (D, None, "定义-单定义选非", "找关键词", 2, False, False, ""),
"2021JSA-111": (D, None, "定义-单定义选是", "找关键词", 2, False, True, "D项缺失"),
"2021JSA-112": (D, None, "定义-单定义选是", "找关键词", 1, False, False, ""),
"2021JSA-113": (D, None, "定义-单定义选非", "找关键词", 1, False, False, ""),
"2021JSA-114": (D, None, "定义-单定义选非(诗句)", "找关键词", 1, False, False, ""),
"2021JSA-115": (D, None, "定义-单定义选是", "找关键词", 1, False, False, ""),
"2021ZJA-85": (T, None, "立体拼合-三块组长方体", "数块+分层", 2, True, False, "立体拼合题，缺图"),
"2021ZJA-106": (L, "C02", "综合-人书专题数三维匹配", "最大信息突破", 2, False, False, ""),
"2021ZJA-107": (L, "L04", "削弱-拆桥(初雪与冬温无关)", "拆桥", 2, False, False, ""),
"2021ZJA-108": (L, "L04", "削弱-他因削弱", "他因", 1, False, False, ""),
"2021ZJA-109": (L, "L04", "削弱-他因削弱(价格上涨)", "他因", 1, False, False, ""),
"2021ZJA-110": (L, "L04", "削弱-否定论点(事实反驳)", "否定论点", 1, False, False, ""),
"2021ZJA-111": (L, "L03", "加强-补充论据(化石证据)", "补充论据", 1, False, False, ""),
"2021ZJA-112": (L, "L04", "削弱选非-排除无关项", "排除法", 1, False, False, ""),
"2021ZJA-113": (L, "L04", "削弱选非-个案推广", "排除法", 1, False, False, ""),
"2021ZJA-114": (L, "L04", "削弱-措施达不到目的", "否定论点", 1, False, False, ""),
"2021ZJA-115": (L, "L03", "加强选非-话题偏差(品质≠产量)", "排除法", 2, False, False, ""),
"2022SC1-71": (A, None, "类比-俗语语义对应", "逐对验证", 2, False, False, ""),
"2022SC1-72": (A, None, "类比-手段-行为-结果", "造句法", 2, False, False, ""),
"2022SC1-73": (A, None, "类比-三级种属", "逐级验证", 2, False, False, ""),
"2022SC1-74": (A, None, "类比-填空型对应", "代入造句", 2, False, False, ""),
"2022SC1-76": (L, "L07", "结构-条件递推形式对比", "符号化对比", 2, False, False, ""),
"2022SC1-77": (L, "L04", "削弱-否定论点(实验证据)", "否定论点", 1, False, False, ""),
"2022SC1-78": (L, "L04", "削弱-否定论点", "否定论点", 2, False, False, "答案缺;B(否定论点)或D(举反例)存疑"),
"2022SC1-79": (L, "L01", "翻译-只有才+肯前推出", "肯前否后", 1, False, False, ""),
"2022SC1-80": (L, "L04", "削弱选非-排除他因项", "排除他因", 2, False, False, ""),
"2022SC1-81": (L, "L05", "前提-搭桥(埋藏相↔生态气候)", "搭桥", 2, False, False, ""),
"2022SC1-83": (L, "L03", "加强-补充论据(实例对比)", "补充论据", 2, False, False, ""),
"2022SC1-84": (L, "C03", "综合-七人评优数量+条件", "假设法", 2, False, False, ""),
"2022SC1-85": (L, "C05", "综合-真假话+获奖数代入", "代入排除", 2, False, False, ""),
"2022SC2-76": (L, "L03", "加强-补充论据(必要性)", "补充论据", 2, False, False, ""),
"2022SC2-77": (L, "L03", "加强-搭桥(看手机↔没动感)", "搭桥", 1, False, False, ""),
"2022SC2-78": (L, "L03", "加强-补充论据(举例说明)", "补充论据", 2, False, False, ""),
"2022SC2-79": (L, "L04", "削弱-否定论点(不可一刀切)", "否定论点", 2, False, False, ""),
"2022SC2-80": (L, "L02", "归纳-日常结论(比较推出)", "排除无中生有", 1, False, False, ""),
"2022SC2-81": (L, "L04", "削弱选非-排除无关项", "排除法", 1, False, False, ""),
"2022SC2-82": (L, "L04", "削弱选非-找支持/无关项", "排除法", 2, False, False, ""),
"2022SC2-83": (L, "L03", "加强-补充论据", "补充论据", 1, False, False, ""),
"2022SC2-84": (L, "C02", "综合-三人籍贯学科三维匹配", "最大信息突破", 2, False, False, ""),
"2022SC2-85": (L, "L07", "结构-论证结构对比", "抽象结构对比", 2, False, False, ""),
"2022GK-106": (L, "L03", "加强选非-排除话题偏差", "排除法", 1, False, False, ""),
"2022GK-107": (L, "L04", "削弱-否定论点(性能不达标)", "否定论点", 1, False, False, ""),
"2022GK-108": (L, "L01", "翻译-才字结构+否后推否前", "逆否等价", 2, False, False, ""),
"2022GK-109": (L, "L02", "真假-矛盾+只有一真", "找矛盾", 2, False, False, ""),
"2022GK-110": (L, "L05", "前提-搭桥(标注要点↔效果)", "搭桥", 2, False, False, ""),
"2022GK-111": (L, "L01", "翻译-补条件得结论(递推链)", "递推+逆否", 2, False, False, "柜子-矿物情境但为纯条件递推,按边界归L01"),
"2022GK-112": (L, "L03", "加强-搭桥(农田变化→熊蜂)", "搭桥", 2, False, False, ""),
"2022GK-113": (L, "L03", "加强选非-找削弱项", "排除法", 2, False, False, ""),
"2022GK-114": (L, "L04", "削弱-他因削弱(价格)", "他因", 1, False, False, ""),
"2022GK-115": (L, "L04", "削弱-多项计数(他因)", "他因", 2, False, False, ""),
"2022SD-54":  (D, None, "定义-多定义选是(君臣佐使)", "找关键词", 2, False, False, ""),
}

ids = [json.loads(l)["id"] for l in open(SRC, encoding="utf-8") if l.strip()]
missing = [i for i in ids if i not in C]
extra = [k for k in C if k not in ids]
assert not missing and not extra, (missing, extra)
assert len(set(ids)) == len(ids), "duplicate ids in input"

bad = []
with open(DST, "w", encoding="utf-8") as f:
    for i in ids:
        kind, module, kaofa, tech, diff, nf, inc, note = C[i]
        assert (module is None) == (kind != L), i
        assert diff in (1, 2, 3), i
        if len(kaofa) > 20 or len(tech) > 12:
            bad.append((i, len(kaofa), len(tech)))
        row = {"id": i, "kind": kind, "module": module, "kaofa": kaofa,
               "technique": tech, "difficulty": diff, "needs_figure": nf,
               "incomplete": inc}
        if note:
            row["note"] = note
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("written", len(ids), "length violations:", bad)
