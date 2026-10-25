# -*- coding: utf-8 -*-
"""综合推理验算小工具：所有题目从题面条件出发穷举，再逐项判断选项。"""
from itertools import permutations, product, combinations

def line(names, n, conds, positions=None):
    """直线排位：names 放到 1..n（每位至多一人），返回满足全部条件的 dict 列表。"""
    pos = positions or list(range(1, n + 1))
    out = []
    for p in permutations(pos, len(names)):
        s = dict(zip(names, p))
        if all(c(s) for c in conds):
            out.append(s)
    return out

def judge(tag, sols, options, mode, expect=None, show=True):
    """mode: must 一定为真 / possible 可能为真 / impossible 不可能为真 / mustfalse 一定为假 / notmust 不能推出。
    options: dict 字母 -> 函数(sol)->bool。要求恰好一个选项成立。"""
    res = {}
    for k, f in options.items():
        vals = [bool(f(s)) for s in sols]
        if mode == 'must':
            res[k] = bool(vals) and all(vals)
        elif mode == 'possible':
            res[k] = any(vals)
        elif mode in ('impossible', 'mustfalse'):
            res[k] = not any(vals)
        elif mode == 'notmust':
            res[k] = not all(vals)
        else:
            raise ValueError(mode)
    good = sorted(k for k, v in res.items() if v)
    ok = (len(good) == 1) and (expect is None or good == [expect])
    if show:
        print(f"[{'OK' if ok else '!!'}] {tag}: 解数={len(sols)} 选项={res} -> {good}" + (f" (预期 {expect})" if expect else ''))
    assert ok, (tag, good, expect)
    return good

def add_cond_unique(tag, sols, options, key, expect=None):
    """补充条件型：选项作为附加条件，问哪项能使 key(sol) 唯一确定。"""
    res = {}
    for k, f in options.items():
        sub = [s for s in sols if f(s)]
        vals = {key(s) for s in sub}
        res[k] = (len(sub) > 0 and len(vals) == 1, len(sub))
    good = sorted(k for k, v in res.items() if v[0])
    ok = (len(good) == 1) and (expect is None or good == [expect])
    print(f"[{'OK' if ok else '!!'}] {tag}: 基础解数={len(sols)} 选项(唯一?,解数)={res} -> {good}" + (f" (预期 {expect})" if expect else ''))
    assert ok, (tag, good)
    return good

def count_options(tag, value, options, expect=None):
    """数值型设问：value 为真实数值，options 字母->数值。"""
    good = sorted(k for k, v in options.items() if v == value)
    ok = len(good) == 1 and (expect is None or good == [expect])
    print(f"[{'OK' if ok else '!!'}] {tag}: 真值={value} 选项={options} -> {good}" + (f" (预期 {expect})" if expect else ''))
    assert ok, (tag, value, good)
    return good

def fmt_line(s, n=None):
    n = n or max(s.values())
    at = {v: k for k, v in s.items()}
    return ' '.join(at.get(i, '_') for i in range(1, n + 1))
