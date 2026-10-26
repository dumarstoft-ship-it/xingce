"""Render the overview booklet: how to use + 42-day schedule table."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_day import CSS, esc, to_pdf, R
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'

def main(out_pdf):
    sc = json.load(open(S + '/db/schedule.json'))
    names = sc['names']
    plan = json.load(open(S + '/db/realonly_plan.json')) if os.path.exists(S + '/db/realonly_plan.json') else {}
    def cell(d, part, label):
        n = len(plan.get(str(d['day']), {}).get(part, []))
        if not plan: return esc(label)
        return esc(label) + ('' if n >= (20 if part == 'logic' else 5) else (f'<span class="todo">（现有 {n} 题，待补）</span>' if n else '<span class="todo">（待补）</span>'))
    fonts = ''.join(f'<link rel="stylesheet" href="file://{R}/node_modules/@fontsource/{f}/{w}.css">' for f in ('noto-serif-sc', 'noto-sans-sc') for w in (400, 700))
    rows = ''.join(f"<tr><td>第 {d['day']} 天</td><td>{esc(names[d['math']])}</td><td>{cell(d, 'logic', names[d['logic']])}</td><td>{cell(d, 'zh', names[d['zh']].replace('综合推理·', ''))}</td></tr>" for d in sc['schedule'])
    n_logic = sum(1 for d in plan.values() if len(d.get('logic', [])) >= 20)
    n_zh = sum(1 for d in plan.values() if len(d.get('zh', [])) >= 5)
    css = CSS + """
    table.sched { width: 100%; border-collapse: collapse; font-size: 9.5pt; }
    table.sched th, table.sched td { border: 1px solid #bbb; padding: 1.2mm 2mm; text-align: left; }
    table.sched th { background: #f1f1f1; font-family: 'Noto Sans SC', sans-serif; }
    table.sched tr:nth-child(7n+2) td { border-top: 2px solid #555; }
    .intro h2 { font-size: 13pt; margin: 6mm 0 2mm 0; }
    .intro p, .intro li { font-size: 10.5pt; }
    .todo { color: #b00020; font-size: 8.5pt; }
    """
    h = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>使用说明</title>{fonts}<style>{css}</style></head><body>
<div class="cover"><h1>广东省考 42 天专项习题本</h1><div class="sub">数量关系（数学运算）+ 判断推理（逻辑判断、综合推理）+ 资料分析 · 使用说明与日程总表</div>
<div class="intro">
<h2>每天的内容</h2>
<ul>
<li><b>数字推理 10 题</b>：找规律的数列与数阵题，用历年真题，题不够时轮换重做，建议用时约 10 分钟。</li>
<li><b>数学运算 30 题</b>：当天只练一个模块，建议用时约 60 分钟，做完精细复盘。</li>
<li><b>逻辑判断 20 题</b>：当天主练一个模块（不含图推、定义、类比，广东 2024 年起不考后两者），建议用时约 20 分钟。</li>
<li><b>综合推理 5 题</b>：排序、匹配、分组、数量比较、真假综合等"组合排列"题，每天主攻一个子类，建议用时约 10 分钟（第 1 天为 10 题）。</li>
<li><b>资料分析 2 套（第 4 天起）</b>：每套 4 篇 20 题，题目在单独的打印册里（纸质练），按考场节奏整套做完，每套建议约 30 分钟；答案和解析在当天的电子版习题本最后。第 2、3 天用你自己的纸质资料。</li>
</ul>
<h2>题目来源</h2>
<ul>
<li><b>题目页只有题号</b>：不标题型、考法和出处，需要你自己判断。</li>
<li><b>真题</b>：取自你提供的 2020–2026 年广东、国考副省级、深圳、浙江、江苏、山东、四川、河北、重庆、贵州等卷子，直接截取原卷（原卷题号已去掉，只保留本册题号）。原卷有遮挡、印错或截图不全的题，改为文字录入，并在解析里注明。</li>
<li><b>数学运算</b>：每道题至少有一个要想清楚的地方（一步转化、一个手法或一个陷阱），设元后一个方程、一步比例就能出的送分题已经去掉。题目有三种：真题；老师笔记精选（你提供的数量关系笔记里的例题，解析用笔记的方法，配图为本册重画，去掉了手写标注）；真题和笔记都覆盖不到的难点，按真题考法写的改编题。改编题不是只换数字，每道都练一个具体的卡点，答案由程序验算，并经过独立盲审。</li>
<li><b>逻辑判断</b>：只用真题，不改编。现有真题够排 {n_logic} 天；总表里标"待补"的天数，等你补充卷子后再排入。</li>
<li><b>综合推理</b>：真题优先，现有真题够排 {n_zh} 天；之后用改编题补齐，每道都由程序穷举验证答案唯一，并经过独立盲审。</li>
<li><b>资料分析</b>：按篇挑难的。有粉笔全站正确率的篇目直接按正确率排；没有的，逐篇评估难度（计算步数、选项接近程度、陷阱、找数难度），评估方法先在有真实正确率的篇目上校验过。只取排名靠前的难篇，重新组成每套 4 篇；国考副省级和地市级重复的篇目只用一次，广东 2024–2026 年卷留作整套模考。</li>
<li><b>答案与解析</b>：每天最后先给"答案速查"，再给逐题解析，解析里注明每道题的出处、考法和技巧。真题用原版解析（截图）。没有官方答案的真题（如 2026 年国考、广东、浙江卷），答案和解析为自解，由两人分别独立求解，核对一致后才采用；这类题在解析里都已注明。</li>
</ul>
<h2>使用建议</h2>
<ul>
<li>每部分整套做完再对答案；同一考法的题目大体相邻，由浅入深。</li>
<li>数学改编题的解析末尾有"参考用时"，超时的题在题号旁做记号，第二轮专门回看这类题的快速解法。</li>
<li>同一模块会间隔重复出现（数学约 2–4 次、逻辑约 4–7 次），数学后几次以深化和拓展为主。</li>
</ul>
</div></div>
<div class="part"><div class="part-h"><span>42 天日程总表</span><span class="meta">每 7 天一条粗线</span></div>
<table class="sched"><tr><th>日期</th><th>数学运算模块</th><th>逻辑判断模块</th><th>综合推理子类</th></tr>{rows}</table></div>
</body></html>"""
    hp = out_pdf[:-4] + '.html'
    open(hp, 'w').write(h)
    to_pdf(hp, out_pdf)
    print('ok', out_pdf)

if __name__ == '__main__':
    main(sys.argv[1])
