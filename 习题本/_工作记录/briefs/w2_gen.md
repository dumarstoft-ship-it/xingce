# 任务：按排题人的需求，出几道"能卡住人"的数学改编题（第二周）

先读：
- /tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/briefs/common.md（背景；其中"每天 45 题"的旧题量已改为每天 30 题，以本文为准）
- /tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/briefs/generate.md（出题、验算、输出格式，全部照办）

背景：考生要的是"方法收敛 + 手感"——每天 30 道一个模块，做完精细复盘。考生的原话："数学这个东西就是降维打击的，难题除了知识难以外，还有一些手法的使用也是比较复杂的。当然不是要每道题都出到这么难，就是平时训练的题至少得有意义，得卡住我，让我学到一点什么。"
排题人已经从真题和老师笔记里选好了当天的大部分题；剩下几个位置题库里没有合适的题，所以要你按需求新出。

需求在当天的决策文件里：/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/w2/D{DD}_decision.json 的 new_variants（每条有 n、group、kaofa、idea、difficulty_hint）。当天其余的题见 groups 里的 real / teacher 条目（真题截图在 crops/real2/<id>_q.png，老师题在数据包 w2/D{DD}_packet.json 的 teacher 里）。新题不能和当天这些题撞模型、撞数据、撞情境。
老师笔记全文在 /tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/teacher/notes.txt，本模块相关的几节请先读，体会他的手法。

要求：
- 每道题都要有一个真正的"卡点"：必须想到某个手法或转化，才能又快又准地做出来。解析里要点明这个卡点，以及想不到时最常见的错法。
- 难，但不能偏、怪、繁：要有真题的样子，计算量适中。
- 照 generate.md：每题一个验算脚本，从题面数据求解，确认恰好一个选项成立；干扰项来自真实的错误路径；题干里不出现任何提示考法的字眼；设问统一以"（ ）+单位"结尾；解析在 250 字以内，不写参考用时。
- vid 用 "D{DD}-math-w2-v01" 起连续编号，顺序与 new_variants 的 n 一致（n=1 → v01）；group 填需求里的组标题（原样）；difficulty 按实际难度填 2 或 3；time_s 填一个熟练考生的合理用时。

输出：
- /tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/gen/D{DD}_math_w2.json
- 验算脚本 /tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/verify/D{DD}-math-w2-vNN.py

完成后运行 python3 /tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/scripts/check_gen.py "D{DD}_math_w2.json"，修到没有 PROBLEM 为止。回复里简要汇报每道题的卡点。只写上面这些文件和草稿目录 work_D{DD}w2/，不要运行 git，不要用前台 sleep。
