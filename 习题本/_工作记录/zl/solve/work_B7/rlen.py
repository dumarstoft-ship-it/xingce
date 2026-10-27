import json, re
p = "/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/zl/solve/out_B7.json"
d = json.load(open(p))
def render(s):
    def rm(m):
        t = m.group(1)
        t = t.replace(r"\approx","≈").replace(r"\times","×").replace(r"\%","%")
        t = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"\1/\2", t)
        t = t.replace("{","").replace("}","")
        t = re.sub(r"\\[a-z]+","",t)
        return t
    return re.sub(r"\$(.+?)\$", rm, s)
for m in d:
    for q in m["q"]:
        r = render(q["jiexi"])
        syn = "综合分析" in q["jiexi"][:12]
        lim = 350 if syn else 250
        flag = "OVER" if len(r)>lim else ""
        print(m["mat"], q["n"], "raw", len(q["jiexi"]), "rendered", len(r), "lim", lim, flag)
