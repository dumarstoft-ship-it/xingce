"""Render the overview booklet: how to use + 42-day schedule table."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_day import CSS, esc, to_pdf, R
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'

def main(out_pdf):
    sc = json.load(open(S + '/db/schedule.json'))
    names = sc['names']
    stats = {}
    for f in os.listdir(S + '/tasks_in'):
        t = json.load(open(os.path.join(S, 'tasks_in', f)))
        stats[t['module']] = t['n_real']
    fonts = ''.join(f'<link rel="stylesheet" href="file://{R}/node_modules/@fontsource/{f}/{w}.css">' for f in ('noto-serif-sc', 'noto-sans-sc') for w in (400, 700))
    rows = ''.join(f"<tr><td>第 {d['day']} 天</td><td>{esc(d['math'])} {esc(names[d['math']])}</td><td>{esc(d['logic'])} {esc(names[d['logic']])}</td><td>{esc(names[d['zh']].replace('综合推理·', ''))}</td></tr>" for d in sc['schedule'])
    css = CSS + """
    table.sched { width: 100%; border-collapse: collapse; font-size: 9.5pt; }
    table.sched th, table.sched td { border: 1px solid #bbb; padding: 1.2mm 2mm; text-align: left; }
    table.sched th { background: #f1f1f1; font-family: 'Noto Sans SC', sans-serif; }
    table.sched tr:nth-child(7n+2) td { border-top: 2px solid #555; }
    .intro h2 { font-size: 13pt; margin: 6mm 0 2mm 0; }
    .intro p, .intro li { font-size: 10.5pt; }
    """
    h = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>使用说明</title>{fonts}<style>{css}</style></head><body>
<div class="cover"><h1>广东省考 42 天专项习题本</h1><div class="sub">数量关系（数学运算）+ 判断推理（逻辑判断、综合推理）· 使用说明与日程总表</div>
<div class="intro">
<h2>每天的内容</h2>
<ul>
<li><b>数学运算 45 题</b>：当天只练一个模块（不含数字推理），建议用时约 90 分钟。</li>
<li><b>逻辑判断 45 题</b>：当天只练一个模块（不含图推、定义、类比，广东 2024 年起不考后两者），建议用时约 45 分钟。</li>
<li><b>综合推理 15 题</b>：排序、匹配、分组、数量比较、真假综合等"组合排列"题，每天主攻一个子类，建议用时约 30 分钟。</li>
</ul>
<h2>题目来源</h2>
<ul>
<li><b>题目页只有题号</b>：不标题型、考法和出处，需要你自己判断。</li>
<li><b>真题</b>：取自你提供的 2020–2026 年广东、国考副省级、深圳、浙江、江苏、山东、四川、河北、重庆等卷子，直接截取原卷（保留原卷题号）。</li>
<li><b>改编</b>：真题不够的部分，按每个模块的"考法地图"改编：有巩固（换问法、正反推）、深化（多一步转化、考法嵌套）和拓展（新结构、跨模块、题库里少见的考法）三类，不是只换数字。数学、综合推理和翻译推理的改编题答案都经过程序验算，论证类改编题经过独立盲审。</li>
<li><b>答案与解析</b>：每天最后先给"答案速查"，再给逐题解析；解析里注明每道题的出处（真题来源与原题号 / 改编）、考法和技巧。真题用原版解析（截图）；少数没有官方解析的真题（如 2026 年卷）为自解，已注明。</li>
</ul>
<h2>使用建议</h2>
<ul>
<li>每部分整套做完再对答案；同一考法的题目大体相邻，由浅入深。</li>
<li>每道题按"参考用时"计时，超时的题在题号旁做记号，第二轮专门回看这类题的秒杀方法。</li>
<li>同一模块会间隔重复出现（数学约 3–4 次、逻辑约 6–7 次），后几次以深化和拓展为主。</li>
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
