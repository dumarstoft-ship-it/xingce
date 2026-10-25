# -*- coding: utf-8 -*-
"""改编 idea 的统一结构（本轮重写）：
题干（可直接改写成正式题，只写情境与条件，不提示考法）+ 四个选项（含干扰项来源）+ compute() 从题面数据独立求解。
idea 文本由同一份数据拼出，保证 JSON、MD 与验算一致。"""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_M04_work/v2')
from m04lib import *
import math

LETTERS = 'ABCD'
REGISTRY = []

# 题干禁用词：任何点明考法/方法的字眼（考生要求题目页不提示题型）
BANNED = ['行程问题', '相遇问题', '追及问题', '流水行船', '牛吃草', '比例法', '赋值', '特值', '方程法', '代入',
          '等距离平均', '调和平均', '平均速度公式', '相对速度', '参照', '公式', '模型', '提示', '技巧', '秒杀',
          '十字交叉', '展开', '等效', '穿越', '勾股', '会合周期', '整体法', '设而不求', '画图', '图像法']

class V:
    def __init__(self, vid, kf, direction, seed, change, stem, options, compute, ans,
                 solution, trap, diff, secs, backup=False):
        self.vid = vid                  # 如 '3-1-1'
        self.day = int(vid.split('-')[0]) if not backup else 0
        self.kf = kf                    # 考法序号 1..15
        self.direction = direction      # 巩固/深化/拓展
        self.seed = seed                # 真题 id 或 '考法X'
        self.change = change            # 改编点（与种子相比"变"在哪里）
        self.stem = stem                # 题干
        self.options = options          # [(显示文字, 值, 干扰项来源或 None)]，按显示顺序
        self.compute = compute
        self.ans = ans
        self.solution = solution        # 最快解法
        self.trap = trap                # 易错点
        self.diff = diff
        self.secs = secs
        self.backup = backup
        REGISTRY.append(self)

    def verify(self):
        val = self.compute()
        hits = []
        for i, (lab, v, note) in enumerate(self.options):
            if isinstance(v, str) or isinstance(val, str):
                ok = (v == val)
            else:
                ok = abs(float(v) - float(val)) < 1e-9
            if ok:
                hits.append(LETTERS[i])
        assert len(hits) == 1, (self.vid, '计算值', val, '命中', hits)
        assert hits[0] == self.ans, (self.vid, '预期', self.ans, '实际', hits[0], val)
        vals = [str(v) if isinstance(v, str) else round(float(v), 9) for _, v, _ in self.options]
        assert len(set(vals)) == 4, (self.vid, '选项重复', vals)
        for w in BANNED:
            assert w not in self.stem, (self.vid, '题干含提示词', w)
        assert self.direction in ('巩固', '深化', '拓展')
        return val

    def tag(self):
        return ('〔备%s〕' % self.vid.split('-')[-1]) if self.backup else ('〔%s〕' % self.vid)

    def right_label(self):
        return self.options[LETTERS.index(self.ans)][0]

    def opts_text(self):
        s = ' / '.join(lab for lab, v, note in self.options)
        notes = '；'.join('%s是%s' % (lab, note) for lab, v, note in self.options if note)
        return s + ('（%s）' % notes if notes else '')

    def idea_text(self):
        return ('%s【%s】题干：%s｜答案：%s（%s）｜选项：%s｜解法：%s｜易错：%s｜难度：%d｜参考用时：%d秒' % (
            self.tag(), self.change, self.stem, self.right_label(), self.ans, self.opts_text(),
            self.solution, self.trap, self.diff, self.secs))
