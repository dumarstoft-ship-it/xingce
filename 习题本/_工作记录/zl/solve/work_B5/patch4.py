p = "build_out.py"
s = open(p, encoding="utf-8").read()
def rep(old_start, new_text):
    global s
    i = s.find('r"' + old_start)
    assert i >= 0, old_start
    j = s.find('", ""', i)
    assert j > i
    s = s[:i] + 'r"' + new_text + s[j:]
rep("本题考查平均数增长率（间隔）", r"本题考查平均数增长率（间隔）。2022年重量增速为1.5% − 4.1% = −2.6%；金额降幅比上年收窄2.8个百分点，则2022年金额下降4.0%。两年间重量增长 $1.015\times 0.974-1\approx -1.14\%$，金额增长 $0.988\times 0.96-1\approx -5.15\%$，每吨金额增长率 = $\frac{-5.15\%+1.14\%}{1-1.14\%}\approx -4.1\%$。“降幅收窄”说明上年降幅更大。故正确答案为C。")
open(p, "w", encoding="utf-8").write(s)
print("patched")
