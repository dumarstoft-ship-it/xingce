"""Prompts for passage-difficulty rating agents (资料分析)."""
import json, os, sys
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
OUT = S + '/crops/zl'
raw = json.load(open(S + '/db/zl_raw.json'))
def imgs(mat):
    rs = sorted([r for r in raw if r['mat'] == mat], key=lambda r: r['pos'])
    first = rs[0]['id']
    from PIL import Image
    from zl_crop import chunk_files
    ps = [f for f in chunk_files(first) if Image.open(f).size[1] >= 20]
    return ps, [f"{OUT}/{r['id']}_q.png" for r in rs]
def block(mat, label, acc=None):
    ps, qs = imgs(mat)
    s = f'### {label}' + (f'  (KNOWN 全站正确率 by question: {acc})' if acc else '') + '\n'
    s += 'Material images (read in order): ' + ', '.join(ps) + '\n'
    s += 'Question images (Q1..Q5 in order): ' + ', '.join(qs) + '\n'
    return s
HEAD = """You are an experienced 行测 资料分析 teacher. A student preparing for a Chinese provincial civil-service exam wants
ONLY the hardest 资料分析 passages for practice. Your job: estimate how hard each passage below is, passage by passage.

For every passage, Read each image file listed (material first, then the five question images, in order; the original
question numbers were removed). Do not solve the questions fully. For each question, work out briefly what it needs:
which data must be located (and how hard that is: dense text, several tables, chart reading), what calculation
(simple lookup / direct ratio / base-period / interval growth / average growth / share change / mixed growth /
multi-step), how close the options are (rough estimation enough, or precise calculation needed), traps, and for
"能够/不能从上述资料中推出" style questions how many statements need real work. Then estimate the 粉笔 全站正确率 —
the percentage of 粉笔 users who answer it correctly in practice (typical range 20–95%; for reference, across real
exam passages the 5-question average is usually 50–80%, a very hard passage is ~40%, an easy one ~80%) — and the
time (seconds) a strong candidate needs.

First calibrate on the ANCHOR passages, whose real 全站正确率 is given: view them the same way and note what made the
hard one hard and the easy one easy. Then rate the TARGET passages. Rate each target independently; do not try to
spread your numbers evenly.

Write your result as a JSON list to {out} — one object per TARGET passage:
{{"mat": "<passage id>", "q": [{{"type": "<short type>", "work": "<what it needs, ≤25 words>", "acc": <int>, "sec": <int>}}, ...5],
  "mat_acc": <mean of the five acc>, "hard_points": "<what makes this passage hard or easy, ≤40 words>"}}
Use the Write tool to create the file. Reply with just "done <n>" when the file is written.
"""
def make(name, targets, anchors, acc):
    s = HEAD.format(out=f'{S}/zl/rate/{name}.json') + '\n## ANCHOR passages\n'
    for a in anchors:
        rs = sorted([r for r in raw if r['mat'] == a], key=lambda r: r['pos'])
        s += block(a, f'ANCHOR {a}', [r['acc'] for r in rs])
    s += '\n## TARGET passages\n'
    for t in targets:
        s += block(t, f'TARGET {t}')
    open(f'{S}/zl/rate/{name}.prompt.txt', 'w').write(s)
    return s
if __name__ == '__main__':
    pl = json.load(open(S + '/zl/pilot.json'))
    t = pl['pilot']
    for k in range(4):
        make(f'pilot{k}', t[k::4], pl['anchors'], pl['acc'])
    print(open(f'{S}/zl/rate/pilot0.prompt.txt').read()[:3000])
