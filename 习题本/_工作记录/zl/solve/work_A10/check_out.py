import json, re
OUT = "/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_A10.json"
task = json.load(open("/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/A10.json", encoding="utf-8"))
d = json.load(open(OUT, encoding="utf-8"))
assert [m["mat"] for m in d] == [m["mat"] for m in task], "mat order mismatch"
def visible(s):
    t = s
    t = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"\1/\2", t)
    t = t.replace("\\times", "×").replace("\\approx", "≈").replace("\\%", "%").replace("$", "")
    t = re.sub(r"\\[a-zA-Z]+", "", t)
    t = t.replace("{", "").replace("}", "")
    return t
ok = True
for m in d:
    assert len(m["q"]) == 5, m["mat"]
    assert [q["n"] for q in m["q"]] == [1, 2, 3, 4, 5]
    for q in m["q"]:
        a = q["answer"]; j = q["jiexi"]
        if a not in "ABCD" or len(a) != 1: print("bad answer", m["mat"], q["n"]); ok = False
        if not j.endswith("故正确答案为%s。" % a): print("bad ending", m["mat"], q["n"]); ok = False
        if j.count("故正确答案为") != 1: print("multiple endings", m["mat"], q["n"]); ok = False
        if q["confidence"] not in ("high", "medium", "low"): print("bad conf"); ok = False
        if j.count("$") % 2: print("odd $", m["mat"], q["n"]); ok = False
        maths = re.findall(r"\$(.*?)\$", j)
        for mm in maths:
            if mm.count("{") != mm.count("}"): print("brace mismatch", m["mat"], q["n"], mm); ok = False
            if re.search(r"[\u4e00-\u9fff]", mm): print("CJK in math", m["mat"], q["n"], mm); ok = False
            if re.search(r"(?<!\\)%", mm): print("unescaped % in math", m["mat"], q["n"], mm); ok = False
        for bad in ("我的计算", "程序算得", "程序", "Python"):
            if bad in j: print("forbidden", bad, m["mat"], q["n"]); ok = False
        if not j.startswith("本题考查"): print("start", m["mat"], q["n"])
        print(m["mat"], q["n"], a, q["confidence"], "raw", len(j), "visible", len(visible(j)))
print("ALL OK" if ok else "PROBLEMS")
print("answers:", {m["mat"]: "".join(q["answer"] for q in m["q"]) for m in d})
