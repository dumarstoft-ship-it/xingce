# -*- coding: utf-8 -*-
"""Rewrites the ISSUES block of plan.py (state re-checked in this run, crops viewed 2026-10-25 after the re-crop)."""
ISSUES = [
    {'id': '2023SC-85', 'problem': '【保留，排版前须处理】重新裁图后，题目截图 crops/real2/2023SC-85_q.png 和排版实际使用的去题号版 crops/real2_nonum/2023SC-85_q.png 下方都仍混有与本题无关的资料分析“材料”段（2020年软件和信息技术服务业数据），提取文字也带着这段。直接排版会把这段印出来，需再裁一次，只保留到选项D（或在 real_overrides 里重新录入题干和选项）。答案C经程序独立复核无误。'},
    {'id': '2020SZS-80', 'problem': '【保留，建议补写解析】官方答案A经程序独立复核无误，但官方解析的推理不成立：它以“B、D选项都成立”为由排除假设，还有“可推出啊”之类的笔误。建议解析改用：甲说真话→真凶在乙、丙中；若被告知“丙说真话”，真凶只能是乙（能确定），若被告知“丙说假话”，乙、丙都有可能（不能确定）；老赵当时推测出了真凶，说明被告知的是“丙说真话”→乙是真凶，所以忘了也能再推出来。题库标难度2，但全站正确率只有46%，按难题排在第36天。'},
    {'id': '2020SZS-75', 'problem': '【保留在L02，归类提示】设问是“上述发现最能支持的论断是”，粉笔按加强论证解析（taxonomy 里“支持”一般归L03）。本题是“题干→选项”的结论型，本模块把它作为归纳推理的弱推出（考法十三）使用。官方答案C（“全球火烧土地面积会继续减少”）含趋势预测，在“最能支持”的问法下可以接受；解析须讲清C与D（题干没有比较两类火烧面积）的区别。正确率39%，排在第36天。'},
    {'id': '2024JSA-102', 'problem': '【保留】区分度公式 $D=P_H-P_L$ 只在截图中（截图清楚），提取文字里没有。用截图排版不受影响；若重新录入题干，须补上公式。官方答案D经程序复核无误（难度为1时D=0；D可以为负；难度0.27时D最大为1，不是0.5）。'},
    {'id': '2020SZS-71', 'problem': '【保留】原卷把第六人印成“巳”（应为“己”），截图和提取文字都是这样。用截图排版时，建议在解析中注明“巳即己”。答案C经程序复核无误。'},
    {'id': '2022ZJA-105', 'problem': '【保留】“β-谷甾醇”的β在截图里颜色很淡，提取文字里漏掉了。用截图排版影响不大；若重新录入，须补上β。本题与2022HB-108是同一道题，本模块只收录ZJA版本，没有重复。'},
]

if __name__ == '__main__':
    import re
    p = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_L02_work/plan.py'
    src = open(p, encoding='utf-8').read()
    start = src.index('ISSUES = [')
    end = src.index('SELF_SOLVED = []')
    block = 'ISSUES = [\n' + ''.join('    ' + repr(i) + ',\n' for i in ISSUES) + ']\n'
    src = src[:start] + block + src[end:]
    open(p, 'w', encoding='utf-8').write(src)
    print('ISSUES rewritten:', len(ISSUES))
