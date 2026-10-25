# Build gen/D07_math_h.json (two hardened new variants for day 7, M08 geometry)
import json, os

S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
fig2 = open(os.path.join(S, 'work_D07h', 'fig2_final.svg')).read().strip()

items = [
    {
        "vid": "D07-math-h-v01",
        "group": "考法七：几何最值入门（周长与面积互定·和定积最大）",
        "seed": "考法七",
        "direction": "深化",
        "kaofa": "面积定费用最小·取等越界取边界",
        "technique": "取离取等点最近的边界",
        "difficulty": 3,
        "time_s": 80,
        "stem": "某养殖户要在一段长 50 米的旧石墙前，用围栏围出一块面积为 600 平方米的矩形羊圈。羊圈的一边紧靠旧墙且不超出旧墙，这一边不用围栏；旧墙前方有一条与墙平行的水渠，因此羊圈的进深（垂直于旧墙的边长）不能超过 15 米。与旧墙相对的一边要安装大门，用加固围栏，每米 200 元（含大门）；另外两边用普通围栏，每米 150 元。围栏的总费用最少为（ ）元。",
        "options": {"A": "10250", "B": "12000", "C": "12500", "D": "13600"},
        "answer": "C",
        "jiexi": "卡点：取等点超出范围时，要取离它最近的边界。设沿墙边长 $y$、进深 $x$，$xy=600$，费用 $200y+300x$ 的两部分之积 $=3600$ 万为定值，各 6000 元时最省，即 $y=30$、$x=20$；但进深不能超过 15 米，取不到。可行范围 $40\\le y\\le50$，$y$ 越近 30 越省，取 $y=40$、$x=15$，$8000+4500=12500$ 元，选 C。陷阱：不查范围直接取等得 12000；以为旧墙用满最省得 13600；侧边只算一条得 10250。",
        "figure_svg": None,
        "verify": S + "/verify/D07-math-h-v01.py",
    },
    {
        "vid": "D07-math-h-v02",
        "group": "考法五：三角形面积比模型（对角线分四块·梯形四块）",
        "seed": "考法五",
        "direction": "拓展",
        "kaofa": "共角（鸟头）模型·延长三边求面积",
        "technique": "补角鸟头·夹边取整边",
        "difficulty": 2,
        "time_s": 60,
        "stem": "某新区的起步区是三角形区域 $ABC$，面积为 5 平方千米。远期规划把新区扩大为三角形区域 $DEF$（如图）：$D$、$E$、$F$ 分别在 $AB$、$BC$、$CA$ 的延长线上，且 $BD=2AB$，$CE=BC$，$AF=4CA$。按远期规划，新区的总面积为（ ）平方千米。",
        "options": {"A": "40", "B": "75", "C": "105", "D": "110"},
        "answer": "D",
        "jiexi": "卡点：外围三块各与原三角形有一组互补角，用鸟头模型：面积比 = 夹角两边之积的比，夹边取“延长段”与“原边+延长段”。如 $\\triangle DBE$：$BD=2AB$，$BE=2BC$，为 4 倍；$\\triangle ECF$ 为 $1\\times5=5$ 倍，$\\triangle FAD$ 为 $4\\times3=12$ 倍。共 $5\\times(1+4+5+12)=110$ 平方千米，选 D。陷阱：夹边只取两段延长段得 75；漏加起步区得 105；只看底边比、忽略高也变了得 40。",
        "figure_svg": fig2,
        "verify": S + "/verify/D07-math-h-v02.py",
    },
]

out = os.path.join(S, 'gen', 'D07_math_h.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=1)
print('wrote', out, len(items))
