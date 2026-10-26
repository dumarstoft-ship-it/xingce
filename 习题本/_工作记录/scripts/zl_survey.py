"""Survey 资料分析 sections across all registered papers: question numbers, material groups, answers."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from split_q import split, load
import answers as A
from papers import PAPERS
from papers_new import PAPERS_NEW
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
for code, disp, qf, jf in PAPERS + PAPERS_NEW:
    if qf.startswith('OCR:') or not os.path.exists(S + '/lines/' + qf + '.json'):
        print(code.ljust(9), 'no lines'); continue
    try:
        res, heads, lines = split(qf, sections_wanted=('资料分析',))
    except Exception as e:
        print(code.ljust(9), 'ERR', e); continue
    nums = [q['num'] for q in res]
    groups = sum(1 for q in res if q.get('stem_lines'))
    ans = {}
    if jf and os.path.exists(S + '/lines/' + jf + '.json'):
        A.LINES = {}; A.STARTS = []
        ans, seg = A.parse_answers(jf)
    na = sum(1 for n in nums if n not in ans)
    print(code.ljust(9), f'{nums[0] if nums else "-"}-{nums[-1] if nums else "-"} n={len(nums)} stems={groups} noans={na}', [h for _, h in heads])
