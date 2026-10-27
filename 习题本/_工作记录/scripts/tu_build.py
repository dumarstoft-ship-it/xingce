"""图推固定题型专项本: the checked candidates (tu/check_*.json) grouped by type, one chapter each,
广东 / 国考 / other provinces and newest first, each chapter's 解析 opening with the methods its official 解析 use; the same question printed in two or
three papers (tu/twins.json) appears once. Writes tu/tu_book.json and the PDF.
Usage: tu_build.py <out.pdf>"""
import json, os, re, sys, glob, itertools
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
TYPES = ['折纸盒与六面体', '视图', '截面与切割', '立体拼合与补形', '平面拼合与分割', '折纸与剪纸', '立体识别']  # chapter order
# each chapter's 解析 opens with the methods its own official 解析 use: (name, pattern counted in the 解析 text, the rule)
METHODS = {
    '折纸盒与六面体': [
        ('相对面', r'相对面', '展开图里同一行或同一列隔一个面的两面相对，Z 字形两端的两面也相对；相对的两面在立体图上不会同时出现。'),
        ('公共边 / 画边', r'公共边|画边', '展开图里构成直角的两条边，折起来是同一条边；在展开图和选项上标出同一条边，比较它两侧的图案。'),
        ('公共点 / 时针', r'公共点|时针', '三个面交于一点时，按相同的起点、相同的路径画时针，展开图和选项的转向必须一致。'),
        ('标号 / 箭头', r'标号|编号|箭头', '先给各面标号，有方向的图案画箭头，再逐项核对相邻关系和方向。')],
    '视图': [
        ('观察方向', r'主视图|正视图|俯视图|左视图|后视图|视图', '主视图（正视图）从前往后看，俯视图从上往下看，左视图从左往右看；“从任一角度观看”就按前、后、左、右、上、下六个方向分别去想。'),
        ('实线与虚线', r'虚线|实线|看不到|看得到|看不见|看得见', '看得见的轮廓线画实线，看不见的画虚线；选项里多一条线、少一条线都要核对。')],
    '截面与切割': [
        ('截面的边', r'截面|切面|剖面', '截面的每条边都落在立体的某个面上：切到平面得到直线段，切到曲面一般得到曲线（顺着圆柱、圆锥的母线切时是直线）。'),
        ('空心与挖空', r'空心|挖', '空心或挖空的立体，要看切面有没有穿过空的部分：穿过时截面中间会出现空洞，或者被分成几块。')],
    '立体拼合与补形': [
        ('数块数', r'块数|个数|\d+\s*个', '先数小正方体的个数：各部分的块数加起来要等于整体，补形题是整体减去已给的部分。'),
        ('特殊部分', r'特殊|凸|凹|突出|最高|最长', '再找特殊部分：凸出、凹进、最高或最长的那一列只能由某一块提供，先定它的位置。'),
        ('转动', r'旋转|翻转|转动', '零件通常可以转动方向后再拼（题目另有说明的除外），比对时把选项在脑中转一转。')],
    '平面拼合与分割': [
        ('平行且等长相消', r'平行且等长|等长|相消', '拼在一起的两条边平行且等长，可以消去；消去后剩下的轮廓应与正确选项一致。'),
        ('平移 / 旋转', r'平移|旋转|翻转', '题目说“只能平移”时不能旋转、翻转，每块的朝向要和原图一致。'),
        ('面积 / 格数', r'面积|格数|小方格|块数', '有方格的可以先数格数或比较面积，排除总量不对的选项。')],
    '折纸与剪纸': [
        ('逆向展开', r'展开|对称|折痕|翻折|折叠', '按折叠的相反顺序一步步展开：每展开一次，剪出的图形关于这一次的折痕对称地多出一份。'),
        ('重叠部分', r'重叠|投影|面积', '求折叠后的面积时，叠在一起的部分只算一次。')],
    '立体识别': [
        ('特征位置', r'特殊|相对|相邻|位置|方向', '抓一个特征最明显的面或点，看它和周围面的位置关系在各选项中是否保持不变。')],
}
TWINS = S + '/tu/twins.json'
FIX = S + '/tu/fixes.json'  # hand decisions after the check: {id: {"drop": reason} | {"answer": X} | {"type": ...}}

def dhash(path, n=16):
    """difference hash of the question crop (figures dominate it), for spotting the same question in two papers"""
    g = np.asarray(Image.open(path).convert('L').resize((n + 1, n)), dtype=np.int16)
    return (g[:, 1:] > g[:, :-1]).flatten()

def acc_of(c):
    m = re.search(r'全站正确率[：:]\s*(\d+)%', c.get('jiexi_raw') or '')
    return int(m.group(1)) if m else None

def collect():
    cands = {c['id']: c for c in json.load(open(S + '/tu/candidates.json'))}
    fixes = json.load(open(FIX)) if os.path.exists(FIX) else {}
    keep, dropped = {}, []
    for f in sorted(glob.glob(S + '/tu/check_*.json')):
        for ck in json.load(open(f)):
            c = dict(cands[ck['id']]); c.update(ck); c.update(fixes.get(c['id'], {}))
            ans = c.get('answer') or c.get('jiexi_answer')
            if c.get('drop') or c['type'] not in TYPES or not ans or not c.get('q_ok', True):
                dropped.append((c['id'], c.get('drop') or ('非固定' if c['type'] not in TYPES else ('无答案' if not ans else c.get('q_problem'))))); continue
            c['final_answer'] = ans; c['acc'] = acc_of(c)
            keep[c['id']] = c
    # one copy of a question printed in two or three papers (groups confirmed by eye in tu/twins.json, preferred copy first)
    for g in json.load(open(TWINS))['groups']:
        have = [i for i in g if i in keep]
        if len(have) < 2: continue
        main = keep[have[0]]
        for i in have[1:]:
            t = keep.pop(i)
            dropped.append((i, f'与 {main["id"]} 同题'))
            if not (main.get('j_img') and main.get('j_ok', True)) and t.get('j_img') and t.get('j_ok', True):
                main['j_img'], main['j_ok'] = t['j_img'], True  # the other paper's 解析 is the same text
            main.setdefault('twins', []).append(f"{t['paper_name']} 第{t['num']}题")
    out = list(keep.values())
    # warn about look-alike crops that are not in a confirmed group (to be checked by eye and added to twins.json)
    hs = {c['id']: dhash(c['q_img']) for c in out}
    for a, b in itertools.combinations(out, 2):
        if a['paper'] != b['paper'] and np.count_nonzero(hs[a['id']] != hs[b['id']]) <= 12:
            print('look-alike, check by eye:', a['id'], b['id'])
    return out, dropped

def item(c):
    label = f"{c['paper_name']} 第{c['num']}题" + (f"（另见{'、'.join(c['twins'])}）" if c.get('twins') else '')
    if c['acc'] is not None: label += f" · 全站正确率 {c['acc']}%"
    it = {'type': 'real', 'id': c['id'], 'src_label': label, 'q_img': c['q_img'], 'answer': c['final_answer'], 'kaofa': None, 'technique': None}
    if c.get('j_parts'): it['jiexi_imgs'] = c['j_parts']  # a long 解析 cut at its page breaks (tu_jfix.py)
    elif c.get('j_img') and c.get('j_ok', True): it['jiexi_img'] = c['j_img']
    else: it['jiexi_text'] = c.get('jiexi_text') or '（原卷解析缺失或截图有缺陷，本题只给答案。）'
    for k in ('extra', 'jiexi_pre'):
        if c.get(k): it[k] = c[k]
    return it

def order(c):
    """广东 first, then 国考, then the other provinces; newest year first (most papers carry no 正确率 to sort by)"""
    p = c['paper']
    return (0 if 'GD' in p else 1 if p[4:6] == 'GK' else 2, -int(p[:4]), p, c['num'])

def intro(t, cs):
    raw = {r['id']: r for r in json.load(open(S + '/db/real_raw.json'))}
    lines = [f'本章 {len(cs)} 题。下面是本章官方解析里用到的方法，括号里是用到它的题数，做完对照解析时再看：']
    for name, pat, rule in METHODS[t]:
        n = sum(1 for c in cs if re.search(pat, raw[c['id']].get('jiexi_raw') or ''))
        if n: lines.append(f'· {name}（{n} 题）：{rule}')
    return '\n'.join(lines)

if __name__ == '__main__':
    out_pdf = sys.argv[1]
    qs, dropped = collect()
    parts = []
    for t in TYPES:
        cs = sorted([c for c in qs if c['type'] == t], key=order)
        if not cs: continue
        parts.append({'title': f'第 {len(parts) + 1} 章', 'module': t, 'time_min': len(cs), 'count_text': f'{len(cs)} 题（真题）',
                      'items': [item(c) for c in cs], 'ana_intro': intro(t, cs)})
    n = sum(len(p['items']) for p in parts)
    book = {'day': 0, 'title': '图形推理 · 空间类固定题型专项', 'module_head': '题型',
            'subtitle': '广东省考专项 · 全部为历年真题（国考、广东和各省卷）',
            'note': f'本册收录历年真题里的空间类固定题型共 {n} 道，按题型分 {len(parts)} 章。每章先放广东真题，再放国考，再放各省真题，同一类按年份由近到远。'
                    '不用每天练，按章做：每题限时 1 分钟，做完一章再对答案。每章解析前列出本章官方解析用到的方法。'
                    '题目用原卷的图，答案和解析为官方答案和原卷解析（粉笔题库收录的题在出处后附全站正确率）；同一道题出现在几份试卷里的只收一次，在出处后注明。',
            'parts': parts}
    json.dump({'book': book, 'dropped': dropped}, open(S + '/tu/tu_book.json', 'w'), ensure_ascii=False, indent=1)
    print('questions', n, [(p['module'], len(p['items'])) for p in parts], 'dropped', len(dropped))
    from render_day import render_day, to_pdf
    hp = out_pdf[:-4] + '.html'
    render_day(book, hp); to_pdf(hp, out_pdf)
    from shrink_pdf import shrink
    shrink(out_pdf, out_pdf + '.tmp'); os.replace(out_pdf + '.tmp', out_pdf)
    print('ok', out_pdf)
