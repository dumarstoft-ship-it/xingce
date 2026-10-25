import json, subprocess, ast, re, sys
key = json.load(open(sys.argv[1], encoding="utf-8"))
bad = 0
for q in key:
    path = q["verify"]
    src = open(path, encoding="utf-8").read()
    m = re.search(r"^OPTIONS\s*=\s*(\{.*?\})", src, re.M | re.S)
    opts = ast.literal_eval(m.group(1))
    same_opts = {k: str(v) for k, v in opts.items()} == {k: str(v).strip() for k, v in q["options"].items()}
    out = subprocess.run([sys.executable, "-I", path], capture_output=True, text=True, timeout=600)
    last = out.stdout.strip().splitlines()[-1] if out.stdout.strip() else "(no output)"
    ok = out.returncode == 0 and last == q["answer"] and same_opts
    bad += not ok
    print(f"{q['vid']}: rc={out.returncode} printed={last} key={q['answer']} options_match={same_opts} {'OK' if ok else 'CHECK'}"
          + (f" stderr={out.stderr.strip()[-200:]}" if out.returncode else ""))
print("scripts:", len(key), "problems:", bad)
