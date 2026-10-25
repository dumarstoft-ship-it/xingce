import json, sys
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
def blueprint_prompt(m):
    t = json.load(open(f'{S}/tasks_in/{m}.json'))
    per = 15 if m == 'C' else 45
    if m == 'C':
        days_desc = '综合推理每天 15 题、42 天每天都有。每天的"主攻子类"是：' + '，'.join(f"第{d['day']}天{d['sub']}" for d in t['days']) + '。子类代码见 taxonomy.md 的 C01–C05。'
    else:
        days_desc = f"本模块在第 {', '.join(str(d) for d in t['days'])} 天出现，每天 {per} 题。"
    solve = [q['id'] for q in t['real'] if q['needs_self_solve']]
    pend = [q['id'] for q in t['real'] if q['answer_pending_ocr']]
    return f"""你是行测命题与教研专家。请为广东省考 42 天习题本的模块「{m} {t['name']}」画考法地图并规划各天配置。

必读（按顺序）：
1. {S}/briefs/common.md（背景、底线、排版约定）
2. {S}/briefs/blueprint.md（本任务的具体要求和交付格式）
3. {S}/taxonomy.md（模块划分与边界规则）
4. 本模块真题清单：{S}/tasks_in/{m}.json（{t['n_real']} 道，含 id、来源、难度、考法标签、官方答案、截图路径、提取文字）。文字缺公式或图时，用 Read 看截图 q_crop / s_crop / j_crop。

{days_desc}
交付：{S}/blueprints/{m}.md 和 {S}/blueprints/{m}.json（格式见 blueprint.md）。

补充说明：
- 需要你自解答案的真题（无官方答案）：{', '.join(solve) if solve else '无'}。数学题用 Python 验算，写进 json 的 self_solved。
- 以下真题的官方答案还在识别中，你不用解：{', '.join(pend) if pend else '无'}。
- 之后还会补进少量真题（扫描版卷子 OCR 中：2021 广东县级/乡镇卷、2021 四川和河北、2022 深圳、2026 贵州和河北联考），会替换后面几天的一部分改编名额，你照常规划即可。
- 考生要求改编"覆盖面更广、可以更深也可以更广、不局限于原题"，这是本任务的重点：考法清单里要主动补上题库里缺的考法，改编方向要具体、有层次。
- 第一次出现的那一天（试点周会先做这一天）请规划得特别细，idea 写到能直接出题的程度。
完成后用 python 校验 json（每天真题+改编={per}、真题不重不漏），回复一段简短汇报：考法数、各天真题/改编数量、你认为本模块最该加练的 3 个点、问题清单里的条目数。"""
if __name__ == '__main__':
    print(blueprint_prompt(sys.argv[1]))

def gen_prompt(day, part, module, groups, out_file, prefix, self_solve_ids):
    """groups: list of group titles this agent should cover"""
    bp = 'C' if part == 'zh' else module
    kind = {'math': '数学运算', 'logic': '逻辑判断', 'zh': '综合推理'}[part]
    n = 0
    plan = json.load(open(f'{S}/blueprints/{bp}.json'))
    dp = next(d for d in plan['days'] if d['day'] == day)
    for g in dp['groups']:
        if g['title'] in groups: n += sum(v['n'] for v in g.get('variants', []))
    gl = '\n'.join(f'  - {g}' for g in groups)
    ss = f"本批组里需要你写解析的自解真题：{', '.join(self_solve_ids)}（写到 {S}/gen/real_{prefix}.json）。" if self_solve_ids else ''
    return f"""你是行测命题专家。请为广东省考 42 天习题本第 {day} 天的{kind}（模块「{module}」）出改编题。

必读：
1. {S}/briefs/common.md
2. {S}/briefs/generate.md（出题要求、验算、输出格式——务必遵守）
3. 考法地图：{S}/blueprints/{bp}.md 和 {S}/blueprints/{bp}.json（找到 day={day} 的配置）
4. 种子真题截图在 {S}/crops/real2/ 下（<id>_q.png 原题，<id>_j.png 官方解析，<id>_s.png 共用材料），真题清单 {S}/tasks_in/{bp}.json

你负责第 {day} 天的这些组（标题与 json 里一致）：
{gl}
按 json 里每组 variants 的数量和 idea 出题，共 {n} 道。vid 用 "{prefix}-v01" 起连续编号；group 字段填所属组标题（原样）。{ss}
验算脚本放在 {S}/verify/ 下（文件名用 vid），verify 字段写绝对路径。
输出文件：{out_file}
完成后运行 python3 {S}/scripts/check_gen.py "{os.path.basename(out_file)}" 自检（它会重跑所有验算脚本），修到没有 PROBLEM 为止，然后按 generate.md 的要求简要汇报。"""

def review_prompt(day, part, module, q_file, key_file, out_file):
    kind = {'math': '数学运算', 'logic': '逻辑判断', 'zh': '综合推理'}[part]
    return f"""你是行测资深审题人。请盲审广东省考习题本第 {day} 天{kind}（模块「{module}」）的改编题。

必读：{S}/briefs/common.md 和 {S}/briefs/review.md（流程与输出格式）。
题目文件（无答案）：{q_file}
答案文件（做完全部题后才能打开）：{key_file}
输出：{out_file}
回复里汇报：题数、你与答案一致的题数、fix/drop 各几道及最主要的问题类型。"""
import os

def split_groups(day, part, module, k):
    bp = 'C' if part == 'zh' else module
    plan = json.load(open(f'{S}/blueprints/{bp}.json'))
    dp = next(d for d in plan['days'] if d['day'] == day)
    gs = [(g['title'], sum(v['n'] for v in g.get('variants', [])), g.get('real', [])) for g in dp['groups']]
    bins = [[] for _ in range(k)]; load = [0] * k
    for t, n, real in gs:  # keep order: fill bins sequentially to balance
        i = load.index(min(load)) if False else None
    # sequential contiguous split for coherent numbering
    total = sum(n for _, n, _ in gs); target = total / k; cur = 0; acc = 0
    for t, n, real in gs:
        if acc >= target * (cur + 1) and cur < k - 1: cur += 1
        bins[cur].append((t, n, real)); acc += n
    return [b for b in bins if b]

def self_solve_ids(module_key, real_ids):
    t = json.load(open(f'{S}/tasks_in/{module_key}.json'))
    need = {q['id'] for q in t['real'] if q['needs_self_solve']}
    return [i for i in real_ids if i in need]
