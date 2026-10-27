import json, re
OUT = "/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_A6.json"
INP = "/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/A6.json"
data = json.load(open(OUT, encoding="utf-8"))
inp = json.load(open(INP, encoding="utf-8"))
ok = True
assert [d["mat"] for d in data] == [d["mat"] for d in inp], "mat order/ids mismatch"
zh = re.compile(r"[一-鿿]")
def visible_len(s):
    t = re.sub(r"\\(frac|times|approx|div|text|Leftrightarrow)", "", s)
    t = t.replace("$", "").replace("{", "").replace("}", "").replace("\\%", "%").replace("\\", "")
    return len(t)
for d in data:
    qs = d["q"]
    if len(qs) != 5 or [q["n"] for q in qs] != [1,2,3,4,5]:
        print("BAD count", d["mat"]); ok = False
    for q in qs:
        a = q["answer"]; j = q["jiexi"]
        if a not in "ABCD" or len(a) != 1: print("BAD answer", d["mat"], q["n"]); ok = False
        if not j.endswith("故正确答案为%s。" % a): print("BAD ending", d["mat"], q["n"]); ok = False
        if j.count("故正确答案为") != 1: print("multiple endings", d["mat"], q["n"]); ok = False
        if q["confidence"] not in ("high","medium","low"): print("BAD conf", d["mat"], q["n"]); ok = False
        if q["confidence"] == "low" and not q["problem"]: print("low without problem", d["mat"], q["n"]); ok = False
        for bad in ["根据我的计算", "程序算得", "程序", "我的计算", "Python"]:
            if bad in j: print("forbidden phrase", bad, d["mat"], q["n"]); ok = False
        if j.count("$") % 2: print("odd $", d["mat"], q["n"]); ok = False
        segs = re.findall(r"\$(.+?)\$", j)
        for s in segs:
            if zh.search(s): print("Chinese in math", d["mat"], q["n"], s); ok = False
            if re.search(r"(?<!\\)%", s): print("unescaped % in math", d["mat"], q["n"], s); ok = False
            if s.count("{") != s.count("}"): print("brace mismatch", d["mat"], q["n"], s); ok = False
        vl = visible_len(j)
        is_zh = j.startswith("本题考查综合分析")
        lim = 350 if is_zh else 250
        flag = "" if 80 <= vl <= lim else "  <-- length out of range"
        print("%s Q%d ans=%s conf=%s raw=%d visible=%d%s" % (d["mat"], q["n"], a, q["confidence"], len(j), vl, flag))
print("ALL OK" if ok else "PROBLEMS FOUND")
print("done", len(data))
