# L01 翻译推理 —— 5 道无官方答案真题的独立求解（真值表穷举）
# 做法：把题干翻译成命题公式，穷举所有赋值，逐项判断选项在"所有满足题干的模型"中是否成立，
# 程序只根据题面数据计算，最后检查恰好一个选项成立并打印字母。
import itertools

def imp(a, b):
    return (not a) or b

def models(names, premises):
    for vals in itertools.product([False, True], repeat=len(names)):
        m = dict(zip(names, vals))
        if all(p(m) for p in premises):
            yield m

def entails(names, premises, concl):
    ms = list(models(names, premises))
    assert ms, "题干条件不相容"
    return all(concl(m) for m in ms)

def consistent(names, premises):
    return any(True for _ in models(names, premises))

def unique(d):
    hits = [k for k, v in d.items() if v]
    assert len(hits) == 1, d
    return hits[0]

res = {}

# ---------- 2026GD-51 ----------
# J=采用集约高效, R=资源消耗量减少, S=减少速度非常缓慢, F=减少速度很快, N=对经济发展造成负面影响
# (1) J -> R ; (2) S -> not N ; "很快"与"非常缓慢"不能同真
names = ["J", "R", "S", "F", "N"]
prem = [lambda m: imp(m["J"], m["R"]),
        lambda m: imp(m["S"], not m["N"]),
        lambda m: not (m["S"] and m["F"])]
opts = {
    "A": lambda m: imp(not m["R"], not m["J"]),
    "B": lambda m: imp(not m["J"], not m["R"]),
    "C": lambda m: imp(m["R"], m["J"]),
    "D": lambda m: imp(m["R"] and m["F"], m["N"]),
}
res["2026GD-51"] = unique({k: entails(names, prem, f) for k, f in opts.items()})

# ---------- 2026GD-54 ----------
# K科技 W文化 B博物 M美术；四馆不都去；不既文化又博物；美术或文化；不去美术
names = ["K", "W", "B", "M"]
prem = [lambda m: not (m["K"] and m["W"] and m["B"] and m["M"]),
        lambda m: not (m["W"] and m["B"]),
        lambda m: m["M"] or m["W"],
        lambda m: not m["M"]]
opts = {
    "A": lambda m: imp(not m["K"], m["B"]),      # 如果不去科技馆，就去博物馆
    "B": lambda m: imp(m["B"], not m["K"]),      # 只有不去科技馆，才去博物馆：去博物馆 -> 不去科技馆
    "C": lambda m: imp(not m["K"], not m["B"]),  # 只有不去博物馆，才不去科技馆：不去科技馆 -> 不去博物馆
    "D": lambda m: imp(m["B"], not m["K"]),      # 如果要去博物馆，不去科技馆
}
target = lambda m: m["K"]
res["2026GD-54"] = unique({k: consistent(names, prem + [f]) and entails(names, prem + [f], target)
                           for k, f in opts.items()})

# ---------- 2026ZJA-96 ----------
# 要求：升级提星 U -> 设施完备 F 且 通过考核 H。"说明没有遵守要求" = 情形本身就使要求为假
names = ["U", "F", "H"]
req = lambda m: imp(m["U"], m["F"] and m["H"])
cases = {
    1: lambda m: m["U"] and not m["H"],
    2: lambda m: m["U"] and not m["F"],
    3: lambda m: m["F"] and m["H"] and not m["U"],
}
violates = {i: entails(names, [c], lambda m: not req(m)) for i, c in cases.items()}
combo = {"A": {1, 2}, "B": {2, 3}, "C": {3}, "D": {1, 2, 3}}
vset = {i for i, v in violates.items() if v}
res["2026ZJA-96"] = unique({k: s == vset for k, s in combo.items()})

# ---------- 2026GK-111 ----------
# T提高卫生事业发展水平 C部门密切合作 S促进三医协同 D深化医改体制机制 Q强化规划刚性约束
# E更好满足新期待 G提高获得感幸福感安全感
# (1) S -> T且C ; (2) S -> D ; (3) D -> Q ; (4) "只有D，才能E，进而G"：E -> D，G -> D
names = ["T", "C", "S", "D", "Q", "E", "G"]
prem = [lambda m: imp(m["S"], m["T"] and m["C"]),
        lambda m: imp(m["S"], m["D"]),
        lambda m: imp(m["D"], m["Q"]),
        lambda m: imp(m["E"], m["D"]),
        lambda m: imp(m["G"], m["D"])]
opts = {
    "A": lambda m: imp(m["T"], m["C"]),
    "B": lambda m: imp(m["G"], m["Q"]),           # 只有Q，才能G
    "C": lambda m: imp(m["D"], m["S"]),           # 要D，就必须S
    "D": lambda m: imp(not m["E"], not m["S"]),
}
res["2026GK-111"] = unique({k: entails(names, prem, f) for k, f in opts.items()})
# 稳健性：若把"进而"读成 E -> G（满足期待带来获得感），则没有任何选项成立，说明命题人取的是 G -> D 的读法
prem_alt = prem[:4] + [lambda m: imp(m["E"], m["G"])]
assert not any(entails(names, prem_alt, f) for f in opts.values())

# ---------- 2026ZJA-99 ----------
# 把每句诗里两命题(X, Y)的关系写成"被排除的真值组合"，与题干比较
# 题干：但使龙城飞将在(X)，不教胡马度阴山(Y)：X -> 非Y
def excluded(rel):
    return {(x, y) for x in (True, False) for y in (True, False) if not rel(x, y)}
stem = excluded(lambda x, y: imp(x, not y))
poems = {
    "A": excluded(lambda x, y: imp(not x, not y)),   # 不破楼兰(X)终不还(Y)：非X -> 非Y
    "B": excluded(lambda x, y: imp(y, x)),           # 清如许(X)，为有源头活水来(Y)：Y 是 X 的原因，Y -> X
    "C": excluded(lambda x, y: imp(y, not x)),       # 不畏浮云遮望眼(X)，自缘身在最高层(Y)：Y -> 非X
    "D": excluded(lambda x, y: imp(not x, y)),       # 若非群玉山头见(X)，会向瑶台月下逢(Y)：非X -> Y
}
res["2026ZJA-99"] = unique({k: v == stem for k, v in poems.items()})

for k, v in res.items():
    print(k, v)
