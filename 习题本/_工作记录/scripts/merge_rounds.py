"""按模块合订：第一轮（第 2–7 天习题本里该模块的数学运算 30 题，题号与原书一致）+ 第二轮专项本（中等题、难题），
合成一本，答案速查和解析也按这三部分排。数据直接取出书时用的 JSON（out/final/D*.json、r2/book_*.json），不重新选题。
Usage: merge_rounds.py <out_dir> [module codes, e.g. M03 M04; default: all]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_day import render_day, to_pdf
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
MODS = [('M03', '工程问题', 2), ('M04', '行程问题', 3), ('M05', '经济利润', 4), ('M06', '排列组合', 5), ('M07', '概率问题', 6), ('M08', '几何问题', 7)]
NOTE = ('第一轮是第 {d} 天习题本里的数学运算 {n1} 题，题号和原书一致，方便对照原来的笔记；第二轮是第二轮专项本的中等题和难题。'
        '题目、答案速查、解析都按“第一轮、第二轮中等题、第二轮难题”三部分排，每部分题号从 1 开始。')

def build(out_dir, only=None):
    os.makedirs(out_dir, exist_ok=True)
    for code, name, d in MODS:
        if only and code not in only: continue
        day = json.load(open(f'{S}/out/final/D{d}.json'))
        r1 = next(p for p in day['parts'] if p['title'] == '数学运算')
        assert r1['module'] == name, (code, r1['module'])
        r2 = json.load(open(f'{S}/r2/book_{code}.json'))
        parts = [dict(r1, title=f'第一轮（第 {d} 天）')] + [dict(p, title='第二轮' + p['title']) for p in r2['parts']]
        book = {'title': f'{name} · 第一轮 + 第二轮', 'subtitle': '广东省考专项 · 数学运算按模块合订', 'module_head': '模块',
                'note': NOTE.format(d=d, n1=len(r1['items'])), 'parts': parts}
        hp, pdf = f'{S}/r2/merged_{code}.html', f'{out_dir}/{name}（第一轮+第二轮）.pdf'
        render_day(book, hp); to_pdf(hp, pdf)
        print(name, [(p['title'], len(p['items'])) for p in parts], pdf)

if __name__ == '__main__':
    build(sys.argv[1], set(sys.argv[2:]) or None)
