# -*- coding: utf-8 -*-
"""按改编编号替换某条 idea 的选项行与答案字母（选项行写成 Python 源码原样）。"""
import re, sys

def set_options(path, vid, opts_src, letter):
    lines = open(path, encoding='utf-8').read().split('\n')
    # 找到 V('vid', 所在行
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith("V('%s'," % vid):
            start = i
            break
    assert start is not None, vid
    # 之后第一个以 "  [(" 开头的行是选项行，紧随其后的是 "  c, 'X',"
    j = start
    while not lines[j].startswith('  [('):
        j += 1
    assert lines[j + 1].startswith("  c, '"), (vid, lines[j + 1])
    lines[j] = '  ' + opts_src + ','
    lines[j + 1] = "  c, '%s'," % letter
    open(path, 'w', encoding='utf-8').write('\n'.join(lines))

if __name__ == '__main__':
    path = sys.argv[1]
    spec = __import__(sys.argv[2])
    for vid, opts_src, letter in spec.CHANGES:
        set_options(path, vid, opts_src, letter)
        print('updated', vid, letter)
