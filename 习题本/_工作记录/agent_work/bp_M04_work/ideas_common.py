# -*- coding: utf-8 -*-
"""改编 idea 的统一结构：题干骨架 + 四个选项(含干扰项来源) + 由 compute() 从题面数据独立算出答案。
idea 文本由同一份数据拼出，保证文字与验算一致。"""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_M04_work')
from m04lib import *

LETTERS = 'ABCD'
REGISTRY = []

class V:
    def __init__(self, vid, day, kf, direction, seed, change, stem, options, compute, ans,
                 explain, diff, secs, tags=''):
        self.vid = vid; self.day = day; self.kf = kf; self.direction = direction; self.seed = seed
        self.change = change          # 与种子相比"变"在哪里（一句话）
        self.stem = stem              # 题干骨架（只写情境与条件，不提示考法）
        self.options = options        # [(显示文字, 值, 干扰项来源或 None)]
        self.compute = compute        # 从题面数据独立求解，返回值
        self.ans = ans                # 预期正确选项字母
        self.explain = explain        # 解析要点（最快解法）
        self.diff = diff; self.secs = secs; self.tags = tags
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
        # 选项值互不相同
        vals = [str(v) if isinstance(v, str) else round(float(v), 9) for _, v, _ in self.options]
        assert len(set(vals)) == 4, (self.vid, '选项重复', vals)
        return val

    def idea_text(self, full=True):
        opts = '；'.join('%s. %s' % (LETTERS[i], lab) for i, (lab, v, note) in enumerate(self.options))
        right = self.options[LETTERS.index(self.ans)][0]
        traps = '；'.join('%s（%s）' % (lab, note) for (lab, v, note) in self.options if note)
        s = '【变】%s 【题干】%s 【选项】%s。【答案】%s（%s）。【解析要点】%s' % (
            self.change, self.stem, opts, self.ans, right, self.explain)
        if traps:
            s += ' 【干扰项】%s。' % traps
        s += ' 难度 %d，参考用时 %d 秒。' % (self.diff, self.secs)
        return s
