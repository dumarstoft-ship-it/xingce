"""第二轮数学运算专项本（行程、排列组合、概率、几何）: unused medium and hard questions — real questions of difficulty
2–3 and teacher-bank 中等/难, deduplicated against everything already printed, 2024–2026 广东 kept back for the full
mock exams — split into 中等题 and 难题 with 考法 mixed inside each part. Every real question was blind-solved and checked
against its official answer (r2/blind_*.json); crop repairs are in db/overrides.json, retyped stems, a corrected answer
and notes under the 解析 in db/real_overrides.json. Usage: r2_build.py <out_dir>"""
import hashlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import assemble_day as A
import crop as C
from render_day import render_day, to_pdf
from PIL import Image
S, CR = A.S, A.CR
MODS = [('M04', '行程问题'), ('M06', '排列组合'), ('M07', '概率问题'), ('M08', '几何问题')]
FIGURE = ['2022JSA-59', '2022JSA-67']  # stems retyped (garbled letters in the original): keep the original figure
NOTE = ('题目都是第 1–14 天没用过的真题和老师笔记精选，去掉了送分题，按难度分成中等题和难题两部分，同一部分里考法打乱排。'
        '每道真题都由一位不看答案的解题者独立做过，再和官方答案核对；原卷截图有缺损的已经补截或重新排了题干，'
        '官方解析有笔误、缺字的，在解析下面加了“补充”。2024–2026 年的广东真题留作最后的整套模考，这里没有收。')

def figure_html(db, qid):
    """the largest picture inside the question's region, cropped on its own"""
    r = db[qid]
    page, (t, b) = next(iter(r['regions'].items()))
    P = C.page_lines(r['qfile'], int(page)); dy = C.doc_offset(r['qfile'])
    ims = [im for im in P['images'] if t - 5 <= im['top'] - dy <= b + 5]
    big = max(ims, key=lambda im: (im['x1'] - im['x0']) * (im['bottom'] - im['top']))
    out = f'{CR}/{qid}_figq.png'
    C.crop(r['qfile'], {page: [round(big['top'] - dy - 2, 1), round(big['bottom'] - dy + 2, 1)]}, out)
    im = Image.open(out)  # the band spans the page: trim it to the figure's ink
    box = Image.eval(im.convert('L'), lambda v: 255 if v < 200 else 0).getbbox()
    im.crop((max(0, box[0] - 6), max(0, box[1] - 6), min(im.width, box[2] + 6), min(im.height, box[3] + 6))).save(out)
    qj = f'{CR}_nonum/{qid}_q.png.json'  # a bare figure has no text to size by: print it at the question crop's scale
    sc = json.load(open(qj)).get('scale', 1.0) if os.path.exists(qj) else 1.0
    return f'<img class="crop" src="file://{out}" style="width:{Image.open(out).size[0] / 200 * sc:.3f}in">'

def count(items):
    nr = sum(1 for it in items if it['type'] == 'real'); nt = len(items) - nr
    return f'{len(items)} 题（真题 {nr}' + (f'，老师精选 {nt}' if nt else '') + '）'

def shuffled(items):
    """a fixed order that mixes 考法 (so it is the same on every rebuild)"""
    return sorted(items, key=lambda it: hashlib.md5((it.get('id') or it.get('tid')).encode()).hexdigest())

def build(out_dir):
    db, fix = A.load_db(); cls = A.load_cls(); tb = A.teacher_bank()
    sel = json.load(open(S + '/r2/selection.json'))
    os.makedirs(out_dir, exist_ok=True)
    for code, name in MODS:
        mid, hard = [], []
        for qid in sel[code]['real']:
            it = A.real_item(qid, db, fix, cls)
            if qid in FIGURE:
                it['figure'] = figure_html(db, qid)
            (hard if cls[qid].get('difficulty') == 3 else mid).append(it)
        for tid in sel[code]['teacher']:
            (hard if tb[tid].get('level') == '难' else mid).append(A.teacher_item(tid))
        mid, hard = shuffled(mid), shuffled(hard)
        day = {'title': f'第二轮 · {name}', 'subtitle': '广东省考专项 · 数学运算第二轮（中等题和难题）', 'module_head': '模块', 'note': NOTE,
               'parts': [{'title': '中等题', 'module': name, 'time_min': round(1.5 * len(mid)), 'items': mid, 'count_text': count(mid)},
                         {'title': '难题', 'module': name, 'time_min': round(2.5 * len(hard)), 'items': hard, 'count_text': count(hard)}]}
        json.dump(day, open(f'{S}/r2/book_{code}.json', 'w'), ensure_ascii=False, indent=1)
        hp, pdf = f'{S}/r2/book_{code}.html', f'{out_dir}/第二轮_{name}.pdf'
        render_day(day, hp); to_pdf(hp, pdf)
        print(name, '中等', len(mid), '难题', len(hard), pdf)

if __name__ == '__main__':
    build(sys.argv[1])
