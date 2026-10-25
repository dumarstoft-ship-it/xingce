"""D06-math-h-v10  挑战环节：第 1 题答对得 100 元，可带走离开或继续答第 2 题；第 2 题答对奖金累计 400 元，
答错清零。答对第 1、2 题的概率为 0.8、0.3，以奖金期望最大为原则决策，求所得奖金的期望。
独立求解：列出选手所有可行策略（答对第 1 题后"结束"或"继续"），对每种策略穷举答题结果树求期望，
取期望最大的策略；再确认四个选项中恰好一个等于该最大期望，打印该选项字母。
"""
from fractions import Fraction as F
from itertools import product

# ---- 题面数据 ----
P1, P2 = F(8, 10), F(3, 10)
PRIZE1, PRIZE2 = 100, 400     # 答对第 1 题的奖金；第 2 题答对后的累计奖金（答错清零）
OPTIONS = {"A": "96", "B": "100", "C": "120", "D": "152"}

def ev(strategy):
    """strategy: 'stop' 答对第 1 题后带走；'go' 继续答第 2 题。穷举两题对错。"""
    e = F(0)
    for r1, r2 in product([True, False], repeat=2):
        pr = (P1 if r1 else 1 - P1) * (P2 if r2 else 1 - P2)
        if not r1:
            pay = 0
        elif strategy == "stop":
            pay = PRIZE1
        else:
            pay = PRIZE2 if r2 else 0
        e += pr * pay
    return e

evs = {s: ev(s) for s in ("stop", "go")}
best = max(evs, key=evs.get)
print("各策略期望：", {k: float(v) for k, v in evs.items()}, "最优：", best)
E = evs[best]

hits = [k for k, v in OPTIONS.items() if F(v) == E]
assert len(hits) == 1, hits
print(hits[0])
