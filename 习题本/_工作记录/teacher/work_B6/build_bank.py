# -*- coding: utf-8 -*-
"""Assemble teacher/bank_B6.json (T228–T267) and teacher/work_B6/extras_B6.json, then run the checks."""
import json, os, re, subprocess, sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
SP = "/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad"
sys.path.insert(0, HERE)
from entries_main import E
from entries_extra import X

KEYS = ["tid", "keep", "db_match", "module", "kaofa", "method", "source", "stem", "options", "options_added",
        "answer", "jiexi", "learn", "level", "figure", "verify", "issues"]

def finalize(e, extra=False):
    e = dict(e)
    e.setdefault("verify", None)
    f = e.get("figure")
    if f and f.get("type") == "svg":
        svg = open(os.path.join(HERE, "fig", f["svg_file"] + ".svg"), encoding="utf-8").read()
        ET.fromstring(svg)  # well-formed check
        e["figure"] = {"type": "svg", "svg": svg, "desc": f["desc"]}
    keys = KEYS[:1] + (["host_tid"] if extra else []) + KEYS[1:]
    out = {k: e.get(k) for k in keys}
    extra_keys = set(e) - set(keys)
    assert not extra_keys, (e["tid"], extra_keys)
    return out

main = [finalize(e) for e in E]
extras = [finalize(x, extra=True) for x in X]

with open(os.path.join(SP, "teacher", "bank_B6.json"), "w", encoding="utf-8") as fh:
    json.dump(main, fh, ensure_ascii=False, indent=1)
with open(os.path.join(HERE, "extras_B6.json"), "w", encoding="utf-8") as fh:
    json.dump(extras, fh, ensure_ascii=False, indent=1)

# ------------------------------------------------------------------ checks
problems = []
def visible_len(s):
    s = re.sub(r"\\(frac|sqrt|text|angle|triangle|parallel|pi|times|div|le|ge|sim|to|rho|cdot)\b", "", s)
    s = s.replace("$", "").replace("{", "").replace("}", "").replace("\\", "").replace("_", "").replace("^", "")
    return len(s)

def check(lst, expected_tids, label):
    data = json.load(open(lst, encoding="utf-8"))
    tids = [d["tid"] for d in data]
    if expected_tids is not None and tids != expected_tids:
        problems.append(f"{label}: tid list mismatch")
    if len(set(tids)) != len(tids):
        problems.append(f"{label}: duplicate tids")
    for d in data:
        t = d["tid"]
        if not d["keep"]:
            if not d["issues"]:
                problems.append(f"{t}: keep=false without reason")
            continue
        if sorted((d["options"] or {}).keys()) != ["A", "B", "C", "D"] or not all(str(v).strip() for v in d["options"].values()):
            problems.append(f"{t}: options incomplete")
        if d["answer"] not in ("A", "B", "C", "D"):
            problems.append(f"{t}: bad answer {d['answer']}")
        for k in ("stem", "jiexi", "learn", "level", "module", "kaofa", "method"):
            if not d.get(k):
                problems.append(f"{t}: empty {k}")
        if len(d["kaofa"]) > 20 or len(d["method"]) > 20:
            problems.append(f"{t}: kaofa/method too long ({len(d['kaofa'])}/{len(d['method'])})")
        if visible_len(d["jiexi"]) > 300:
            problems.append(f"{t}: jiexi too long ({visible_len(d['jiexi'])})")
        if d["level"] not in ("基础", "中等", "难", "很难"):
            problems.append(f"{t}: bad level")
        if "参考用时" in d["jiexi"]:
            problems.append(f"{t}: jiexi mentions 参考用时")
        for k in ("stem", "jiexi"):
            if d[k].count("$") % 2:
                problems.append(f"{t}: unbalanced $ in {k}")
        for k, v in d["options"].items():
            if v.count("$") % 2:
                problems.append(f"{t}: unbalanced $ in option {k}")
        if re.search(r"樱有尽有|公众号|淘宝", d["stem"] + json.dumps(d["options"], ensure_ascii=False)):
            problems.append(f"{t}: watermark text")
        vp = d["verify"]
        if not vp or not os.path.exists(vp):
            problems.append(f"{t}: verify script missing")
            continue
        r = subprocess.run([sys.executable, vp], capture_output=True, text=True, timeout=600)
        got = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
        if r.returncode != 0 or got != d["answer"]:
            problems.append(f"{t}: verify output {got!r} (rc={r.returncode}) != answer {d['answer']}; {r.stderr[-200:]}")
    return data

expected = [f"T{i}" for i in range(228, 268)]
m = check(os.path.join(SP, "teacher", "bank_B6.json"), expected, "main")
x = check(os.path.join(HERE, "extras_B6.json"), None, "extras")

from collections import Counter
print("main: total", len(m), "keep", sum(d["keep"] for d in m), "skip", sum(not d["keep"] for d in m))
print("main modules:", Counter(d["module"] for d in m if d["keep"]))
print("main levels:", Counter(d["level"] for d in m if d["keep"]))
print("main answers:", Counter(d["answer"] for d in m if d["keep"]))
print("main figures:", sum(1 for d in m if d["figure"]), "db_match:", sum(1 for d in m if d["db_match"]))
print("extras: total", len(x), "keep", sum(d["keep"] for d in x))
print("PROBLEMS:" if problems else "ALL CHECKS PASSED", *problems, sep="\n  ")
