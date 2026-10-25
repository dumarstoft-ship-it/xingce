# 任务：按审题人的需求，出几道"能卡住人"的数学改编题

先读：
- /tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/briefs/common.md（背景）
- /tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/briefs/generate.md（出题、验算、输出格式，全部照办）

背景：考生觉得第一周数学简单题太多。考生的原话："数学这个东西就是降维打击的，难题除了知识难以外，还有一些手法的使用也是比较复杂的。当然不是要每道题都出到这么难，就是平时训练的题至少得有意义，得卡住我，让我学到一点什么。"
审题人已经逐题去掉了没有训练价值的题，补进了老师的题和更有分量的真题。剩下几个空位题库里没有合适的题，所以要你按需求新出。

需求在当天的决策文件里：/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/harden/D0{N}_decision.json 的 new_variants，每条写了组、考法、出题方向和"为什么更有训练价值"。当天最终会用到的题见 remove、add_real、add_teacher，以及数据包 harden/D0{N}_packet.json。新题不能和这些题撞模型、撞数据、撞情境。

老师笔记全文在 /tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/teacher/notes.txt，本模块相关的几节请先读，体会他的手法。

要求：
- 每道题都要有一个真正的"卡点"，也就是必须想到某个手法或转化，才能又快又准地做出来。解析里要点明这个卡点，以及想不到时最常见的错法。
- 难，但不能偏、怪、繁：要有真题的样子，计算量适中。
- 照 generate.md 的规定：
  - 每题一个验算脚本，从题面数据求解，确认恰好一个选项成立；
  - 干扰项来自真实的错误路径；
  - 题干里不出现任何提示考法的字眼；
  - 设问统一以"（ ）+单位"结尾；
  - 解析在 250 字以内，不写参考用时。
- vid 用 "D0{N}-math-h-v01" 起连续编号；group 填需求里的组标题（原样）；difficulty 按实际难度填 2 或 3。

输出：
- /tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/gen/D0{N}_math_h.json
- 验算脚本 verify/D0{N}-math-h-vNN.py

完成后运行 python3 /tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/scripts/check_gen.py "D0{N}_math_h.json"，修到没有 PROBLEM 为止。回复里简要汇报：每道题的卡点是什么。只写上面这些文件和你的草稿目录 work_D0{N}h/，不要运行 git，不要用前台 sleep。
