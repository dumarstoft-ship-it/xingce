import json, re
p = "/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_B3.json"
inp = "/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/B3.json"
d = json.load(open(p, encoding="utf-8"))
src = json.load(open(inp, encoding="utf-8"))
assert [m["mat"] for m in d] == [m["mat"] for m in src], "mat order mismatch"
ok = True
def visible_len(s):
    t = re.sub(r"\\(frac|times|approx|left|right)", "", s)
    t = t.replace("$", "").replace("{", "").replace("}", "").replace("\\", "")
    return len(t)
for m in d:
    if len(m["q"]) != 5: print("BAD count", m["mat"]); ok = False
    for qq in m["q"]:
        a = qq["answer"]
        if a not in "ABCD" or len(a) != 1: print("BAD answer", m["mat"], qq["n"]); ok = False
        if not qq["jiexi"].endswith(f"故正确答案为{a}。"): print("BAD ending", m["mat"], qq["n"]); ok = False
        if qq["jiexi"].count("$") % 2: print("odd $", m["mat"], qq["n"]); ok = False
        for bad in ["根据我的计算", "程序算得", "我的", "程序"]:
            if bad in qq["jiexi"]: print("forbidden phrase", bad, m["mat"], qq["n"]); ok = False
        if qq["confidence"] not in ("high","medium","low"): print("bad conf"); ok = False
        print(m["mat"], qq["n"], qq["answer"], qq["confidence"], "len_raw", len(qq["jiexi"]), "len_vis", visible_len(qq["jiexi"]))
print("ALL OK" if ok else "PROBLEMS")
print("answers:", {m["mat"]: "".join(q["answer"] for q in m["q"]) for m in d})
print("low:", [(m["mat"], q["n"]) for m in d for q in m["q"] if q["confidence"] == "low"])
