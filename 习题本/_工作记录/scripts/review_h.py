"""Blind-review files for the new "卡点" variants (gen/D0x_math_h*.json) of the given days."""
import json, glob, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'

def make(name, days, vids=None):
    vs = []
    for d in days:
        for f in sorted(glob.glob(f'{S}/gen/D{d:02d}_math_h*.json')):
            vs += json.load(open(f))
    if vids: vs = [v for v in vs if v['vid'] in vids]
    q = [{k: v[k] for k in ('vid', 'group', 'shared_stem', 'stem', 'options', 'figure_svg') if k in v} for v in vs]
    qf, kf, of = f'{S}/review/{name}_questions.json', f'{S}/review/{name}_key.json', f'{S}/review/{name}_review.json'
    json.dump(q, open(qf, 'w'), ensure_ascii=False, indent=1); json.dump(vs, open(kf, 'w'), ensure_ascii=False, indent=1)
    prompt = f"""你是行测资深审题人。请盲审广东省考习题本第一周"去水"后新出的数学改编题（第 {', '.join(map(str, days))} 天，共 {len(vs)} 道）。

必读：{S}/briefs/common.md 和 {S}/briefs/review.md（流程与输出格式）。
背景：考生嫌第一周简单题太多，要求"平时训练的题至少得有意义，得卡住我，让我学到一点什么"。所以这批新题每道都应该有一个真正的卡点：必须想到某个手法或转化，才能又快又准地做出来。同时，难不等于偏、怪、繁。
题目文件（无答案）：{qf}
答案文件（做完全部题后才能打开）：{kf}
输出：{of}

除了 review.md 要求的对错检查，每题再判断两件事：
- 卡点是否真实存在：会不会其实一步就出答案？
- 有没有歧义或偏怪。
没有卡点的题记为 fix，并给出加深的建议；有硬伤的记为 drop。
回复里汇报：题数，与答案一致的题数，fix 和 drop 各几道，以及主要问题类型。"""
    if vids:  # second round: items revised after the first blind review
        prompt += """

这一批是第一轮盲审后修改过的题（加深卡点、换情境、改数据，或只为摊匀答案字母而调整了选项）。请照样先盲做、再开答案，另外特别检查：解析里的数字、选项字母、“误选X”与新题面和新选项是否一致；只调整了选项的题，干扰项是否仍对应真实错法。"""
    pf = f'{S}/prompts/rev_{name}.txt'
    open(pf, 'w').write(prompt)
    return pf, len(vs)

if __name__ == '__main__':
    name = sys.argv[1]; days = [int(x) for x in sys.argv[2].split(',')]
    vids = sys.argv[3].split(',') if len(sys.argv) > 3 else None
    print(make(name, days, vids))
