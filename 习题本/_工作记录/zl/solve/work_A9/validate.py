import json, re
P = "/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_A9.json"
task = json.load(open("/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/A9.json"))
d = json.load(open(P))
ok = True
assert [m["mat"] for m in d] == [m["mat"] for m in task], "mat order mismatch"
cjk = re.compile(r"[一-鿿，。、；：（）“”]")
for m in d:
    if len(m["q"]) != 5: print("bad count", m["mat"]); ok = False
    for i, q in enumerate(m["q"], 1):
        j = q["jiexi"]
        if q["n"] != i: print("bad n", m["mat"], i); ok = False
        if q["answer"] not in "ABCD" or len(q["answer"]) != 1: print("bad ans", m["mat"], i); ok = False
        if not j.endswith("故正确答案为%s。" % q["answer"]): print("bad ending", m["mat"], i); ok = False
        if j.count("$") % 2: print("odd $", m["mat"], i); ok = False
        maths = re.findall(r"\$(.+?)\$", j)
        for s in maths:
            if re.search(r"(?<!\\)%", s): print("unescaped % in math", m["mat"], i, s); ok = False
            if cjk.search(s): print("CJK in math", m["mat"], i, s); ok = False
            if "≈" in s or "×" in s: print("unicode op in math", m["mat"], i, s); ok = False
        # visible length: replace math blocks by rough rendered length
        vis = re.sub(r"\$(.+?)\$", lambda mo: re.sub(r"\\(frac|times|approx|text)|[{}\\]", "", mo.group(1)), j)
        for bad in ["根据我的计算", "程序", "Python", "计算机"]:
            if bad in j: print("forbidden phrase", m["mat"], i, bad); ok = False
        print(m["mat"], i, q["answer"], q["confidence"], "raw", len(j), "vis", len(vis))
print("ALL OK" if ok else "PROBLEMS")
